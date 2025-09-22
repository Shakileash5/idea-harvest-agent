#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Idea Harvest Agent
Tests the system with mock data when API keys are not available
"""

import json
import os
from datetime import datetime
from main import IdeaHarvestAgent

def test_with_mock_data():
    """Test the system with mock data"""
    print("🧪 Testing Idea Harvest Agent with mock data...")
    
    # Create mock data
    mock_data = [
        {
            'source': 'reddit',
            'subreddit': 'Entrepreneur',
            'title': 'I wish there was a tool to automate my social media posting',
            'content': 'I spend hours every week manually posting to Instagram, Twitter, and LinkedIn. There has to be a better way!',
            'comments': ['I use Buffer but it\'s expensive', 'Try Hootsuite', 'I need something simpler'],
            'url': 'https://reddit.com/mock1',
            'score': 15,
            'created_utc': 1640995200,
            'timestamp': datetime.now().isoformat(),
            'tags': ['automation', 'social media', 'productivity']
        },
        {
            'source': 'hackernews',
            'title': 'Looking for a simple tool to track my expenses',
            'content': 'I\'m a freelancer and need to track expenses for tax purposes. Current tools are too complex.',
            'comments': ['Try Mint', 'YNAB is good but expensive', 'I built my own spreadsheet'],
            'url': 'https://news.ycombinator.com/mock1',
            'score': 8,
            'created_utc': 1640995200,
            'timestamp': datetime.now().isoformat(),
            'tags': ['expenses', 'tracking', 'freelancer']
        },
        {
            'source': 'producthunt',
            'title': 'TimeTracker Pro',
            'content': 'A simple time tracking tool for freelancers',
            'tagline': 'Track time, bill clients, get paid',
            'comments': ['Great tool but needs better reporting', 'Wish it had mobile app', 'Too expensive for solo freelancers'],
            'url': 'https://producthunt.com/mock1',
            'votes': 45,
            'comments_count': 12,
            'created_at': '2024-01-01T00:00:00Z',
            'timestamp': datetime.now().isoformat(),
            'tags': ['time tracking', 'freelancer', 'billing']
        }
    ]
    
    # Initialize agent
    agent = IdeaHarvestAgent()
    agent.results['raw_data'] = mock_data
    
    print("✅ Mock data created")
    
    # Test processing
    print("🔄 Testing problem processing...")
    try:
        clusters = agent.process_problems()
        print(f"✅ Processing completed: {len(clusters)} clusters found")
    except Exception as e:
        print(f"❌ Processing failed: {e}")
        return False
    
    # Test idea generation
    print("💡 Testing idea generation...")
    try:
        ideas = agent.generate_ideas()
        print(f"✅ Ideas generated: {len(ideas)} ideas created")
    except Exception as e:
        print(f"❌ Idea generation failed: {e}")
        return False
    
    # Test validation playbooks
    print("📋 Testing validation playbooks...")
    try:
        playbooks = agent.create_validation_playbooks()
        print(f"✅ Playbooks created: {len(playbooks)} playbooks generated")
    except Exception as e:
        print(f"❌ Playbook creation failed: {e}")
        return False
    
    # Test file output
    print("💾 Testing file output...")
    try:
        json_file = agent.save_results('test_results.json')
        md_file = agent.generate_markdown_report('test_report.md')
        print(f"✅ Files saved: {json_file}, {md_file}")
    except Exception as e:
        print(f"❌ File output failed: {e}")
        return False
    
    # Display results summary
    print("\n" + "="*50)
    print("📊 TEST RESULTS SUMMARY")
    print("="*50)
    print(f"Raw data items: {len(agent.results.get('raw_data', []))}")
    print(f"Normalized problems: {len(agent.results.get('normalized_problems', []))}")
    print(f"Clusters: {len(agent.results.get('clusters', []))}")
    print(f"Scored clusters: {len(agent.results.get('scored_clusters', []))}")
    print(f"Top ideas: {len(agent.results.get('top_ideas', []))}")
    print(f"Validation playbooks: {len(agent.results.get('validation_playbooks', {}))}")
    
    # Show sample idea
    if agent.results.get('top_ideas'):
        print("\n🎯 SAMPLE IDEA:")
        idea = agent.results['top_ideas'][0]
        print(f"Name: {idea.get('ideaName', 'N/A')}")
        print(f"Description: {idea.get('description', 'N/A')}")
        print(f"Target: {idea.get('targetPersona', 'N/A')}")
        print(f"Pricing: {idea.get('monetization', 'N/A')}")
    
    print("\n✅ All tests passed!")
    return True

def main():
    """Main test function"""
    print("🚀 Idea Harvest Agent - System Test")
    print("="*50)
    
    # Check if API keys are available
    has_reddit = os.getenv('REDDIT_CLIENT_ID') and os.getenv('REDDIT_CLIENT_SECRET')
    has_google = os.getenv('GOOGLE_AI_API_KEY')
    
    print(f"Reddit API: {'✅ Available' if has_reddit else '❌ Not configured'}")
    print(f"Google AI API: {'✅ Available' if has_google else '❌ Not configured'}")
    
    if not has_reddit or not has_google:
        print("\n⚠️  API keys not configured, running with mock data...")
    
    # Run tests
    success = test_with_mock_data()
    
    if success:
        print("\n🎉 System test completed successfully!")
        print("\nNext steps:")
        print("1. Configure API keys in .env file")
        print("2. Run: python main.py")
        print("3. Or run: python web_interface.py")
    else:
        print("\n❌ System test failed!")
        print("Check the error messages above and fix any issues.")

if __name__ == "__main__":
    main()
