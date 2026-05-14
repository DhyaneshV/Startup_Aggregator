# Startup Aggregator

An automated pipeline to aggregate startup opportunities (grants, accelerators, news) from various sources like Dev.to, HackerNews, NASSCOM, and StartupIndia.

## 🚀 Setup Instructions
1. Clone the repository
2. Install dependencies: `pip install -r backend/requirements.txt`
3. Set up your `.env` file based on `.env.example`
4. Run the application: `python main.py`

## 🌐 Data Sources
- **Dev.to**: RSS Feed for startup-tagged articles.
- **HackerNews**: HTML scraping of the jobs page.
- **NASSCOM**: Manual data entry for key programs.
- **StartupIndia**: Manual data entry for government grants.
