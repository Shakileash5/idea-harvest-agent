#!/usr/bin/env python3

import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_processor_ollama import OllamaAIProcessor
from datetime import datetime

def load_data():
    all_data = []
    files = ['reddit_data.json', 'hackernews_data.json', 'producthunt_data.json']
    
    for file in files:
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                all_data.extend(data)
                print("Loaded {} items from {}".format(len(data), file))
        except FileNotFoundError:
            print("File not found: {}".format(file))
    
    return all_data

def main():
    # Load data
    raw_data = load_data()
    if not raw_data:
        print("No data found to cluster")
        return
    
    print("Total items to process: {}".format(len(raw_data)))
    
    # Initialize AI processor
    processor = OllamaAIProcessor()
    
    # Normalize problems
    print("Normalizing problems...")
    normalized = processor.normalize_problems(raw_data)
    
    # Cluster problems
    print("Clustering problems...")
    clusters = processor.cluster_problems(normalized)
    
    # Score clusters
    print("Scoring clusters...")
    scored_clusters = processor.score_clusters(clusters, normalized)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = "cluster_results_{}.json".format(timestamp)
    
    results = {
        'normalized_problems': normalized,
        'clusters': clusters,
        'scored_clusters': scored_clusters,
        'summary': {
            'total_raw': len(raw_data),
            'normalized': len(normalized),
            'clusters_found': len(clusters),
            'scored_clusters': len(scored_clusters)
        }
    }
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("Results saved to: {}".format(output_file))
    print("Summary:")
    print("- Raw problems: {}".format(len(raw_data)))
    print("- Normalized: {}".format(len(normalized)))
    print("- Clusters: {}".format(len(clusters)))

if __name__ == "__main__":
    main()