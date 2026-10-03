import requests
import json
import time
import logging
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, SUBREDDITS, SEARCH_QUERIES

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RedditScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': REDDIT_USER_AGENT})
        self.results = []
        self.use_api = False
        
        logging.info("🔴 Initializing Reddit scraper")
        
        # Try to authenticate with Reddit API
        if REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET:
            logging.info("🔑 Attempting Reddit API authentication")
            self.use_api = self._authenticate()
        else:
            logging.info("⚠️ No Reddit API credentials provided")
        
        if not self.use_api:
            logging.info("📰 Using Reddit JSON feeds (no authentication required)")
    
    def _authenticate(self) -> bool:
        """Authenticate with Reddit API"""
        try:
            auth = requests.auth.HTTPBasicAuth(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)
            data = {'grant_type': 'client_credentials'}
            headers = {'User-Agent': REDDIT_USER_AGENT}
            
            response = requests.post('https://www.reddit.com/api/v1/access_token',
                                   auth=auth, data=data, headers=headers)
            
            print("response from the reddit api is " + response.text)
            if response.status_code == 200:
                token = response.json()['access_token']
                self.session.headers.update({'Authorization': f'bearer {token}'})
                return True
            else:
                print(f"Reddit API auth failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"Reddit API auth error: {e}")
            return False
    
    def search_subreddit(self, subreddit_name: str, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for posts in a specific subreddit"""
        try:
            print(f"🔍 Fetching from r/{subreddit_name} (limit: {limit}) with the query {query}")
            
            if self.use_api:
                # Use authenticated API
                url = f'https://oauth.reddit.com/r/{subreddit_name}/search'
                params = {'q': query, 'sort': 'top', 't': 'month', 'limit': limit}
                print("params from the reddit api is " + str(params))
                print("🔑 Using authenticated Reddit API")
            else:
                # Use public JSON feed
                url = f'https://www.reddit.com/r/{subreddit_name}/top.json'
                params = {'t': 'month', 'limit': limit}
                print("params from the reddit api is " + str(params))
                print("📰 Using public Reddit JSON feed")
            
            response = self.session.get(url, params=params)
            print("response from the reddit api is " + response.text)
            
            if response.status_code != 200:
                logging.error(f"❌ r/{subreddit_name} returned {response.status_code}")
                return self._get_mock_data(subreddit_name, query, limit)
            
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            print(f"📄 Retrieved {len(posts)} raw posts from r/{subreddit_name}")
            
            results = []
            for post_data in posts:
                post = post_data['data']
                
                # Filter by query if not using API search
                if not self.use_api and query and query.lower() not in (post.get('title', '') + post.get('selftext', '')).lower():
                    continue
                
                result = {
                    'source': 'reddit',
                    'subreddit': subreddit_name,
                    'title': post.get('title', ''),
                    'content': post.get('selftext', ''),
                    'comments': self._get_comments_with_retry(post.get('permalink', ''), limit=5),
                    'url': f"https://reddit.com{post.get('permalink', '')}",
                    'score': post.get('score', 0),
                    'created_utc': post.get('created_utc', 0),
                    'timestamp': datetime.fromtimestamp(post.get('created_utc', 0)).isoformat(),
                    'tags': self._extract_tags(post.get('title', '') + ' ' + post.get('selftext', ''))
                }
                results.append(result)
            
            print(f"✅ Processed {len(results)} posts from r/{subreddit_name}")
            return results[:limit]
            
        except Exception as e:
            print(f"❌ Error searching r/{subreddit_name}: {e}")
            return self._get_mock_data(subreddit_name, query, limit)
    
    def _get_comments_with_retry(self, permalink: str, limit: int = 5, max_retries: int = 3) -> List[str]:
        """Fetch comments with rate limit handling"""
        for attempt in range(max_retries):
            try:
                if not permalink:
                    return []
                
                url = f"https://www.reddit.com{permalink}.json"
                response = self.session.get(url)
                
                if response.status_code == 429:  # Rate limited
                    wait_time = 60 * (attempt + 1)  # Exponential backoff
                    logging.warning(f"⏳ Rate limited, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                
                if response.status_code != 200:
                    return []
                
                data = response.json()
                if len(data) < 2:
                    return []
                
                comments = data[1]['data']['children']
                comment_texts = []
                
                for comment in comments[:limit]:
                    if comment['kind'] == 't1':
                        body = comment['data'].get('body', '')
                        if body and body != '[deleted]' and len(body) > 10:
                            comment_texts.append(body)
                
                # Rate limiting between requests
                time.sleep(1)
                return comment_texts
                
            except Exception as e:
                logging.debug(f"Failed to get comments (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                    
        return []
    
    def _extract_tags(self, text: str) -> List[str]:
        """Extract relevant tags from text"""
        tags = []
        text_lower = text.lower()
        
        # Common problem indicators
        problem_indicators = [
            'automation', 'manual', 'time consuming', 'frustrating', 'expensive',
            'integration', 'workflow', 'productivity', 'efficiency', 'pain point',
            'wish', 'need', 'want', 'looking for', 'tool', 'solution', 'help'
        ]
        
        for indicator in problem_indicators:
            if indicator in text_lower:
                tags.append(indicator)
        
        return list(set(tags))
    
    def harvest_problems(self, max_items: int = 50) -> List[Dict[str, Any]]:
        """Harvest problem statements from Reddit"""
        logging.info(f"📡 Starting Reddit harvest (max {max_items} items)")
        start_time = time.time()
        all_results = []
        
        for i, subreddit in enumerate(SUBREDDITS, 1):
            logging.info(f"🔍 Searching r/{subreddit} ({i}/{len(SUBREDDITS)})")
            
            # Get top posts from subreddit
            results = self.search_subreddit(subreddit, 'is there a tool for', limit=10)
            all_results.extend(results)
            logging.info(f"✅ r/{subreddit}: {len(results)} posts found")
            
            # Rate limiting
            time.sleep(2)
            
            if len(all_results) >= max_items:
                logging.info(f"🎯 Reached max items limit ({max_items})")
                break
        
        # Remove duplicates and return top results
        unique_results = self._deduplicate(all_results)
        self.results = unique_results[:max_items]
        
        harvest_time = time.time() - start_time
        logging.info(f"✅ Reddit harvest complete: {len(self.results)} unique items in {harvest_time:.2f}s")
        
        return self.results
    
    def _deduplicate(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate results based on title similarity"""
        unique_results = []
        seen_titles = set()
        
        for result in results:
            title_key = result['title'].lower().strip()
            if title_key not in seen_titles and len(title_key) > 10:
                seen_titles.add(title_key)
                unique_results.append(result)
        
        return unique_results
    
    def _get_mock_data(self, subreddit_name: str, query: str, limit: int) -> List[Dict[str, Any]]:
        """Return mock data when Reddit API is not available"""
        mock_posts = [
            {
                'source': 'reddit',
                'subreddit': subreddit_name,
                'title': f'I wish there was a tool to {query}',
                'content': f'I\'m looking for a solution to {query}. Current options are too expensive or don\'t work well.',
                'comments': ['I use X but it\'s not great', 'Try Y tool', 'I need something simpler'],
                'url': f'https://reddit.com/r/{subreddit_name}/mock1',
                'score': 15,
                'created_utc': 1640995200,
                'timestamp': datetime.now().isoformat(),
                'tags': ['automation', 'productivity', 'tool']
            },
            {
                'source': 'reddit',
                'subreddit': subreddit_name,
                'title': f'Anyone know a good tool for {query}?',
                'content': f'I\'ve been struggling with {query} and need recommendations.',
                'comments': ['Buffer is good but expensive', 'Try Hootsuite', 'I built my own'],
                'url': f'https://reddit.com/r/{subreddit_name}/mock2',
                'score': 8,
                'created_utc': 1640995200,
                'timestamp': datetime.now().isoformat(),
                'tags': ['recommendation', 'tool', 'help']
            }
        ]
        return mock_posts[:limit]
    
    def save_results(self, filename: str = 'reddit_data.json'):
        """Save results to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            
            file_size = os.path.getsize(filename) if os.path.exists(filename) else 0
            logging.info(f"💾 Saved {len(self.results)} Reddit results to {filename} ({file_size:,} bytes)")
        except Exception as e:
            logging.error(f"❌ Failed to save Reddit results: {e}")
