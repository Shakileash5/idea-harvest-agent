#!/usr/bin/env python3

import json
import os
from scrapers.reddit_scraper import RedditScraper

def load_existing_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []

def main():
    print("Starting combined harvest...")
    
    hn_data = load_existing_data('hackernews_data.json')
    ph_data = load_existing_data('producthunt_data.json')
    
    print("Loaded " + str(len(hn_data)) + " HN items, " + str(len(ph_data)) + " PH items")
    
    print("Harvesting Reddit with comments...")
    reddit_scraper = RedditScraper()
    reddit_data = reddit_scraper.harvest_problems(max_items=30)
    
    all_data = hn_data + ph_data + reddit_data
    
    with open('combined_harvest_data.json', 'w') as f:
        json.dump(all_data, f, indent=2)
    
    print("Combined harvest complete:")
    print("   - HackerNews: " + str(len(hn_data)) + " items")
    print("   - ProductHunt: " + str(len(ph_data)) + " items") 
    print("   - Reddit (with comments): " + str(len(reddit_data)) + " items")
    print("   - Total: " + str(len(all_data)) + " items")
    print("Saved to: combined_harvest_data.json")

if __name__ == "__main__":
    main()