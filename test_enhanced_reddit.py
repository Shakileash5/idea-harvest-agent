#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for enhanced Reddit scraper with exponential retry
"""

import logging
import time
from scrapers.reddit_scraper import RedditScraper

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_enhanced_scraper():
    """Test the enhanced Reddit scraper"""
    print("Testing Enhanced Reddit Scraper")
    print("=" * 50)
    
    # Initialize scraper
    scraper = RedditScraper()
    
    # Test small harvest first
    print("\nTesting small harvest (50 items)...")
    start_time = time.time()
    
    results = scraper.harvest_problems(max_items=50)
    
    harvest_time = time.time() - start_time
    
    print("\nHarvest Results:")
    print("   Items collected: {}".format(len(results)))
    print("   Time taken: {:.2f}s".format(harvest_time))
    if harvest_time > 0:
        print("   Rate: {:.2f} items/second".format(len(results) / harvest_time))
    
    # Show sample results
    if results:
        print("\nSample Results:")
        for i, result in enumerate(results[:3], 1):
            print("   {}. r/{}: {}...".format(i, result['subreddit'], result['title'][:60]))
            print("      Score: {}, Comments: {}".format(result['score'], len(result['comments'])))
    
    # Save results
    scraper.save_results('test_enhanced_reddit.json')
    print("\nResults saved to test_enhanced_reddit.json")
    
    return len(results) > 0

if __name__ == "__main__":
    success = test_enhanced_scraper()
    if success:
        print("\nEnhanced scraper test PASSED!")
    else:
        print("\nEnhanced scraper test FAILED!")
