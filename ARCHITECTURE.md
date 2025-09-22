# 🏗️ Idea Harvest Agent - Complete Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    IDEA HARVEST AGENT                          │
│                     (Main Orchestrator)                        │
└─────────────────────┬───────────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   REDDIT    │ │ HACKER NEWS │ │PRODUCT HUNT │
│   SCRAPER   │ │   SCRAPER   │ │   SCRAPER   │
│             │ │             │ │             │
│ • PRAW API  │ │ • Firebase  │ │ • GraphQL   │
│ • 25+ subs  │ │ • REST API  │ │ • OAuth2    │
│ • Real data │ │ • Real data │ │ • Real data │
└─────────────┘ └─────────────┘ └─────────────┘
        │             │             │
        └─────────────┼─────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RAW DATA STORAGE                            │
│                                                                 │
│ • reddit_data.json      (Reddit posts)                         │
│ • hackernews_data.json  (HN stories)                           │
│ • producthunt_data.json (PH products)                          │
│ • idea_harvest_results_*.json (Combined results)               │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                   OLLAMA AI PROCESSOR                          │
│                     (Local AI)                                 │
│                                                                 │
│ • Problem Normalization  (Raw → Structured)                    │
│ • Clustering            (Group similar problems)               │
│ • Scoring               (Rate opportunities)                   │
│ • Idea Generation       (Create product ideas)                 │
│ • Validation Playbooks  (Action plans)                         │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OUTPUT GENERATION                           │
│                                                                 │
│ • JSON Reports        (Machine-readable)                       │
│ • Markdown Reports    (Human-readable)                         │
│ • Web Interface       (Interactive dashboard)                  │
│ • Export Options      (Download results)                       │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
1. HARVEST PHASE
   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
   │   Reddit    │───▶│   Hacker    │───▶│  Product    │
   │   Posts     │    │   News      │    │   Hunt      │
   │             │    │   Stories   │    │  Products   │
   └─────────────┘    └─────────────┘    └─────────────┘
           │                   │                   │
           └───────────────────┼───────────────────┘
                               │
                               ▼
                    ┌─────────────────┐
                    │  Raw Data JSON  │
                    │  (95+ items)    │
                    └─────────────────┘

2. PROCESSING PHASE
   ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
   │   Normalize     │───▶│    Cluster      │───▶│     Score       │
   │   Problems      │    │   Problems      │    │  Opportunities  │
   └─────────────────┘    └─────────────────┘    └─────────────────┘
           │                       │                       │
           └───────────────────────┼───────────────────────┘
                                   │
                                   ▼
                    ┌─────────────────┐
                    │ Scored Clusters │
                    │  (Opportunities)│
                    └─────────────────┘

3. GENERATION PHASE
   ┌─────────────────┐    ┌─────────────────┐
   │  Generate Ideas │───▶│ Create Playbooks│
   │                 │    │                 │
   └─────────────────┘    └─────────────────┘
           │                       │
           └───────────────────────┘
                   │
                   ▼
        ┌─────────────────┐
        │ Final Results   │
        │ • Product Ideas │
        │ • Validation    │
        │ • Playbooks     │
        └─────────────────┘
```

## File Structure

```
idea-harvest-agent/
├── main.py                    # Main orchestrator
├── config.py                  # Configuration & API keys
├── web_interface.py           # Flask web app
├── test_system.py             # System tests
├── setup.py                   # Setup script
├── requirements.txt           # Dependencies
├── .env                       # API credentials (your keys)
├── ARCHITECTURE.md            # This file
├── README.md                  # Documentation
├── DEMO_SUMMARY.md            # Demo summary
├── cost_analysis.py           # Cost analysis
│
├── scrapers/                  # Data source scrapers
│   ├── reddit_scraper.py      # Reddit API (PRAW)
│   ├── hackernews_scraper.py  # HN Firebase API
│   └── producthunt_scraper.py # PH GraphQL API
│
├── ai_processor_ollama.py     # OLLAMA AI processor
├── ai_processor.py            # Google AI processor (backup)
│
├── templates/                 # Web interface
│   └── index.html             # Dashboard UI
│
├── data/                      # Data storage (auto-created)
│   ├── reddit_data.json       # Reddit posts
│   ├── hackernews_data.json   # HN stories
│   ├── producthunt_data.json  # PH products
│   └── idea_harvest_results_*.json # Combined results
│
└── output/                    # Generated reports
    ├── idea_harvest_report_*.md # Markdown reports
    └── idea_harvest_results_*.json # JSON results
```

## Data Storage Locations

### 1. **Reddit Data**
- **File**: `reddit_data.json`
- **Source**: Reddit API (PRAW)
- **Content**: Posts from 25+ subreddits
- **Format**: JSON with posts, comments, metadata
- **Size**: ~44 items per run

### 2. **Hacker News Data**
- **File**: `hackernews_data.json`
- **Source**: HN Firebase API
- **Content**: Top stories and comments
- **Format**: JSON with stories, comments, metadata
- **Size**: ~1-5 items per run

### 3. **Product Hunt Data**
- **File**: `producthunt_data.json`
- **Source**: PH GraphQL API
- **Content**: Recent product launches
- **Format**: JSON with products, votes, comments
- **Size**: ~50 items per run

### 4. **Combined Results**
- **File**: `idea_harvest_results_YYYYMMDD_HHMMSS.json`
- **Content**: All processed data + AI analysis
- **Format**: Complete pipeline results
- **Size**: ~95+ items + AI processing

## API Credentials

### **Reddit API**
- **Client ID**: `2XAU4xsPicbSlOwt9RSk-Q`
- **Client Secret**: `LUgsC_uowCDGJIeJoLDtUfby3Q8p-A`
- **User Agent**: `idea-harvest-agent/1.0`

### **Product Hunt API**
- **API Key**: `KnX3Al4Nt6tRcB3g0KHur9ORuMVFo_kmDh7VZKvPg6Y`
- **API Secret**: `eOBc-vpseITccIk6KYzDRqss6cVg1TV06YzeGRhNN-I`
- **Redirect URI**: `https://localhost:8080`

### **Hacker News**
- **API**: Free Firebase API (no credentials needed)

### **OLLAMA AI**
- **Model**: `llama3.2` (local)
- **Cost**: 100% FREE
- **Location**: Local on your Mac

## Performance Metrics

- **Harvest Time**: ~2-3 minutes
- **AI Processing**: ~5-10 minutes
- **Total Runtime**: ~10-15 minutes
- **Data Volume**: 95+ items per run
- **Storage**: ~10-50MB per run
- **Cost**: $0 (completely free)
