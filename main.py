#!/usr/bin/env python3
"""
Idea Harvest Agent - Main orchestrator
Harvests problem statements from various sources and generates validated micro-SaaS ideas
"""

import json
import os
import logging
import time
from datetime import datetime
from typing import List, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from scrapers.reddit_scraper import RedditScraper
from scrapers.hackernews_scraper import HackerNewsScraper
from scrapers.producthunt_scraper import ProductHuntScraper
from ai_processor_ollama import OllamaAIProcessor
from config import TOTAL_TARGET_ITEMS, MAX_ITEMS_PER_SOURCE

class IdeaHarvestAgent:
    def __init__(self):
        self.scrapers = {
            'reddit': RedditScraper(),
            'hackernews': HackerNewsScraper(),
            'producthunt': ProductHuntScraper()
        }
        self.ai_processor = OllamaAIProcessor('llama3.2')
        self.results = {
            'harvest_summary': {},
            'normalized_problems': [],
            'clusters': [],
            'scored_clusters': [],
            'top_ideas': [],
            'validation_playbooks': {}
        }
    
    def harvest_all_sources(self) -> Dict[str, Any]:
        """Harvest problem statements from all sources"""
        logging.info("🌱 Starting idea harvest pipeline")
        start_time = time.time()
        
        all_data = []
        harvest_summary = {}
        
        for source_name, scraper in self.scrapers.items():
            logging.info(f"📡 Harvesting from {source_name} (max {MAX_ITEMS_PER_SOURCE} items)")
            source_start = time.time()
            
            try:
                data = scraper.harvest_problems(MAX_ITEMS_PER_SOURCE)
                all_data.extend(data)
                
                source_time = time.time() - source_start
                harvest_summary[source_name] = {
                    'items_found': len(data),
                    'status': 'success',
                    'time_taken': f"{source_time:.2f}s"
                }
                logging.info(f"✅ {source_name}: {len(data)} items in {source_time:.2f}s")
                
            except Exception as e:
                source_time = time.time() - source_start
                logging.error(f"❌ {source_name} failed after {source_time:.2f}s: {e}")
                harvest_summary[source_name] = {
                    'items_found': 0,
                    'status': 'error',
                    'error': str(e),
                    'time_taken': f"{source_time:.2f}s"
                }
        
        total_time = time.time() - start_time
        self.results['harvest_summary'] = harvest_summary
        self.results['raw_data'] = all_data
        
        logging.info(f"📊 Harvest complete: {len(all_data)} total items in {total_time:.2f}s")
        
        # Log breakdown by source
        for source, summary in harvest_summary.items():
            status = "✅" if summary['status'] == 'success' else "❌"
            logging.info(f"  {status} {source}: {summary['items_found']} items")
        
        return harvest_summary
    
    def process_problems(self) -> List[Dict[str, Any]]:
        """Normalize and cluster the harvested problems"""
        logging.info("🔄 Starting problem processing pipeline")
        start_time = time.time()
        
        raw_data = self.results.get('raw_data', [])
        if not raw_data:
            logging.error("❌ No raw data found to process")
            return []
        
        logging.info(f"📊 Processing {len(raw_data)} raw items")
        
        # Normalize problems
        logging.info("📝 Step 1: Normalizing problem statements")
        norm_start = time.time()
        normalized = self.ai_processor.normalize_problems(raw_data)
        norm_time = time.time() - norm_start
        
        self.results['normalized_problems'] = normalized
        logging.info(f"✅ Normalization: {len(normalized)}/{len(raw_data)} items in {norm_time:.2f}s")
        
        if not normalized:
            logging.error("❌ No problems were normalized successfully")
            return []
        
        # Cluster problems
        logging.info("🔗 Step 2: Clustering problems into themes")
        cluster_start = time.time()
        clusters = self.ai_processor.cluster_problems(normalized)
        cluster_time = time.time() - cluster_start
        
        self.results['clusters'] = clusters
        logging.info(f"✅ Clustering: {len(clusters)} clusters in {cluster_time:.2f}s")
        
        if not clusters:
            logging.error("❌ No clusters were created")
            return []
        
        # Score clusters
        logging.info("📊 Step 3: Scoring clusters")
        score_start = time.time()
        scored_clusters = self.ai_processor.score_clusters(clusters, normalized)
        score_time = time.time() - score_start
        
        self.results['scored_clusters'] = scored_clusters
        
        total_time = time.time() - start_time
        logging.info(f"✅ Processing complete: {len(scored_clusters)} scored clusters in {total_time:.2f}s")
        
        # Log top clusters
        sorted_clusters = sorted(scored_clusters, key=lambda x: x.get('score', {}).get('total', 0), reverse=True)
        logging.info("🏆 Top 3 clusters:")
        for i, cluster in enumerate(sorted_clusters[:3], 1):
            score = cluster.get('score', {}).get('total', 0)
            name = cluster.get('clusterName', 'Unknown')
            logging.info(f"  {i}. {name} (score: {score}/15)")
        
        return scored_clusters
    
    def generate_ideas(self, top_n: int = 12) -> List[Dict[str, Any]]:
        """Generate product ideas for top clusters"""
        logging.info(f"💡 Starting idea generation for top {top_n} clusters")
        start_time = time.time()
        
        scored_clusters = self.results.get('scored_clusters', [])
        if not scored_clusters:
            logging.error("❌ No scored clusters found for idea generation")
            return []
        
        # Sort clusters by score and take top N
        sorted_clusters = sorted(
            scored_clusters, 
            key=lambda x: x.get('score', {}).get('total', 0), 
            reverse=True
        )[:top_n]
        
        logging.info(f"🎯 Selected top {len(sorted_clusters)} clusters for idea generation")
        for i, cluster in enumerate(sorted_clusters, 1):
            score = cluster.get('score', {}).get('total', 0)
            name = cluster.get('clusterName', 'Unknown')
            logging.info(f"  {i}. {name} (score: {score}/15)")
        
        # Generate ideas for each cluster
        ideas = self.ai_processor.generate_ideas(sorted_clusters)
        self.results['top_ideas'] = ideas
        
        idea_time = time.time() - start_time
        logging.info(f"✅ Idea generation complete: {len(ideas)}/{len(sorted_clusters)} ideas in {idea_time:.2f}s")
        
        # Log generated ideas
        for i, idea in enumerate(ideas, 1):
            idea_name = idea.get('ideaName', 'Unknown')
            logging.info(f"  💡 {i}. {idea_name}")
        
        return ideas
    
    def create_validation_playbooks(self) -> Dict[str, Any]:
        """Create validation playbooks for top ideas"""
        logging.info("📋 Starting validation playbook creation")
        start_time = time.time()
        
        top_ideas = self.results.get('top_ideas', [])
        if not top_ideas:
            logging.error("❌ No ideas found for playbook creation")
            return {}
        
        logging.info(f"📝 Creating playbooks for {len(top_ideas)} ideas")
        
        playbooks = {}
        for i, idea in enumerate(top_ideas, 1):
            idea_name = idea.get('ideaName', f'Idea {i}')
            logging.info(f"📋 Creating playbook {i}/{len(top_ideas)}: {idea_name}")
            
            playbook = self.ai_processor.generate_validation_playbook(idea)
            playbooks[idea_name] = playbook
        
        self.results['validation_playbooks'] = playbooks
        
        playbook_time = time.time() - start_time
        logging.info(f"✅ Playbook creation complete: {len(playbooks)} playbooks in {playbook_time:.2f}s")
        
        return playbooks
    
    def save_results(self, filename: str = None) -> str:
        """Save all results to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"idea_harvest_results_{timestamp}.json"
        
        logging.info(f"💾 Saving results to {filename}")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            
            file_size = os.path.getsize(filename)
            logging.info(f"✅ Results saved: {filename} ({file_size:,} bytes)")
            return filename
            
        except Exception as e:
            logging.error(f"❌ Failed to save results: {e}")
            raise
    
    def generate_markdown_report(self, filename: str = None) -> str:
        """Generate human-readable markdown report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"idea_harvest_report_{timestamp}.md"
        
        report = self._create_markdown_report()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📄 Markdown report saved to {filename}")
        return filename
    
    def _create_markdown_report(self) -> str:
        """Create markdown report content"""
        report = f"""# Idea Harvest Report
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Harvest Summary
"""
        
        # Add harvest summary
        for source, data in self.results['harvest_summary'].items():
            report += f"- **{source.title()}**: {data['items_found']} items ({data['status']})\n"
        
        report += f"\n**Total Items**: {len(self.results.get('raw_data', []))}\n\n"
        
        # Add top clusters
        report += "## Top Problem Clusters\n\n"
        for i, cluster in enumerate(self.results['scored_clusters'][:12], 1):
            score = cluster.get('score', {})
            report += f"### {i}. {cluster.get('clusterName', 'Unknown')}\n"
            report += f"- **Score**: {score.get('total', 0)}/15\n"
            report += f"- **Size**: {cluster.get('clusterSize', 0)} problems\n"
            report += f"- **Theme**: {cluster.get('commonTheme', 'N/A')}\n"
            report += f"- **Opportunity**: {cluster.get('opportunitySignal', 'N/A')}\n\n"
        
        # Add top ideas
        report += "## Top Product Ideas\n\n"
        for i, idea in enumerate(self.results['top_ideas'][:5], 1):
            report += f"### {i}. {idea.get('ideaName', 'Unknown')}\n"
            report += f"**Description**: {idea.get('description', 'N/A')}\n\n"
            report += f"**Target Persona**: {idea.get('targetPersona', 'N/A')}\n\n"
            report += f"**Monetization**: {idea.get('monetization', 'N/A')}\n\n"
            report += f"**Validation Method**: {idea.get('validationMethod', 'N/A')}\n\n"
            
            # Add MVP features
            mvp_features = idea.get('mvpFeatures', [])
            if mvp_features:
                report += "**MVP Features**:\n"
                for feature in mvp_features:
                    report += f"- {feature}\n"
                report += "\n"
            
            # Add roadmap
            roadmap = idea.get('roadmap', {})
            if roadmap:
                report += "**2-Week Roadmap**:\n"
                for task in roadmap.get('2week', []):
                    report += f"- {task}\n"
                report += "\n"
                report += "**6-Week Roadmap**:\n"
                for task in roadmap.get('6week', []):
                    report += f"- {task}\n"
                report += "\n"
            
            report += "---\n\n"
        
        return report
    
    def run_full_pipeline(self) -> Dict[str, Any]:
        """Run the complete idea harvesting pipeline"""
        logging.info("🚀 Starting full idea harvest pipeline")
        pipeline_start = time.time()
        
        try:
            # Step 1: Harvest from all sources
            logging.info("📡 Pipeline Step 1: Harvesting from all sources")
            step1_start = time.time()
            self.harvest_all_sources()
            step1_time = time.time() - step1_start
            logging.info(f"✅ Step 1 complete in {step1_time:.2f}s")
            
            # Step 2: Process and cluster problems
            logging.info("🔄 Pipeline Step 2: Processing and clustering problems")
            step2_start = time.time()
            self.process_problems()
            step2_time = time.time() - step2_start
            logging.info(f"✅ Step 2 complete in {step2_time:.2f}s")
            
            # Step 3: Generate ideas
            logging.info("💡 Pipeline Step 3: Generating ideas")
            step3_start = time.time()
            self.generate_ideas()
            step3_time = time.time() - step3_start
            logging.info(f"✅ Step 3 complete in {step3_time:.2f}s")
            
            # Step 4: Create validation playbooks
            logging.info("📋 Pipeline Step 4: Creating validation playbooks")
            step4_start = time.time()
            self.create_validation_playbooks()
            step4_time = time.time() - step4_start
            logging.info(f"✅ Step 4 complete in {step4_time:.2f}s")
            
            # Step 5: Save results
            logging.info("💾 Pipeline Step 5: Saving results")
            step5_start = time.time()
            json_file = self.save_results()
            md_file = self.generate_markdown_report()
            step5_time = time.time() - step5_start
            logging.info(f"✅ Step 5 complete in {step5_time:.2f}s")
            
            total_time = time.time() - pipeline_start
            logging.info(f"🎉 Pipeline completed successfully in {total_time:.2f}s!")
            logging.info(f"📊 Results saved to: {json_file}")
            logging.info(f"📄 Report saved to: {md_file}")
            
            # Final summary
            raw_count = len(self.results.get('raw_data', []))
            cluster_count = len(self.results.get('scored_clusters', []))
            idea_count = len(self.results.get('top_ideas', []))
            playbook_count = len(self.results.get('validation_playbooks', {}))
            
            logging.info("📈 PIPELINE SUMMARY:")
            logging.info(f"  📊 Raw items: {raw_count}")
            logging.info(f"  🔗 Clusters: {cluster_count}")
            logging.info(f"  💡 Ideas: {idea_count}")
            logging.info(f"  📋 Playbooks: {playbook_count}")
            
            return self.results
            
        except Exception as e:
            total_time = time.time() - pipeline_start
            logging.error(f"❌ Pipeline failed after {total_time:.2f}s: {e}")
            raise

def main():
    """Main entry point"""
    agent = IdeaHarvestAgent()
    results = agent.run_full_pipeline()
    
    # Print summary
    print("\n" + "="*50)
    print("📈 SUMMARY")
    print("="*50)
    print(f"Total items harvested: {len(results.get('raw_data', []))}")
    print(f"Clusters identified: {len(results.get('clusters', []))}")
    print(f"Ideas generated: {len(results.get('top_ideas', []))}")
    print(f"Validation playbooks: {len(results.get('validation_playbooks', {}))}")

if __name__ == "__main__":
    main()
