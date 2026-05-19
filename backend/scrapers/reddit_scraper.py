import requests

class RedditScraper:
    def __init__(self):
        # We use the .json endpoint which is scraper-friendly
        self.url = "https://www.reddit.com/r/startups/new.json?limit=25"
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.source = "Reddit"

    def scrape(self):
        items = []
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            data = response.json()
            posts = data.get('data', {}).get('children', [])

            for post in posts:
                p = post.get('data', {})
                title = p.get('title')
                link = "https://www.reddit.com" + p.get('permalink')
                text = p.get('selftext', '')
                
                # Check for opportunity keywords
                keywords = ["hiring", "apply", "program", "grant", "accelerator", "vc", "founder"]
                if any(k in title.lower() for k in keywords):
                    items.append({
                        "title": title[:100],
                        "opportunity_type": "Community",
                        "organizer": "r/startups",
                        "location": "Remote",
                        "region": "International",
                        "source_link": link,
                        "apply_link": link,
                        "source": self.source,
                        "description": text[:250] + "..." if text else "Community discussion on startup growth.",
                        "deadline_text": "Rolling",
                        "ai_tags": ["Community", "Remote", "Networking"]
                    })
        except Exception as e:
            print(f"Reddit Scrape Error: {e}")
        return items
