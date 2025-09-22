#!/usr/bin/env python3

import json
from datetime import datetime
from main import IdeaHarvestAgent

def cluster_and_save():
    agent = IdeaHarvestAgent()
    
    # Load existing raw data if available
    try:
        with open('reddit_data.json', 'r') as f:
            reddit_data = json.load(f)
        with open('hackernews_data.json', 'r') as f:
            hn_data = json.load(f)
        with open('producthunt_data.json', 'r') as f:
            ph_data = json.load(f)
        
        all_data = reddit_data + hn_data + ph_data
        agent.results['raw_data'] = all_data
        print("Loaded {} existing problems".format(len(all_data)))
        
    except FileNotFoundError:
        print("No existing data found, harvesting fresh...")
        agent.harvest_all_sources()
    
    # Process and cluster
    agent.process_problems()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file = "clusters_output_{}.json".format(timestamp)
    md_file = "clusters_report_{}.md".format(timestamp)
    
    with open(json_file, 'w') as f:
        json.dump({
            'clusters': agent.results['clusters'],
            'scored_clusters': agent.results['scored_clusters'],
            'normalized_problems': agent.results['normalized_problems']
        }, f, indent=2)
    
    agent.generate_markdown_report(md_file)
    
    print("Clusters saved to: {}".format(json_file))
    print("Report saved to: {}".format(md_file))

if __name__ == "__main__":
    cluster_and_save()