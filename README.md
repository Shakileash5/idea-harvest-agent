# 🚀 Idea Harvest Agent

An AI-powered system that harvests problem statements from various sources (Reddit, Hacker News, Product Hunt, etc.) and generates validated micro-SaaS ideas with comprehensive validation playbooks.

## ✨ Features

- **Multi-Source Harvesting**: Automatically scrapes problem statements from Reddit, Hacker News, Product Hunt, and more
- **AI-Powered Processing**: Uses Google's Gemini AI to normalize, cluster, and score problems
- **Idea Generation**: Generates specific product ideas with target personas and monetization strategies
- **Validation Playbooks**: Creates actionable validation experiments for each idea
- **Web Interface**: Beautiful, responsive web UI for easy interaction
- **Export Options**: Export results as JSON or Markdown reports

## 🏗️ System Architecture

```
┌─────────────┐      ┌───────────────┐      ┌─────────────┐
│ Data Source │──▶──▶│ Scraper Layer │──▶──▶│ Raw Dataset │
└─────────────┘      └───────────────┘      └─────────────┘
   Reddit, HN,          Python (APIs,        JSON/CSV of
   Product Hunt,        BeautifulSoup,       problem statements
   G2, App Reviews      PRAW, requests)

┌──────────────────┐
│ AI Agent (LLM)   │
│ Gemini Free or   │
│ Ollama LLaMA 3.2 │
└──────────────────┘
   ▲ Normalize, cluster, score,
   │ generate validation playbooks
   ▼
┌───────────────┐
│ Final Outputs │
│  - JSON       │
│  - Markdown   │
│  - Ranked     │
└───────────────┘
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd idea-harvest-agent

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### 2. Configuration

Create a `.env` file with your API keys:

```env
# Reddit API credentials (get from https://www.reddit.com/prefs/apps)
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=idea-harvest-agent/1.0

# Google AI API key (get from https://makersuite.google.com/app/apikey)
GOOGLE_AI_API_KEY=your_google_ai_api_key

# Optional: SerpAPI for enhanced search
SERPAPI_KEY=your_serpapi_key
```

### 3. Run the System

#### Option A: Command Line Interface

```bash
# Run the full pipeline
python main.py

# Or run individual components
python -c "from main import IdeaHarvestAgent; agent = IdeaHarvestAgent(); agent.harvest_all_sources()"
```

#### Option B: Web Interface

```bash
# Start the web server
python web_interface.py

# Open http://localhost:5000 in your browser
```

## 📊 Output Format

The system generates two main outputs:

### 1. JSON Results (`idea_harvest_results_YYYYMMDD_HHMMSS.json`)

```json
{
  "harvest_summary": {
    "reddit": {"items_found": 45, "status": "success"},
    "hackernews": {"items_found": 23, "status": "success"},
    "producthunt": {"items_found": 12, "status": "success"}
  },
  "normalized_problems": [...],
  "clusters": [...],
  "scored_clusters": [...],
  "top_ideas": [...],
  "validation_playbooks": {...}
}
```

### 2. Markdown Report (`idea_harvest_report_YYYYMMDD_HHMMSS.md`)

Human-readable report with:
- Harvest summary
- Top problem clusters with scores
- Detailed product ideas
- Validation playbooks
- Actionable next steps

## 🔧 API Endpoints

The web interface provides these REST endpoints:

- `POST /api/harvest` - Start harvesting problems
- `POST /api/process` - Process and cluster problems
- `POST /api/ideas` - Generate product ideas
- `POST /api/playbooks` - Create validation playbooks
- `POST /api/run-full` - Run complete pipeline
- `GET /api/results` - Get current results
- `GET /api/export/json` - Export JSON results
- `GET /api/export/markdown` - Export Markdown report

## 🎯 Scoring Algorithm

Each problem cluster is scored on:

- **Frequency (30%)**: How many times the problem appears
- **Willingness to Pay (25%)**: Mentions of paying, expensive alternatives
- **Competition (20%)**: Market saturation level
- **Ease of MVP (15%)**: Technical complexity for solo developer
- **Virality (10%)**: Referral and growth potential

## 🛠️ Customization

### Adding New Sources

1. Create a new scraper class in `scrapers/`
2. Implement the `harvest_problems()` method
3. Add to the scrapers dictionary in `main.py`

### Modifying AI Prompts

Edit the prompts in `ai_processor.py` to customize:
- Problem normalization
- Clustering logic
- Scoring criteria
- Idea generation
- Validation playbooks

### Adjusting Search Queries

Modify `SEARCH_QUERIES` in `config.py` to target different problem types.

## 📈 Example Results

After running the system, you might get ideas like:

### 1. **DataFlow Automator**
- **Problem**: Manual data entry is time-consuming
- **Solution**: AI-powered data entry automation
- **Target**: Small businesses, 1-50 employees
- **Pricing**: $29/month SaaS
- **Validation**: Reddit survey in r/smallbusiness

### 2. **Social Media Scheduler Pro**
- **Problem**: Managing multiple social media accounts manually
- **Solution**: Unified scheduling and analytics platform
- **Target**: Content creators, small agencies
- **Pricing**: $19/month per account
- **Validation**: Product Hunt launch + influencer outreach

## 🔍 Troubleshooting

### Common Issues

1. **Reddit API Rate Limits**: Reduce `MAX_ITEMS_PER_SOURCE` in config.py
2. **Google AI API Errors**: Check your API key and quota
3. **Empty Results**: Verify your search queries and source availability
4. **Memory Issues**: Process data in smaller batches

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Reddit API for data access
- Google AI for language processing
- Product Hunt for startup insights
- Hacker News community for problem statements

## 📞 Support

For questions or issues:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the API documentation

---

**Happy Idea Harvesting! 🚀**
