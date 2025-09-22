import requests
import json
import time
from datetime import datetime
from typing import List, Dict, Any
from config import SEARCH_QUERIES, PRODUCTHUNT_API_KEY, PRODUCTHUNT_API_SECRET, PRODUCTHUNT_REDIRECT_URI

class ProductHuntScraper:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or PRODUCTHUNT_API_KEY
        self.api_secret = PRODUCTHUNT_API_SECRET
        self.redirect_uri = PRODUCTHUNT_REDIRECT_URI
        self.base_url = "https://api.producthunt.com/v2/api/graphql"
        self.results = []
        self.access_token = None
    
    def get_access_token(self) -> str:
        """Get Product Hunt access token using client credentials"""
        if not self.api_key or not self.api_secret:
            return None
        
        try:
            # Product Hunt uses OAuth2 client credentials flow
            token_url = "https://api.producthunt.com/v2/oauth/token"
            data = {
                'client_id': self.api_key,
                'client_secret': self.api_secret,
                'grant_type': 'client_credentials'
            }
            
            response = requests.post(token_url, data=data, timeout=10)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data.get('access_token')
            return self.access_token
            
        except Exception as e:
            print(f"Error getting Product Hunt access token: {e}")
            return None
    
    def search_products(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search for products on Product Hunt"""
        if not self.api_key:
            print("Product Hunt API key not provided, using mock data")
            return self._get_mock_data()
        
        # Get access token
        if not self.access_token:
            self.access_token = self.get_access_token()
            if not self.access_token:
                print("Failed to get Product Hunt access token, using mock data")
                return self._get_mock_data()
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        # GraphQL query to get recent posts (Product Hunt doesn't have search in free tier)
        graphql_query = {
            "query": """
            query GetPosts($first: Int!) {
                posts(first: $first) {
                    edges {
                        node {
                            id
                            name
                            tagline
                            description
                            url
                            votesCount
                            commentsCount
                            createdAt
                            comments {
                                edges {
                                    node {
                                        body
                                    }
                                }
                            }
                        }
                    }
                }
            }
            """,
            "variables": {
                "first": limit
            }
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=graphql_query)
            response.raise_for_status()
            data = response.json()
            
            results = []
            if 'data' in data and 'posts' in data['data']:
                for edge in data['data']['posts']['edges']:
                    node = edge['node']
                    comments = []
                    if 'comments' in node and 'edges' in node['comments']:
                        comments = [comment['node']['body'] for comment in node['comments']['edges']]
                    
                    result = {
                        'source': 'producthunt',
                        'title': node.get('name', ''),
                        'content': node.get('description', ''),
                        'tagline': node.get('tagline', ''),
                        'comments': comments,
                        'url': node.get('url', ''),
                        'votes': node.get('votesCount', 0),
                        'comments_count': node.get('commentsCount', 0),
                        'created_at': node.get('createdAt', ''),
                        'timestamp': datetime.now().isoformat(),
                        'tags': self._extract_tags(node.get('name', '') + ' ' + node.get('description', ''))
                    }
                    results.append(result)
            
            return results
        except Exception as e:
            print(f"Error searching Product Hunt: {e}")
            return []
    
    def _get_mock_data(self) -> List[Dict[str, Any]]:
        """Return mock data when API key is not available"""
        mock_products = [
            {
                'source': 'producthunt',
                'title': 'SocialFlow Pro',
                'content': 'AI-powered social media management platform that automates posting across multiple platforms',
                'tagline': 'Automate your social media posting',
                'comments': ['I wish this had better analytics', 'Needs integration with more platforms', 'Too expensive for small businesses'],
                'url': 'https://producthunt.com/socialflow-pro',
                'votes': 150,
                'comments_count': 25,
                'created_at': '2024-01-01T00:00:00Z',
                'timestamp': datetime.now().isoformat(),
                'tags': ['automation', 'social media', 'productivity']
            },
            {
                'source': 'producthunt',
                'title': 'TimeTracker AI',
                'content': 'Smart time tracking tool that automatically categorizes your work activities',
                'tagline': 'AI-powered time tracking',
                'comments': ['Great tool but needs better reporting', 'Wish it had mobile app', 'Too expensive for solo freelancers'],
                'url': 'https://producthunt.com/timetracker-ai',
                'votes': 89,
                'comments_count': 12,
                'created_at': '2024-01-02T00:00:00Z',
                'timestamp': datetime.now().isoformat(),
                'tags': ['time tracking', 'ai', 'productivity']
            },
            {
                'source': 'producthunt',
                'title': 'DataSync Hub',
                'content': 'Automated data synchronization between different business tools and databases',
                'tagline': 'Sync your data seamlessly',
                'comments': ['Finally! I needed this for my business', 'Integration with Salesforce would be great', 'Pricing is reasonable'],
                'url': 'https://producthunt.com/datasync-hub',
                'votes': 203,
                'comments_count': 18,
                'created_at': '2024-01-03T00:00:00Z',
                'timestamp': datetime.now().isoformat(),
                'tags': ['data', 'automation', 'integration']
            },
            {
                'source': 'producthunt',
                'title': 'EmailCraft',
                'content': 'AI-powered email writing assistant that helps create professional emails',
                'tagline': 'Write better emails with AI',
                'comments': ['This saves me so much time', 'Wish it had more templates', 'Great for cold outreach'],
                'url': 'https://producthunt.com/emailcraft',
                'votes': 167,
                'comments_count': 31,
                'created_at': '2024-01-04T00:00:00Z',
                'timestamp': datetime.now().isoformat(),
                'tags': ['email', 'ai', 'writing']
            },
            {
                'source': 'producthunt',
                'title': 'InvoiceGenie',
                'content': 'Automated invoice generation and payment tracking for freelancers',
                'tagline': 'Automate your invoicing',
                'comments': ['Perfect for my freelance business', 'Needs better payment integration', 'Love the automation features'],
                'url': 'https://producthunt.com/invoicegenie',
                'votes': 134,
                'comments_count': 22,
                'created_at': '2024-01-05T00:00:00Z',
                'timestamp': datetime.now().isoformat(),
                'tags': ['invoicing', 'freelance', 'automation']
            }
        ]
        return mock_products
    
    def harvest_problems(self, max_items: int = 50) -> List[Dict[str, Any]]:
        """Harvest problem statements from Product Hunt"""
        all_results = []
        
        # Search for products with problem-related keywords
        problem_queries = [
            'automation tool',
            'productivity app',
            'time tracking',
            'workflow management',
            'integration platform',
            'data analysis',
            'marketing automation',
            'customer support',
            'project management',
            'team collaboration'
        ]
        
        for query in problem_queries:
            if len(all_results) >= max_items:
                break
            
            results = self.search_products(query, limit=5)
            all_results.extend(results)
            time.sleep(1)  # Rate limiting
        
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
            'saas', 'startup', 'business', 'developer', 'marketing', 'analytics'
        ]
        
        for indicator in problem_indicators:
            if indicator in text_lower:
                tags.append(indicator)
        
        return list(set(tags))
    
    def save_results(self, filename: str = 'producthunt_data.json'):
        """Save results to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
