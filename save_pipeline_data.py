#!/usr/bin/env python3

import json
import logging
from main import IdeaHarvestAgent

def save_all_pipeline_data():
    """Save all pipeline data at each step"""
    print("💾 Extracting and saving all pipeline data...")
    
    # Load the agent with existing data
    agent = IdeaHarvestAgent()
    
    # Load raw harvest data
    try:
        with open('test_harvest_raw.json', 'r') as f:
            data = json.load(f)
        
        raw_data = data.get('raw_data', [])
        print(f"📊 Found {len(raw_data)} raw items")
        
        # Save individual source files
        sources = {}
        for item in raw_data:
            source = item.get('source', 'unknown')
            if source not in sources:
                sources[source] = []
            sources[source].append(item)
        
        # Save by source
        for source, items in sources.items():
            filename = f"{source}_data.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(items, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved {len(items)} items to {filename}")
        
        # Save normalized data if it exists
        normalized = data.get('normalized_problems', [])
        if normalized:
            with open('normalized_problems.json', 'w', encoding='utf-8') as f:
                json.dump(normalized, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved {len(normalized)} normalized problems")
        
        # Save clusters if they exist
        clusters = data.get('clusters', [])
        if clusters:
            with open('clusters.json', 'w', encoding='utf-8') as f:
                json.dump(clusters, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved {len(clusters)} clusters")
        
        # Save scored clusters if they exist
        scored_clusters = data.get('scored_clusters', [])
        if scored_clusters:
            with open('scored_clusters.json', 'w', encoding='utf-8') as f:
                json.dump(scored_clusters, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved {len(scored_clusters)} scored clusters")
        
        # Save ideas if they exist
        ideas = data.get('top_ideas', [])
        if ideas:
            with open('generated_ideas.json', 'w', encoding='utf-8') as f:
                json.dump(ideas, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved {len(ideas)} generated ideas")
        
        # Save playbooks if they exist
        playbooks = data.get('validation_playbooks', {})
        if playbooks:
            with open('validation_playbooks.json', 'w', encoding='utf-8') as f:
                json.dump(playbooks, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved {len(playbooks)} validation playbooks")
        
        print("\n✅ All available data extracted and saved!")
        print("\n📁 Files created:")
        print("  - reddit_data.json (Reddit posts)")
        print("  - hackernews_data.json (Hacker News stories)")  
        print("  - producthunt_data.json (Product Hunt products)")
        if normalized:
            print("  - normalized_problems.json (AI-processed problems)")
        if clusters:
            print("  - clusters.json (Problem clusters)")
        if scored_clusters:
            print("  - scored_clusters.json (Scored clusters)")
        if ideas:
            print("  - generated_ideas.json (Product ideas)")
        if playbooks:
            print("  - validation_playbooks.json (Validation strategies)")
            
    except FileNotFoundError:
        print("❌ test_harvest_raw.json not found. Run the harvest first.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    save_all_pipeline_data()