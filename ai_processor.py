import json
import google.generativeai as genai
from typing import List, Dict, Any
from config import GOOGLE_AI_API_KEY
import re

class AIProcessor:
    def __init__(self):
        if GOOGLE_AI_API_KEY:
            genai.configure(api_key=GOOGLE_AI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
            print("Google AI API key not provided, using mock processing")
    
    def normalize_problems(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Normalize raw problem statements into structured format"""
        if not self.model:
            return self._mock_normalize(raw_data)
        
        normalized = []
        
        for item in raw_data:
            try:
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
                
                response = self.model.generate_content(prompt)
                result = self._parse_json_response(response.text)
                
                if result:
                    result['original_data'] = item
                    normalized.append(result)
                
            except Exception as e:
                print(f"Error normalizing item: {e}")
                continue
        
        return normalized
    
    def cluster_problems(self, normalized_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Cluster normalized problems into themes"""
        if not self.model:
            return self._mock_cluster(normalized_data)
        
        try:
            # Prepare data for clustering
            problems_text = [item['problem'] for item in normalized_data]
            
            prompt = f"""
            You are an AI clustering engine.
            Input: A list of normalized problem statements in JSON.
            Problems: {json.dumps(problems_text[:50], indent=2)}
            
            Task:
            - Group them into **niches** based on similarity.
            - For each cluster, output:
            {{
              "clusterName": "...",
              "clusterSize": 12,
              "examples": ["...","..."],
              "commonTheme": "...",
              "opportunitySignal": "High/Medium/Low"
            }}
            
            Return as JSON array.
            """
            
            response = self.model.generate_content(prompt)
            clusters = self._parse_json_response(response.text)
            
            return clusters if clusters else []
            
        except Exception as e:
            print(f"Error clustering problems: {e}")
            return []
    
    def score_clusters(self, clusters: List[Dict[str, Any]], normalized_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Score clusters based on frequency, pain intensity, and market willingness"""
        if not self.model:
            return self._mock_score(clusters)
        
        scored_clusters = []
        
        for cluster in clusters:
            try:
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
                  "cluster": "{cluster['clusterName']}",
                  "score": {{
                    "frequency": 4,
                    "pain": 5,
                    "willingness": 3,
                    "total": 12
                  }},
                  "justification": "Users repeatedly express frustration with ..."
                }}
                """
                
                response = self.model.generate_content(prompt)
                score_result = self._parse_json_response(response.text)
                
                if score_result:
                    cluster.update(score_result)
                    scored_clusters.append(cluster)
                
            except Exception as e:
                print(f"Error scoring cluster: {e}")
                continue
        
        return scored_clusters
    
    def generate_ideas(self, top_clusters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate product ideas for top clusters"""
        if not self.model:
            return self._mock_generate_ideas(top_clusters)
        
        ideas = []
        
        for cluster in top_clusters:
            try:
                prompt = f"""
                You are an AI startup ideator.
                Input: Scored cluster of user problems.
                Cluster: {json.dumps(cluster, indent=2)}
                
                For this cluster, propose 1 startup idea:
                - Idea name
                - What it does (one-liner)
                - Why now (timing)
                - 1-sentence validation method
                - Rough monetization path
                - Target customer persona
                - MVP feature list
                - 2-week and 6-week solo MVP roadmap
                
                Return as JSON:
                {{
                  "ideaName": "...",
                  "description": "...",
                  "timing": "...",
                  "validationMethod": "...",
                  "monetization": "...",
                  "targetPersona": "...",
                  "mvpFeatures": ["..."],
                  "roadmap": {{
                    "2week": ["..."],
                    "6week": ["..."]
                  }}
                }}
                """
                
                response = self.model.generate_content(prompt)
                idea = self._parse_json_response(response.text)
                
                if idea:
                    idea['cluster'] = cluster
                    ideas.append(idea)
                
            except Exception as e:
                print(f"Error generating idea for cluster: {e}")
                continue
        
        return ideas
    
    def generate_validation_playbook(self, idea: Dict[str, Any]) -> Dict[str, Any]:
        """Generate validation playbook for an idea"""
        if not self.model:
            return self._mock_validation_playbook(idea)
        
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
            
            response = self.model.generate_content(prompt)
            playbook = self._parse_json_response(response.text)
            
            return playbook if playbook else {}
            
        except Exception as e:
            print(f"Error generating validation playbook: {e}")
            return {}
    
    def _parse_json_response(self, text: str) -> Any:
        """Parse JSON from AI response"""
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return None
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            return None
    
    def _mock_normalize(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Mock normalization for testing"""
        return [
            {
                "problem": "Manual data entry is time consuming",
                "userContext": "Small business owner spending hours on data entry",
                "source": "reddit",
                "tags": ["automation", "productivity", "data entry"]
            }
        ]
    
    def _mock_cluster(self, normalized_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Mock clustering for testing"""
        return [
            {
                "clusterName": "Data Automation",
                "clusterSize": 15,
                "examples": ["Manual data entry", "Excel automation"],
                "commonTheme": "Automating repetitive data tasks",
                "opportunitySignal": "High"
            }
        ]
    
    def _mock_score(self, clusters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Mock scoring for testing"""
        for cluster in clusters:
            cluster['score'] = {
                "frequency": 4,
                "pain": 5,
                "willingness": 3,
                "total": 12
            }
            cluster['justification'] = "Users repeatedly express frustration with manual processes"
        return clusters
    
    def _mock_generate_ideas(self, top_clusters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Mock idea generation for testing"""
        return [
            {
                "ideaName": "DataFlow Automator",
                "description": "AI-powered tool that automates data entry and processing",
                "timing": "AI tools are becoming more accessible and businesses need efficiency",
                "validationMethod": "Post in r/smallbusiness asking about data entry pain points",
                "monetization": "SaaS subscription $29/month",
                "targetPersona": "Small business owners, 1-50 employees, $100K-1M revenue",
                "mvpFeatures": ["CSV import", "Basic automation rules", "Export to Excel"],
                "roadmap": {
                    "2week": ["Build landing page", "Create basic automation engine"],
                    "6week": ["Add AI features", "Integrate with popular tools"]
                }
            }
        ]
    
    def _mock_validation_playbook(self, idea: Dict[str, Any]) -> Dict[str, Any]:
        """Mock validation playbook for testing"""
        return {
            "validationChannels": ["r/smallbusiness", "r/entrepreneur", "LinkedIn groups"],
            "experiments": [
                {
                    "name": "Reddit Survey",
                    "description": "Post survey about data entry pain points",
                    "timeline": "3 days"
                }
            ],
            "landingPageCopy": "Stop wasting time on manual data entry. Automate your workflow in minutes.",
            "outreachMessages": ["Hi! I'm building a tool to automate data entry. Would you be interested in testing it?"],
            "metrics": {
                "go": "50+ signups in first week",
                "iterate": "20+ signups in first week",
                "kill": "Less than 10 signups in first week"
            }
        }
