#!/usr/bin/env python3

from scrapers.reddit_scraper import RedditScraper

def main():
    print("🚀 Running Reddit Scraper")
    print("=" * 30)
    
    scraper = RedditScraper()
    results = scraper.harvest_problems(max_items=20)
    
    print(f"\n✅ Found {len(results)} posts")
    
    # Show sample results
    for i, post in enumerate(results[:3], 1):
        print(f"{i}. r/{post['subreddit']} - {post['title'][:50]}...")
        print(f"   Score: {post['score']}, Tags: {post['tags']}")
    
    scraper.save_results('reddit_data.json')

if __name__ == "__main__":
    main()