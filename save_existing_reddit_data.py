#!/usr/bin/env python3

import json
from datetime import datetime

# Real Reddit data from your successful API calls (from the log)
real_reddit_data = [
    {
        'source': 'reddit',
        'subreddit': 'Entrepreneur',
        'title': 'Sorry everyone, because of my fatal mistakes, Comick was taken down.',
        'content': 'I built Comick in early 2021, because anime and manga have always been my main favorites. Firstly, I saw that almost all manga sites were slow and out of date -> I think I can do better than them ( also I was naive and think I could even purchase licenses if Comick grew enough, like Crunchyroll lol). Then, when Comick became popular in 2023, my dream focused on developing Comick to become the best manga site in the world, dominating all other sites. With the timer, I could help scanlator groups, and everyone wouldn't have to deal with bad ads if Comick completely dominated. But my fatal flaw was that I didn't think publishers would target manga sites without licenses so aggressively from the beginning and I was too focused on features for Comick and forgot other things , and I dunno almost all CDN Cloudflare and domain providers gave my information so easily. Publishers got my real information before I understood that these things were serious.',
        'comments': [],
        'url': 'https://reddit.com/r/ComicK/comments/1nkbg1g/sorry_everyone_because_of_my_fatal_mistakes/',
        'score': 17844,
        'created_utc': 1758209429,
        'timestamp': datetime.fromtimestamp(1758209429).isoformat(),
        'tags': ['startup failure', 'legal issues', 'business lessons', 'manga', 'licensing']
    },
    {
        'source': 'reddit',
        'subreddit': 'startups',
        'title': 'AITA for reporting my ex and her husband to the police for stealing my property?',
        'content': 'My ex-wife (39f) and I (41m) share custody of our three children (16, 14 and 12) equally and no child support is paid. Our marriage didn\'t end on the best of terms and we communicate through an app only when required to for the sake of the kids. She has since remarried and has a 15 year old stepchild and a 13 year old stepchild. Her husband and I do not speak also. We\'ve had some issues with my ex keeping property that is mine if the kids have it on her time. It started with a cell phone. I gave our eldest my old phone when one of ex\'s stepkids broke his phone. My ex then told our oldest they were keeping it at her house and she refused to return it even when I went over there and asked.',
        'comments': [],
        'url': 'https://reddit.com/r/AITAH/comments/1naqszd/aita_for_reporting_my_ex_and_her_husband_to_the/',
        'score': 10338,
        'created_utc': 1757244601,
        'timestamp': datetime.fromtimestamp(1757244601).isoformat(),
        'tags': ['legal', 'family', 'property', 'communication']
    },
    {
        'source': 'reddit',
        'subreddit': 'antiwork',
        'title': 'America Is Crying and the Leaders Don't Care',
        'content': 'I see it every day. Kids going to bed with empty stomachs. Parents breaking down in their cars because they gave everything and it still was not enough. Veterans wandering streets they once swore to protect, left to rot. Teachers buying supplies with money they do not have. And the homeless, entire families living in tents under bridges, children sleeping on concrete, people huddled in doorways just to survive, treated like trash while politicians like Biden, McConnell, Schumer, Trump, Pelosi and the rest argue on TV, cash checks, and pretend this is progress.',
        'comments': [],
        'url': 'https://reddit.com/r/antiwork/comments/1n7cwri/america_is_crying_and_the_leaders_dont_care/',
        'score': 7578,
        'created_utc': 1756900989,
        'timestamp': datetime.fromtimestamp(1756900989).isoformat(),
        'tags': ['social issues', 'politics', 'inequality', 'activism']
    },
    {
        'source': 'reddit',
        'subreddit': 'gaming',
        'title': 'Hollow Knight: Silksong devs address difficulty concerns: "You have choices"',
        'content': 'Game Worlds co-curator Jini Maxwell spoke with Team Cherry's Ari Gibson and William Pellen, with difficulty being a major focus of the conversation. Admitting Silksong is indeed far more complicated than the original title, Gibson explained how it's all designed to give players choices. "The important thing for us is that we allow you to go way off the path. So one player may choose to follow it directly to its conclusion, and then another may choose to constantly divert from it and find all the other things that are waiting and all the other ways and routes."',
        'comments': [],
        'url': 'https://reddit.com/r/gaming/comments/1nkdh1m/hollow_knight_silksong_devs_address_difficulty/',
        'score': 6662,
        'created_utc': 1758213937,
        'timestamp': datetime.fromtimestamp(1758213937).isoformat(),
        'tags': ['gaming', 'game development', 'difficulty', 'player choice']
    }
]

def save_real_data():
    """Save the real Reddit data that was successfully retrieved"""
    
    # Save real data
    with open('reddit_real_data.json', 'w', encoding='utf-8') as f:
        json.dump(real_reddit_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved {len(real_reddit_data)} real Reddit posts to reddit_real_data.json")
    
    # Load mock data
    try:
        with open('reddit_comprehensive_mock_data.json', 'r', encoding='utf-8') as f:
            mock_data = json.load(f)
        print(f"📊 Loaded {len(mock_data)} mock posts")
    except FileNotFoundError:
        print("❌ Mock data file not found")
        return
    
    # Combine real and mock data
    combined_data = real_reddit_data + mock_data
    
    # Save combined dataset
    with open('reddit_combined_data.json', 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, indent=2, ensure_ascii=False)
    
    print(f"🎯 Created combined dataset with {len(combined_data)} total posts")
    print(f"   - {len(real_reddit_data)} real posts from successful API calls")
    print(f"   - {len(mock_data)} mock posts using SEARCH_QUERIES")
    
    # Generate summary
    subreddits = {}
    for item in combined_data:
        subreddit = item.get('subreddit', 'unknown')
        subreddits[subreddit] = subreddits.get(subreddit, 0) + 1
    
    print(f"📊 Subreddit distribution:")
    for subreddit, count in sorted(subreddits.items(), key=lambda x: x[1], reverse=True)[:15]:
        print(f"   r/{subreddit}: {count} posts")
    
    file_size = len(json.dumps(combined_data, indent=2))
    print(f"💾 Combined dataset: {file_size:,} bytes")
    print(f"🚀 Ready for comprehensive idea harvesting!")

if __name__ == "__main__":
    save_real_data()