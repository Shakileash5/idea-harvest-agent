#!/usr/bin/env python3

from scrapers.reddit_scraper import RedditScraper

def main():
    scraper = RedditScraper()
    results = scraper.harvest_problems(max_items=150)
    scraper.save_results('reddit_with_comments.json')
    print(f'Harvested {len(results)} posts with comments')

if __name__ == "__main__":
    main()