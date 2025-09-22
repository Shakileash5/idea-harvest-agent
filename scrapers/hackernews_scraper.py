import requests
import json
import time
from datetime import datetime
from typing import List, Dict, Any
from config import SEARCH_QUERIES
import ssl
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class HackerNewsScraper:
    def __init__(self):
        self.base_url = "https://hacker-news.firebaseio.com/v0"
        self.results = []
        
        # Create session with retry strategy and SSL handling
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Disable SSL warnings for Firebase API
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    def get_top_stories(self, limit: int = 100) -> List[int]:
        """Get top story IDs from Hacker News"""
        try:
            response = self.session.get(f"{self.base_url}/topstories.json", timeout=10)
            response.raise_for_status()
            return response.json()[:limit]
        except Exception as e:
            print(f"Error fetching top stories: {e}")
            return []
    
    def get_story_details(self, story_id: int) -> Dict[str, Any]:
        """Get detailed information about a specific story"""
        try:
            response = self.session.get(f"{self.base_url}/item/{story_id}.json", timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching story {story_id}: {e}")
            return {}
    
    def get_comments(self, story_id: int, limit: int = 10) -> List[str]:
        """Get comments for a story"""
        try:
            story = self.get_story_details(story_id)
            if not story or 'kids' not in story:
                return []
            
            comments = []
            for comment_id in story['kids'][:limit]:
                comment = self.get_story_details(comment_id)
                if comment and 'text' in comment:
                    comments.append(comment['text'])
                time.sleep(0.1)  # Rate limiting
            
            return comments
        except Exception as e:
            print(f"Error fetching comments for {story_id}: {e}")
            return []
    
    def is_problem_statement(self, text: str) -> bool:
        """Check if text contains problem statement indicators"""
        if not text:
            return False
        
        text_lower = text.lower()
        problem_indicators = [
            'i wish', 'i need', 'looking for', 'anyone know', 'how do you',
            'is there a way', 'help with', 'frustrated', 'pain point',
            'manual process', 'time consuming', 'expensive', 'alternative'
        ]
        
        return any(indicator in text_lower for indicator in problem_indicators)
    
    def harvest_problems(self, max_items: int = 50) -> List[Dict[str, Any]]:
        """Harvest problem statements from Hacker News"""
        all_results = []
        story_ids = self.get_top_stories(200)
        
        for story_id in story_ids:
            if len(all_results) >= max_items:
                break
            
            story = self.get_story_details(story_id)
            if not story or story.get('type') != 'story':
                continue
            
            # Check if story title or text contains problem indicators
            story_text = f"{story.get('title', '')} {story.get('text', '')}"
            
            if self.is_problem_statement(story_text):
                comments = self.get_comments(story_id, limit=5)
                
                result = {
                    'source': 'hackernews',
                    'title': story.get('title', ''),
                    'content': story.get('text', ''),
                    'comments': comments,
                    'url': f"https://news.ycombinator.com/item?id={story_id}",
                    'score': story.get('score', 0),
                    'created_utc': story.get('time', 0),
                    'timestamp': datetime.fromtimestamp(story.get('time', 0)).isoformat(),
                    'tags': self._extract_tags(story_text + ' ' + ' '.join(comments))
                }
                all_results.append(result)
            
            time.sleep(0.1)  # Rate limiting
        
        return all_results[:max_items]
    
    def _extract_tags(self, text: str) -> List[str]:
        """Extract relevant tags from text"""
        tags = []
        text_lower = text.lower()
        
        # Common problem indicators
        problem_indicators = [
            'automation', 'manual', 'time consuming', 'frustrating', 'expensive',
            'integration', 'workflow', 'productivity', 'efficiency', 'pain point',
            'wish', 'need', 'want', 'looking for', 'tool', 'solution', 'help',
            'api', 'saas', 'startup', 'business', 'developer', 'marketing'
        ]
        
        for indicator in problem_indicators:
            if indicator in text_lower:
                tags.append(indicator)
        
        return list(set(tags))
    
    def save_results(self, filename: str = 'hackernews_data.json'):
        """Save results to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
