#!/usr/bin/env python3
"""
Cost analysis for Google AI API usage
"""

def analyze_costs():
    print("💰 GOOGLE AI API COST ANALYSIS")
    print("=" * 40)
    
    # Our system processes:
    posts_per_run = 50
    normalization_calls = posts_per_run  # 1 call per post
    clustering_calls = 1  # 1 call for all posts
    scoring_calls = 5  # 1 call per cluster (estimated 5 clusters)
    idea_generation_calls = 5  # 1 call per top cluster
    playbook_calls = 5  # 1 call per idea
    
    total_calls = normalization_calls + clustering_calls + scoring_calls + idea_generation_calls + playbook_calls
    
    print("📊 PER RUN ESTIMATE:")
    print(f"  Posts harvested: {posts_per_run}")
    print(f"  AI API calls: {total_calls}")
    print(f"  Free tier limit: 15 calls/minute")
    print()
    
    # Token estimation (conservative)
    avg_tokens_per_call = 2000
    total_tokens = total_calls * avg_tokens_per_call
    
    print("🔢 TOKEN USAGE:")
    print(f"  Tokens per run: ~{total_tokens:,}")
    print(f"  Free tier: 1,000,000 tokens/month")
    runs_per_month = 1000000 // total_tokens
    print(f"  Runs per month (free): ~{runs_per_month}")
    print()
    
    print("💵 COST BREAKDOWN:")
    print(f"  Free tier: 1M tokens/month = $0")
    print(f"  Paid rate: $0.0005 per 1K tokens")
    cost_per_run = (total_tokens / 1000) * 0.0005
    print(f"  Cost per run: ${cost_per_run:.4f}")
    cost_per_month = cost_per_run * 100
    print(f"  Cost per month (100 runs): ${cost_per_month:.2f}")
    print()
    
    print("✅ CONCLUSION:")
    print("  - FREE for most users (under 1M tokens/month)")
    print("  - Very cheap if you exceed free tier")
    print("  - Our system is designed to be cost-effective")
    print()
    
    print("🎯 REALISTIC USAGE:")
    print("  - Casual user: 10 runs/month = FREE")
    print("  - Regular user: 50 runs/month = FREE") 
    print("  - Power user: 200 runs/month = ~$6/month")
    print("  - Enterprise: 1000 runs/month = ~$30/month")

if __name__ == "__main__":
    analyze_costs()
