#!/usr/bin/env python3
"""
AI Processor using OLLAMA (100% FREE local AI)
No API costs, runs completely locally
"""

import json
import requests
import re
import logging
import time
from typing import List, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OllamaAIProcessor:
    def __init__(self, model_name: str = "llama3.2"):
        self.model_name = model_name
        self.ollama_url = "http://localhost:11434/api/generate"
        self.results = []
    
    def _call_ollama(self, prompt: str, max_retries: int = 3) -> str:
        """Call OLLAMA API with retry logic"""
        logging.info(f"🤖 Calling OLLAMA with model: {self.model_name}")
        logging.debug(f"📝 Prompt length: {len(prompt)} chars")
        
        for attempt in range(max_retries):
            try:
                logging.info(f"🔄 OLLAMA attempt {attempt + 1}/{max_retries}")
                start_time = time.time()
                
                response = requests.post(
                    self.ollama_url,
                    json={
                        "model": self.model_name,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "top_p": 0.9,
                            "max_tokens": 2000
                        }
                    },
                    timeout=60
                )
                
                elapsed = time.time() - start_time
                logging.info(f"⏱️ OLLAMA response time: {elapsed:.2f}s")
                
                response.raise_for_status()
                result = response.json()
                response_text = result.get('response', '')
                logging.info(f"✅ OLLAMA success - Response length: {len(response_text)} chars")
                return response_text
                
            except requests.exceptions.ConnectionError as e:
                logging.error(f"🔌 OLLAMA connection failed (attempt {attempt + 1}): {e}")
                logging.error("💡 Is OLLAMA running? Try: ollama serve")
            except requests.exceptions.Timeout as e:
                logging.error(f"⏰ OLLAMA timeout (attempt {attempt + 1}): {e}")
            except Exception as e:
                logging.error(f"❌ OLLAMA error (attempt {attempt + 1}): {e}")
                
            if attempt == max_retries - 1:
                logging.warning("🔄 All OLLAMA attempts failed, using mock response")
                return self._mock_response(prompt)
                
        return ""
    
    def _mock_response(self, prompt: str) -> str:
        """Fallback mock response when OLLAMA is not available"""
        if "normalize" in prompt.lower():
            return '{"problem": "Manual data entry is time consuming", "userContext": "Small business owner", "source": "reddit", "tags": ["automation", "productivity"]}'
        elif "cluster" in prompt.lower():
            return '[{"clusterName": "Data Automation", "clusterSize": 15, "examples": ["Manual data entry", "Excel automation"], "commonTheme": "Automating repetitive tasks", "opportunitySignal": "High"}]'
        elif "score" in prompt.lower():
            return '{"frequency": 4, "pain": 5, "willingness": 3, "total": 12, "justification": "Users express frustration with manual processes"}'
        elif "idea" in prompt.lower():
            return '{"ideaName": "DataFlow Automator", "description": "AI-powered data entry automation", "timing": "AI tools becoming accessible", "validationMethod": "Reddit survey", "monetization": "SaaS $29/month", "targetPersona": "Small business owners", "mvpFeatures": ["CSV import", "Automation rules", "Excel export"], "roadmap": {"2week": ["Build landing page", "Create automation engine"], "6week": ["Add AI features", "Integrate tools"]}}'
        else:
            return '{"validationChannels": ["r/smallbusiness"], "experiments": [{"name": "Reddit Survey", "description": "Post survey", "timeline": "3 days"}], "landingPageCopy": "Stop wasting time on manual data entry", "outreachMessages": ["Hi! Building a tool to automate data entry"], "metrics": {"go": "50+ signups", "iterate": "20+ signups", "kill": "<10 signups"}}'
    
    def normalize_problems(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Normalize raw problem statements using OLLAMA"""
        logging.info(f"📝 Starting normalization of {len(raw_data)} items")
        normalized = []
        
        for i, item in enumerate(raw_data, 1):
            try:
                logging.info(f"🔄 Processing item {i}/{len(raw_data)} from {item.get('source', 'unknown')}")
                logging.debug(f"📄 Title: {item.get('title', '')[:100]}...")
                
                prompt = f"""
                You are an AI idea-normalizer. 
                Input: Raw problem statement from {item['source']}
                Title: {item.get('title', '')}
                Content: {item.get('content', '')}
                Comments: {item.get('comments', [])}
                
                Task:
                1. Extract the **main problem** in plain words.
                2. Extract any **attempted solutions or context**.
                3. Return structured JSON:
                {{
                  "problem": "...",
                  "userContext": "...",
                  "source": "{item['source']}",
                  "tags": ["..."]
                }}
                """
                
                response = self._call_ollama(prompt)
                result = self._parse_json_response(response)
                
                if result:
                    result['original_data'] = item
                    normalized.append(result)
                    logging.info(f"✅ Item {i} normalized successfully")
                else:
                    logging.warning(f"⚠️ Item {i} failed to normalize - invalid JSON response")
                
            except Exception as e:
                logging.error(f"❌ Error normalizing item {i}: {e}")
                continue
        
        logging.info(f"✅ Normalization complete: {len(normalized)}/{len(raw_data)} items processed")
        return normalized
    
    def cluster_problems(self, normalized_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Cluster normalized problems using OLLAMA"""
        logging.info(f"🔗 Starting clustering of {len(normalized_data)} normalized problems")
        
        try:
            problems_text = [item['problem'] for item in normalized_data]
            logging.info(f"📊 Processing {len(problems_text)} problems for clustering")
            
            # Use all problems for better clustering
            problems_subset = problems_text
            logging.info(f"🎯 Using all {len(problems_subset)} problems for clustering")
            
            prompt = f"""
            You are a micro-SaaS opportunity finder. Find problems suitable for small, focused SaaS tools.
            
            Problems to analyze:
            {json.dumps(problems_subset, indent=2)}
            
            Rules:
            1. Each problem can be its own micro-SaaS opportunity
            2. Look for problems that can be solved with simple software tools
            3. Focus on problems that small businesses/individuals would pay $10-100/month for
            4. Avoid problems requiring complex infrastructure or large teams
            
            Return JSON array of micro-SaaS opportunities:
            [
              {{
                "clusterName": "Social Media Scheduling",
                "clusterSize": 1,
                "examples": ["Managing multiple social accounts manually"],
                "commonTheme": "Time-consuming social media management",
                "opportunitySignal": "High",
                "microSaasViability": "Perfect for solo developer - simple scheduling + API integrations"
              }}
            ]
            """
            
            logging.info("🤖 Sending clustering request to OLLAMA...")
            response = self._call_ollama(prompt)
            clusters = self._parse_json_response(response)
            
            if clusters and isinstance(clusters, list):
                logging.info(f"✅ Successfully created {len(clusters)} clusters")
                for i, cluster in enumerate(clusters, 1):
                    logging.debug(f"📋 Cluster {i}: {cluster.get('clusterName', 'Unknown')} ({cluster.get('clusterSize', 0)} items)")
                return clusters
            else:
                logging.warning("⚠️ Invalid clustering response, using fallback")
                return self._fallback_clustering(normalized_data)
            
        except Exception as e:
            logging.error(f"❌ Error during clustering: {e}")
            return self._fallback_clustering(normalized_data)
    
    def score_clusters(self, clusters: List[Dict[str, Any]], normalized_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Score clusters using OLLAMA"""
        logging.info(f"📊 Starting scoring of {len(clusters)} clusters")
        scored_clusters = []
        
        for i, cluster in enumerate(clusters, 1):
            try:
                cluster_name = cluster.get('clusterName', f'Cluster {i}')
                logging.info(f"🎯 Scoring cluster {i}/{len(clusters)}: {cluster_name}")
                
                prompt = f"""
                You are an AI opportunity scorer.
                Input: Cluster of user problems.
                Cluster: {json.dumps(cluster, indent=2)}
                
                Score each cluster:
                - Frequency: 1–5 (based on how many times this problem appears)
                - Pain Intensity: 1–5 (how frustrated users seem)
                - Market Willingness: 1–5 (mentions of paying, expensive alternatives)
                
                Output as JSON:
                {{
                  "cluster": "{cluster_name}",
                  "score": {{
                    "frequency": 4,
                    "pain": 5,
                    "willingness": 3,
                    "total": 12
                  }},
                  "justification": "Users repeatedly express frustration with ..."
                }}
                """
                
                response = self._call_ollama(prompt)
                score_result = self._parse_json_response(response)
                
                if score_result:
                    cluster.update(score_result)
                    scored_clusters.append(cluster)
                    total_score = score_result.get('score', {}).get('total', 0)
                    logging.info(f"✅ Cluster {i} scored: {total_score}/15")
                else:
                    logging.warning(f"⚠️ Cluster {i} scoring failed, using fallback")
                    # Fallback scoring
                    cluster['score'] = {
                        "frequency": 4,
                        "pain": 5,
                        "willingness": 3,
                        "total": 12
                    }
                    cluster['justification'] = "Users express frustration with manual processes"
                    scored_clusters.append(cluster)
                
            except Exception as e:
                logging.error(f"❌ Error scoring cluster {i}: {e}")
                continue
        
        logging.info(f"✅ Scoring complete: {len(scored_clusters)}/{len(clusters)} clusters scored")
        return scored_clusters
    
    def generate_ideas(self, top_clusters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate product ideas using OLLAMA"""
        logging.info(f"💡 Starting idea generation for {len(top_clusters)} clusters")
        ideas = []
        
        for i, cluster in enumerate(top_clusters, 1):
            try:
                cluster_name = cluster.get('clusterName', f'Cluster {i}')
                logging.info(f"🚀 Generating idea {i}/{len(top_clusters)} for: {cluster_name}")
                
                prompt = f"""
                You are a micro-SaaS idea generator. Create a simple, focused SaaS tool for solo developers.
                
                Problem cluster: {json.dumps(cluster, indent=2)}
                
                Generate a micro-SaaS idea that:
                - Solves ONE specific problem very well
                - Can be built by 1 person in 2-8 weeks
                - Targets small businesses or individuals
                - Pricing: $10-100/month
                - Uses simple tech stack (no AI/ML unless essential)
                
                Return as JSON:
                {{
                  "ideaName": "TaskFlow Scheduler",
                  "description": "Simple task scheduling tool for small teams",
                  "timing": "Remote work trend + need for async coordination",
                  "validationMethod": "Post in r/smallbusiness asking about scheduling pain",
                  "monetization": "$29/month per team (up to 10 users)",
                  "targetPersona": "Small business owners with 3-10 remote employees",
                  "mvpFeatures": ["Task creation", "Due date tracking", "Email notifications"],
                  "techStack": "React + Node.js + PostgreSQL",
                  "soloDevTime": "4-6 weeks",
                  "roadmap": {{
                    "week1-2": ["Basic task CRUD", "User auth", "Simple UI"],
                    "week3-4": ["Email notifications", "Team invites", "Basic dashboard"],
                    "week5-6": ["Polish UI", "Payment integration", "Deploy"]
                  }}
                }}
                """
                
                response = self._call_ollama(prompt)
                idea = self._parse_json_response(response)
                
                if idea:
                    idea['cluster'] = cluster
                    ideas.append(idea)
                    idea_name = idea.get('ideaName', 'Unknown Idea')
                    logging.info(f"✅ Generated idea {i}: {idea_name}")
                else:
                    logging.warning(f"⚠️ Failed to generate idea {i} - invalid response")
                
            except Exception as e:
                logging.error(f"❌ Error generating idea {i}: {e}")
                continue
        
        logging.info(f"✅ Idea generation complete: {len(ideas)}/{len(top_clusters)} ideas generated")
        return ideas
    
    def generate_validation_playbook(self, idea: Dict[str, Any]) -> Dict[str, Any]:
        """Generate validation playbook using OLLAMA"""
        idea_name = idea.get('ideaName', 'Unknown Idea')
        logging.info(f"📋 Generating validation playbook for: {idea_name}")
        
        try:
            prompt = f"""
            You are a startup validation coach.
            Input: Startup idea
            Idea: {json.dumps(idea, indent=2)}
            
            Generate validation playbook:
            - Subreddits / Discords / Slack groups to test
            - 2 fast validation experiments (<7 days)
            - Landing page copy sample
            - First 10 outreach messages
            - Metrics to watch & thresholds
            
            Return as JSON:
            {{
              "validationChannels": ["..."],
              "experiments": [
                {{
                  "name": "...",
                  "description": "...",
                  "timeline": "..."
                }}
              ],
              "landingPageCopy": "...",
              "outreachMessages": ["..."],
              "metrics": {{
                "go": "...",
                "iterate": "...",
                "kill": "..."
              }}
            }}
            """
            
            response = self._call_ollama(prompt)
            playbook = self._parse_json_response(response)
            
            if playbook:
                logging.info(f"✅ Validation playbook generated for: {idea_name}")
                return playbook
            else:
                logging.warning(f"⚠️ Failed to generate playbook for: {idea_name}")
                return {}
            
        except Exception as e:
            logging.error(f"❌ Error generating validation playbook for {idea_name}: {e}")
            return {}
    
    def _parse_json_response(self, text: str) -> Any:
        """Parse JSON from AI response"""
        try:
            logging.debug(f"🔍 Parsing JSON from response (length: {len(text)} chars)")
            
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                json_text = json_match.group()
                logging.debug(f"📄 Found JSON block (length: {len(json_text)} chars)")
                result = json.loads(json_text)
                logging.debug("✅ JSON parsed successfully")
                return result
            else:
                logging.warning("⚠️ No JSON block found in response")
                logging.debug(f"📝 Response preview: {text[:200]}...")
                return None
        except json.JSONDecodeError as e:
            logging.error(f"❌ JSON decode error: {e}")
            logging.debug(f"📝 Problematic text: {text[:500]}...")
            return None
        except Exception as e:
            logging.error(f"❌ Error parsing JSON: {e}")
            return None
    
    def _fallback_clustering(self, normalized_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Fallback clustering when OLLAMA fails"""
        return [
            {
                "clusterName": "Data Automation",
                "clusterSize": len(normalized_data),
                "examples": [item['problem'] for item in normalized_data[:3]],
                "commonTheme": "Automating repetitive tasks",
                "opportunitySignal": "High"
            }
        ]
