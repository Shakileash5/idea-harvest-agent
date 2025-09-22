#!/usr/bin/env python3

import logging
import sys
from main import IdeaHarvestAgent

# Set up detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('harvest_debug.log')
    ]
)

def test_harvest_with_logs():
    """Test the harvest with comprehensive logging"""
    logging.info("🚀 Starting test harvest with full logging")
    
    try:
        agent = IdeaHarvestAgent()
        
        # Test just the harvest step first
        logging.info("📡 Testing harvest step only...")
        harvest_summary = agent.harvest_all_sources()
        
        logging.info("✅ Harvest test completed")
        logging.info(f"📊 Summary: {harvest_summary}")
        
        # Save just the raw data for inspection
        agent.save_results('test_harvest_raw.json')
        
        return True
        
    except Exception as e:
        logging.error(f"❌ Test failed: {e}")
        import traceback
        logging.error(f"📋 Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = test_harvest_with_logs()
    if success:
        print("\n✅ Test completed successfully! Check harvest_debug.log for details.")
    else:
        print("\n❌ Test failed! Check harvest_debug.log for details.")