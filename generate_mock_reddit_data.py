#!/usr/bin/env python3

import json
import random
import time
from datetime import datetime, timedelta

# Search queries for finding problem statements
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

def generate_comprehensive_mock_data(max_items: int = 500) -> list:
    """Generate comprehensive mock Reddit data using SEARCH_QUERIES"""
    
    # Problem templates based on SEARCH_QUERIES with realistic scenarios
    problem_scenarios = {
        "I wish there was a tool to": [
            "automate social media posting across all platforms without losing engagement",
            "track time spent on projects without being invasive to team members", 
            "manage customer support tickets that actually learns from responses",
            "sync data between Shopify, QuickBooks, and my CRM automatically",
            "create professional invoices that clients actually want to pay quickly",
            "schedule meetings across different time zones without the back-and-forth",
            "backup all my business files to multiple clouds with one click",
            "monitor my website uptime and automatically fix common issues",
            "convert PDFs to editable formats that don't mess up the formatting",
            "organize all my digital assets so I can actually find them later",
            "automate email follow-ups that don't sound like a robot wrote them",
            "manage inventory across multiple sales channels in real-time",
            "create landing pages without needing to code or hire developers",
            "analyze which social media posts actually drive sales",
            "track expenses for tax season without wanting to cry",
            "streamline the hiring process so I don't waste weeks on bad candidates"
        ],
        
        "Is there a tool for": [
            "managing freelance projects when you have 5+ clients going at once",
            "tracking employee productivity without being Big Brother about it", 
            "organizing customer feedback so you can actually act on it",
            "simplifying accounting for people who hate numbers",
            "creating professional presentations in under 10 minutes",
            "managing multiple Etsy/Amazon/eBay stores from one dashboard",
            "automating repetitive tasks in Google Sheets or Excel",
            "scheduling social media that doesn't post at 3am by accident",
            "managing a team when everyone works different hours",
            "tracking which marketing campaigns actually make money",
            "organizing digital receipts for business expenses",
            "creating email newsletters that people actually open",
            "managing client communications without losing important messages",
            "automating data entry between different business systems",
            "creating simple websites that don't require a CS degree",
            "tracking project profitability in real-time"
        ],
        
        "Looking for a solution to": [
            "reduce the 3 hours I spend daily on manual data entry",
            "improve team communication when everyone's remote",
            "streamline our hiring process - it's taking forever to find good people",
            "manage multiple client projects without dropping the ball",
            "automate the repetitive tasks that are killing my productivity",
            "track what my team is working on without micromanaging",
            "organize customer feedback so we can prioritize feature requests",
            "simplify our accounting - QuickBooks is overkill and confusing",
            "manage our social media without posting the same thing everywhere",
            "track which marketing efforts actually bring in customers",
            "organize all our business documents in one searchable place",
            "automate follow-up emails for leads that go cold",
            "manage inventory across our online and physical stores",
            "create professional proposals without starting from scratch each time",
            "track project time and costs so we know if we're profitable",
            "streamline customer onboarding - it's currently a mess"
        ],
        
        "Too expensive": [
            "Salesforce is $150/month per user - way too much for our 3-person team",
            "Adobe Creative Suite costs $600/year and I only use Photoshop occasionally", 
            "Slack's premium features are $8/user/month but we only need file sharing",
            "Zoom Pro is $15/month but we only have 2-3 meetings per week",
            "Mailchimp jumps to $30/month after 2000 contacts - huge price jump",
            "Asana premium is $11/user/month for features that should be basic",
            "Shopify's transaction fees add up to hundreds per month",
            "QuickBooks is $50/month for features I don't understand or need",
            "HubSpot CRM starts at $50/month but their free version is too limited",
            "Canva Pro is $15/month just to remove backgrounds from images",
            "Buffer costs $15/month per social account - adds up fast",
            "Calendly premium is $10/month for basic scheduling features",
            "Dropbox Business is $20/month when Google Drive is much cheaper",
            "Hootsuite is $50/month for social media scheduling we barely use",
            "FreshBooks is $30/month for invoicing that should be simpler",
            "Zendesk starts at $55/month for customer support we're not ready for"
        ],
        
        "alternatives to": [
            "Photoshop for basic image editing - don't need all the advanced features",
            "Excel for project management - spreadsheets aren't cutting it anymore",
            "Google Analytics - too complex, just want simple visitor stats",
            "Calendly for appointment scheduling - their free plan is too limited", 
            "Dropbox for file sharing - need something more affordable",
            "Trello for task management - need more features but Asana is expensive",
            "WordPress for simple business websites - too complicated to maintain",
            "Zoom for small team meetings - don't need all the enterprise features",
            "Mailchimp for email newsletters - pricing gets crazy after 2000 subscribers",
            "Slack for team communication - free version is too limited",
            "QuickBooks for simple invoicing - way more complex than we need",
            "Shopify for small online stores - transaction fees are killing us",
            "HubSpot for basic CRM - their free version missing key features",
            "Canva for social media graphics - premium features should be cheaper",
            "Buffer for social media scheduling - need something more affordable",
            "Zendesk for customer support - overkill for our small business"
        ],
        
        "Anyone recommend a tool for": [
            "managing client projects when you're a solo freelancer",
            "tracking business expenses without manually entering every receipt",
            "creating professional invoices that get paid faster",
            "scheduling social media posts across multiple platforms",
            "managing email lists without breaking the bank",
            "organizing digital files so you can actually find them",
            "automating repetitive tasks in your daily workflow",
            "tracking time spent on different projects accurately",
            "creating simple websites without learning to code",
            "managing customer relationships for a small business",
            "organizing team tasks when everyone works remotely",
            "creating professional graphics without design skills",
            "managing inventory for an online store",
            "automating email follow-ups for potential clients",
            "tracking which marketing efforts actually work",
            "simplifying bookkeeping for tax season"
        ],
        
        "How do you automate": [
            "social media posting without losing the personal touch",
            "data entry between different business systems",
            "email follow-ups for leads that don't respond",
            "invoice creation and sending for recurring clients", 
            "expense tracking from receipts and bank statements",
            "customer onboarding without losing the human element",
            "inventory updates across multiple sales channels",
            "appointment scheduling and confirmation emails",
            "social media engagement and response to comments",
            "lead qualification before they get to sales calls",
            "project status updates to keep clients informed",
            "time tracking without constantly watching the clock",
            "file organization and backup processes",
            "customer support for common questions",
            "marketing campaign performance tracking",
            "team task assignment and progress monitoring"
        ]
    }
    
    # Business pain points and contexts
    business_contexts = [
        "As a freelance designer with 8 clients",
        "Running a small e-commerce store with my partner", 
        "Managing a 5-person remote marketing agency",
        "Solo consultant trying to scale my business",
        "Small restaurant owner dealing with online orders",
        "Etsy shop owner with 500+ products",
        "Local service business with 3 employees",
        "SaaS startup with limited budget",
        "Content creator managing multiple platforms",
        "Small accounting firm with 50+ clients",
        "Online course creator with growing audience",
        "Dropshipping business owner",
        "Local gym owner managing memberships",
        "Wedding photographer booking 20+ events/year",
        "Small law firm handling client communications",
        "Real estate agent managing multiple listings"
    ]
    
    # Realistic pricing complaints and alternatives mentioned
    pricing_contexts = [
        "Currently paying $200/month for tools that barely work together",
        "Spending 10+ hours/week on tasks that should be automated",
        "Using 5 different tools when one integrated solution would be better",
        "Free versions are too limited, paid versions are too expensive",
        "Enterprise pricing for features that small businesses need too",
        "Monthly costs adding up to more than we spend on rent",
        "Tried the free trial but can't justify the ongoing cost",
        "Works great but pricing scales too aggressively",
        "Perfect features but way outside our budget",
        "Good tool but nickel-and-dimes you for basic features"
    ]
    
    mock_results = []
    
    for query_type, problems in problem_scenarios.items():
        for problem in problems:
            if len(mock_results) >= max_items:
                break
                
            # Select random subreddit and context
            subreddit = random.choice(SUBREDDITS)
            context = random.choice(business_contexts)
            
            # Create realistic post based on query type
            if "expensive" in query_type.lower():
                title = f"{problem} - looking for cheaper alternatives"
                content = f"{context}, currently using {problem.split(' ')[0]} but {random.choice(pricing_contexts)}. Need something more affordable that actually works for small businesses. Budget is tight but this is essential for our workflow."
                tags = ['expensive', 'alternative', 'budget', 'small business']
                
            elif "tool" in query_type.lower():
                title = f"{query_type} {problem}"
                content = f"{context}. I've been doing {problem} manually and it's taking way too much time. There has to be a better way to handle this. Current process is inefficient and error-prone. Any recommendations?"
                tags = ['automation', 'productivity', 'tool', 'efficiency']
                
            elif "automate" in query_type.lower():
                title = f"How do you automate {problem}?"
                content = f"{context}. Currently spending hours each week on {problem}. Looking for ways to automate this process without losing quality or personal touch. What tools or methods have worked for you?"
                tags = ['automation', 'workflow', 'efficiency', 'scaling']
                
            else:
                title = f"{query_type} {problem}"
                content = f"{context}. Has anyone found a good solution for {problem}? Current methods aren't working well and it's becoming a bottleneck. Open to paid solutions if they're reasonably priced."
                tags = ['solution', 'help', 'recommendation', 'business']
            
            # Add realistic engagement metrics
            score = random.randint(5, 150)
            comments_count = random.randint(3, 45)
            created_days_ago = random.randint(1, 30)
            created_time = datetime.now() - timedelta(days=created_days_ago)
            
            mock_results.append({
                'source': 'reddit',
                'subreddit': subreddit,
                'title': title,
                'content': content,
                'comments': [],  # Skip comments for now to focus on volume
                'url': f'https://reddit.com/r/{subreddit}/generated{len(mock_results)+1}',
                'score': score,
                'created_utc': int(created_time.timestamp()),
                'timestamp': created_time.isoformat(),
                'tags': tags,
                'num_comments': comments_count,
                'query_type': query_type,
                'business_context': context
            })
    
    return mock_results[:max_items]

def save_mock_data(filename: str = 'reddit_comprehensive_mock_data.json', max_items: int = 500):
    """Generate and save comprehensive mock data"""
    print(f"🤖 Generating {max_items} comprehensive mock Reddit posts using SEARCH_QUERIES...")
    
    mock_data = generate_comprehensive_mock_data(max_items)
    
    # Save to JSON file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(mock_data, f, indent=2, ensure_ascii=False)
    
    # Generate summary
    query_types = {}
    subreddits = {}
    
    for item in mock_data:
        query_type = item.get('query_type', 'unknown')
        subreddit = item.get('subreddit', 'unknown')
        
        query_types[query_type] = query_types.get(query_type, 0) + 1
        subreddits[subreddit] = subreddits.get(subreddit, 0) + 1
    
    print(f"✅ Generated {len(mock_data)} mock posts")
    print(f"📊 Query type distribution:")
    for query_type, count in sorted(query_types.items(), key=lambda x: x[1], reverse=True):
        print(f"   {query_type}: {count} posts")
    
    print(f"📊 Top subreddits:")
    for subreddit, count in sorted(subreddits.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   r/{subreddit}: {count} posts")
    
    file_size = len(json.dumps(mock_data, indent=2))
    print(f"💾 Saved to {filename} ({file_size:,} bytes)")
    
    return mock_data

if __name__ == "__main__":
    # Generate comprehensive mock data
    mock_data = save_mock_data('reddit_comprehensive_mock_data.json', 500)
    
    # Also save a smaller sample for testing
    sample_data = mock_data[:50]
    with open('reddit_sample_mock_data.json', 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, indent=2, ensure_ascii=False)
    
    print(f"📝 Also saved 50-item sample to reddit_sample_mock_data.json")
    print(f"🚀 Ready for idea harvesting!")