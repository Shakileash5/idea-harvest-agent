#!/usr/bin/env python3

import json
import os
from datetime import datetime

def extract_source_data():
    """Extract data from web interface results and save to individual files"""
    
    # Check if we have any results files
    result_files = [f for f in os.listdir('.') if f.startswith('idea_harvest_results_')]
    
    if not result_files:
        print("❌ No harvest results found. Run the web interface harvest first.")
        return
    
    # Use the most recent results file
    latest_file = sorted(result_files)[-1]
    print(f"📂 Reading from {latest_file}")
    
    with open(latest_file, 'r') as f:
        data = json.load(f)
    
    raw_data = data.get('raw_data', [])
    if not raw_data:
        print("❌ No raw data found in results")
        return
    
    # Separate by source
    sources = {}
    for item in raw_data:
        source = item.get('source', 'unknown')
        if source not in sources:
            sources[source] = []
        sources[source].append(item)
    
    # Save individual files
    for source, items in sources.items():
        filename = f"{source}_data.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(items, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved {len(items)} items to {filename}")
    
    print(f"\n✅ Extracted data from {len(sources)} sources")
    return sources

if __name__ == "__main__":
    extract_source_data()