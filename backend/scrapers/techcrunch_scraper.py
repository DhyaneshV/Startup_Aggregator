import requests
from bs4 import BeautifulSoup
from datetime import datetime

class TechCrunchScraper:
    def __init__(self):
        self.url = "https://techcrunch.com/feed/"
        self.source = "TechCrunch"

    def scrape(self):
        items = []
        try:
            response = requests.get(self.url, timeout=10)
            soup = BeautifulSoup(response.content, 'xml')
            entries = soup.find_all('item')

            for entry in entries:
                title = entry.title.text
                link = entry.link.text
                description = entry.description.text if entry.description else "High-impact startup news and strategic insights."
                
                # Filter for opportunity-like keywords
                keywords = ["launch", "accelerator", "funding", "grant", "startup", "program", "cohort"]
                if any(k in title.lower() or k in description.lower() for k in keywords):
                    items.append({
                        "title": title,
                        "opportunity_type": "News/Event",
                        "organizer": "TechCrunch",
                        "location": "Global",
                        "region": "International",
                        "source_link": link,
                        "apply_link": link,
                        "source": self.source,
                        "description": description[:300] + "...",
                        "deadline_text": "Check Portal",
                        "ai_tags": ["Tech", "News", "Silicon Valley"]
                    })
        except Exception as e:
            print(f"TechCrunch Scrape Error: {e}")
        return items
