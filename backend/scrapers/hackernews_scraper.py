import requests
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class HackerNewsScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape(self, keyword="startup"):
        """Scrapes Hacker News using Algolia API for startup stories."""
        logger.info(f"Scraping Hacker News for: {keyword}")
        opportunities = []
        # Using Algolia API for HN search
        url = f"https://hn.algolia.com/api/v1/search?query={keyword}&tags=story&hitsPerPage=30"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for item in data.get('hits', []):
                    # Map API fields to our Opportunity model
                    opp = {
                        "title": item.get('title'),
                        "opportunity_type": "Other",
                        "organizer": "Hacker News Community",
                        "location": "Remote",
                        "region": "Global",
                        "deadline": None, 
                        "deadline_text": "Rolling",
                        "source_link": item.get('url') if item.get('url') else f"https://news.ycombinator.com/item?id={item.get('objectID')}",
                        "source": "Hacker News",
                        "description": f"Posted by {item.get('author')}",
                        "eligibility": "Varies. Check the thread for details."
                    }
                    opportunities.append(opp)
            else:
                logger.error(f"HN API returned status code {response.status_code}")
        except Exception as e:
            logger.error(f"Error scraping Hacker News: {e}")
            
        return opportunities

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scraper = HackerNewsScraper()
    results = scraper.scrape()
    print(f"Found {len(results)} items from Hacker News")
