#!/usr/bin/env python3

import logging
import sys
import json
from main import IdeaHarvestAgent

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('ai_debug.log')
    ]
)

def test_ai_processing():
    """Test AI processing with a small dataset"""
    logging.info("🤖 Testing AI processing with small dataset")
    
    try:
        agent = IdeaHarvestAgent()
        
        # Load the harvested data
        with open('test_harvest_raw.json', 'r') as f:
            data = json.load(f)
        
        raw_data = data.get('raw_data', [])
        logging.info(f"📊 Loaded {len(raw_data)} items from harvest")
        
        # Test with just 3 items to start
        test_data = raw_data[:3]
        logging.info(f"🎯 Testing with {len(test_data)} items")
        
        agent.results['raw_data'] = test_data
        
        # Test normalization step
        logging.info("📝 Testing normalization...")
        normalized = agent.ai_processor.normalize_problems(test_data)
        logging.info(f"✅ Normalization result: {len(normalized)} items")
        
        if normalized:
            # Test clustering step
            logging.info("🔗 Testing clustering...")
            clusters = agent.ai_processor.cluster_problems(normalized)
            logging.info(f"✅ Clustering result: {len(clusters)} clusters")
            
            if clusters:
                # Test scoring step
                logging.info("📊 Testing scoring...")
                scored = agent.ai_processor.score_clusters(clusters, normalized)
                logging.info(f"✅ Scoring result: {len(scored)} scored clusters")
        
        return True
        
    except Exception as e:
        logging.error(f"❌ AI processing test failed: {e}")
        import traceback
        logging.error(f"📋 Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = test_ai_processing()
    if success:
        print("\n✅ AI processing test completed! Check ai_debug.log for details.")
    else:
        print("\n❌ AI processing test failed! Check ai_debug.log for details.")