#!/usr/bin/env python3
"""
Monitor large-scale Reddit harvesting with real-time stats
"""

import logging
import time
import json
from datetime import datetime
from scrapers.reddit_scraper import RedditScraper

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class HarvestMonitor:
    def __init__(self):
        self.start_time = None
        self.last_check = None
        self.total_items = 0
        self.rate_history = []
    
    def start_monitoring(self, target_items: int = 1000):
        """Start large-scale harvest with monitoring"""
        print(f"🚀 Starting Large-Scale Reddit Harvest")
        print(f"🎯 Target: {target_items} items")
        print("=" * 60)
        
        self.start_time = time.time()
        self.last_check = self.start_time
        
        # Initialize scraper
        scraper = RedditScraper()
        
        # Start harvest
        results = scraper.harvest_problems(max_items=target_items)
        
        # Final stats
        self._print_final_stats(results)
        
        # Save with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"large_harvest_{timestamp}.json"
        scraper.save_results(filename)
        
        return results
    
    def _print_final_stats(self, results):
        """Print final harvest statistics"""
        total_time = time.time() - self.start_time
        
        print(f"\n🎉 Harvest Complete!")
        print("=" * 60)
        print(f"📊 Final Statistics:")
        print(f"   Total Items: {len(results)}")
        print(f"   Total Time: {total_time:.2f}s ({total_time/60:.1f} minutes)")
        print(f"   Average Rate: {len(results) / total_time:.2f} items/second")
        
        # Subreddit breakdown
        subreddit_counts = {}
        for result in results:
            sub = result.get('subreddit', 'unknown')
            subreddit_counts[sub] = subreddit_counts.get(sub, 0) + 1
        
        print(f"\n📈 Top Subreddits:")
        for sub, count in sorted(subreddit_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"   r/{sub}: {count} items")
        
        # Quality metrics
        with_comments = sum(1 for r in results if r.get('comments'))
        high_score = sum(1 for r in results if r.get('score', 0) > 10)
        
        print(f"\n🏆 Quality Metrics:")
        print(f"   Items with comments: {with_comments} ({with_comments/len(results)*100:.1f}%)")
        print(f"   High-score items (>10): {high_score} ({high_score/len(results)*100:.1f}%)")

def main():
    """Main monitoring function"""
    monitor = HarvestMonitor()
    
    # Test different harvest sizes
    test_sizes = [100, 500, 1000]
    
    for size in test_sizes:
        print(f"\n🔄 Testing harvest size: {size}")
        try:
            results = monitor.start_monitoring(target_items=size)
            print(f"✅ Successfully harvested {len(results)} items")
            
            # Brief pause between tests
            if size < max(test_sizes):
                print("⏳ Waiting 30s before next test...")
                time.sleep(30)
                
        except KeyboardInterrupt:
            print("\n⏹️ Harvest interrupted by user")
            break
        except Exception as e:
            print(f"❌ Harvest failed: {e}")
            break

if __name__ == "__main__":
    main()
