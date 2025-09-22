import os
from dotenv import load_dotenv

load_dotenv()

# Reddit API Configuration
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'idea-harvest-agent/1.0')

# Google AI Configuration
GOOGLE_AI_API_KEY = os.getenv('GOOGLE_AI_API_KEY')

# SerpAPI Configuration (optional)
SERPAPI_KEY = os.getenv('SERPAPI_KEY')

# Product Hunt API Configuration
PRODUCTHUNT_API_KEY = os.getenv('PRODUCTHUNT_API_KEY')
PRODUCTHUNT_API_SECRET = os.getenv('PRODUCTHUNT_API_SECRET')
PRODUCTHUNT_REDIRECT_URI = os.getenv('PRODUCTHUNT_REDIRECT_URI', 'https://localhost:8080')

# Search Configuration
SEARCH_QUERIES = [
    "I wish there was a tool to",
    "Is there a tool for",
    "How do you automate",
    "Anyone recommend a tool for",
    "Looking for a solution to",
    "Feature request:",
    "Please add",
    "Too expensive",
    "alternatives to",
    "I need a tool to",
    "anyone built",
    "wish there was a tool"
]

# Target Subreddits
SUBREDDITS = [
    'Entrepreneur', 'startups', 'SaaS', 'SideProject', 'IndieHackers', 
    'SmallBusiness', 'webdev', 'reactjs', 'vuejs', 'androiddev', 
    'iOSProgramming', 'programming', 'YouTubers', 'Blogging', 'Instagram', 
    'ContentCreators', 'ecommerce', 'shopify', 'FulfillmentByAmazon', 
    'freelance', 'DesignJobs', 'accounting', 'sysadmin', 'Excel'
]

# Output Configuration
MAX_ITEMS_PER_SOURCE = 500  # Increased for large harvests
TOTAL_TARGET_ITEMS = 2000   # Increased target
