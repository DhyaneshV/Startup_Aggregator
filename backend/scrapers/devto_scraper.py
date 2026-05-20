import requests
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class DevtoScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape(self, keyword="startup"):
        """Scrapes Dev.to for startup-related posts/opportunities using the Articles API."""
        logger.info(f"Scraping Dev.to for: {keyword}")
        opportunities = []
        # Using the Articles API with the specified tag
        url = f"https://dev.to/api/articles?tag={keyword}&top=1"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    for item in data:
                        # Map API fields to our Opportunity model
                        # Note: organization might be None
                        org = item.get('organization')
                        user = item.get('user')
                        organizer = org.get('name') if org else (user.get('name') if user else "Dev.to Author")
                        
                        opp = {
                            "title": item.get('title'),
                            "opportunity_type": "Other",
                            "organizer": organizer,
                            "location": "Remote",
                            "region": "Global",
                            "deadline": None,
                            "deadline_text": "Rolling",
                            "source_link": item.get('url'),
                            "source": "Dev.to",
                            "description": item.get('description', ''),
                            "eligibility": "Check source link for eligibility details."
                        }
                        opportunities.append(opp)
                else:
                    logger.error("Dev.to API returned unexpected data format (expected list)")
            else:
                logger.error(f"Dev.to API returned status code {response.status_code}")
        except Exception as e:
            logger.error(f"Error scraping Dev.to: {e}")
            
        return opportunities

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scraper = DevtoScraper()
    results = scraper.scrape()
    print(f"Found {len(results)} items from Dev.to")
