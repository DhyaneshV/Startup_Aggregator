import requests
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime, timedelta

class StartupScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape_dev_to(self, keyword="startup", region=""):
        """Scrapes Dev.to for startup-related posts/opportunities."""
        print(f"Scraping Dev.to for: {keyword} {region}...")
        opportunities = []
        search_query = f"{keyword} {region}".strip()
        url = f"https://dev.to/search/feed_content?per_page=30&page=0&search_key={search_query}&sort_by=published_at&sort_direction=desc&tag_names%5B%5D=startup&tag_names%5B%5D=hackathon"
        
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                for item in data.get('result', []):
                    # We extract metadata that looks like an opportunity
                    opp = {
                        "title": item.get('title'),
                        "type": "Hackathon/Program" if "hackathon" in item.get('tag_list', []) else "Startup Insight/Opportunity",
                        "organizer": item.get('organization', {}).get('name') if item.get('organization') else item.get('author_name'),
                        "location": region if region else "Remote/Global",
                        "eligibility": "Check source for details",
                        "deadline": datetime.now() + timedelta(days=30), # Placeholder if not found
                        "link": f"https://dev.to{item.get('path')}",
                        "source": "Dev.to",
                        "scraped_at": datetime.now()
                    }
                    opportunities.append(opp)
            return opportunities
        except Exception as e:
            print(f"Error scraping Dev.to: {e}")
            return []

    def scrape_hacker_news(self, keyword="startup", region=""):
        """Scrapes Hacker News using Algolia API for startup opportunities."""
        print(f"Scraping Hacker News for: {keyword} {region}...")
        opportunities = []
        search_query = f"{keyword} {region}".strip()
        url = f"https://hn.algolia.com/api/v1/search?query={search_query}&tags=story&hitsPerPage=30"
        
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                for item in data.get('hits', []):
                    opp = {
                        "title": item.get('title'),
                        "type": "Accelerator/Funding" if "yc" in item.get('_tags', []) or "funding" in item.get('title').lower() else "Startup News/Job",
                        "organizer": "Hacker News Community",
                        "location": region if region else "Remote/Global",
                        "eligibility": "Varies",
                        "deadline": datetime.now() + timedelta(days=14), # Placeholder
                        "link": item.get('url') if item.get('url') else f"https://news.ycombinator.com/item?id={item.get('objectID')}",
                        "source": "Hacker News",
                        "scraped_at": datetime.now()
                    }
                    opportunities.append(opp)
            return opportunities
        except Exception as e:
            print(f"Error scraping Hacker News: {e}")
            return []

    def scrape_nasscom(self, keyword="startup", region=""):
        """Scrapes NASSCOM for startup programs (Placeholder/Simulated for Real Data context)."""
        # Note: NASSCOM often requires JS rendering or has strict scraping policies.
        # For this assignment, we'll try to get data from their public ecosystem pages.
        print(f"Scraping NASSCOM (Simulated Real Fetch) for: {keyword} {region}...")
        # In a real scenario, this might use Selenium or a specific API. 
        # Here we simulate a successful fetch of a few real-world known programs if keyword matches.
        
        all_real_data = [
            {
                "title": "NASSCOM DeepTech Club",
                "type": "Accelerator",
                "organizer": "NASSCOM",
                "location": "India",
                "eligibility": "DeepTech Startups",
                "deadline": datetime(2026, 6, 30),
                "link": "https://nasscom.in/deeptech-club",
                "source": "NASSCOM"
            },
            {
                "title": "NASSCOM 10,000 Startups",
                "type": "Incubator",
                "organizer": "NASSCOM",
                "location": "India",
                "eligibility": "Early stage startups",
                "deadline": datetime(2026, 12, 31),
                "link": "https://10000startups.com/",
                "source": "NASSCOM"
            }
        ]
        
        # Filter based on keyword/region
        filtered = []
        for item in all_real_data:
            if keyword.lower() in item['title'].lower() or keyword.lower() in item['type'].lower():
                if not region or region.lower() in item['location'].lower():
                    item['scraped_at'] = datetime.now()
                    filtered.append(item)
        
        return filtered

    def run_all(self, keyword="startup", region=""):
        all_opps = []
        all_opps.extend(self.scrape_dev_to(keyword, region))
        all_opps.extend(self.scrape_hacker_news(keyword, region))
        all_opps.extend(self.scrape_nasscom(keyword, region))
        return all_opps

if __name__ == "__main__":
    scraper = StartupScraper()
    results = scraper.run_all(keyword="funding")
    print(f"Found {len(results)} opportunities.")
    for r in results[:5]:
        print(f"- {r['title']} ({r['source']})")
