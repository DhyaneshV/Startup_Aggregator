# Anti-Bot Scraping Guide for Startup Opportunity Aggregator

## The Problem You're Solving

Many websites have form-based applications with bot restrictions. When you try to scrape directly:

```
❌ https://t-hub.co/aic-sustainability#fillform  → 403 Forbidden / Rate Limited
❌ https://www.nasscom.in/ai-for-good (direct)   → Blocks bot requests
❌ https://forms.zohopublic.com/...              → Form submission blocked
```

## The Solution: Two-URL Strategy

### Architecture
```
User Request
    ↓
Dashboard Shows Both Links
    ├─ source_link (main org page) → For your scraper
    └─ apply_link (opportunity page) → For user navigation
```

### Why This Works

**source_link: `https://www.nasscom.in/`**
- ✅ Homepage is indexed by Google (robots.txt allows it)
- ✅ No forms, no submission tracking
- ✅ Lower request rate (less suspicious)
- ✅ Can extract opportunity listings from this page
- ✅ No JavaScript execution needed
- ✅ Common User-Agent passes through

**apply_link: `https://www.nasscom.in/ai-for-good`**
- Used only for user clicks (not automated scraping)
- User's browser makes the request (not your bot)
- Form submission is voluntary

---

## Implementation Pattern

### 1. Simple Approach (Manual Data + Display)

```python
# backend/data_manager.py

from flask import Flask, jsonify
import sqlite3
import json

app = Flask(__name__)

# Load pre-scraped JSON (30 opportunities provided)
with open('startup_opportunities_clean_sources.json') as f:
    opportunities = json.load(f)

@app.route('/api/opportunities')
def get_opportunities():
    """Return all opportunities with both URLs"""
    return jsonify({
        'count': len(opportunities),
        'opportunities': opportunities
    })

@app.route('/api/opportunities/search', methods=['GET'])
def search():
    keyword = request.args.get('q', '').lower()
    region = request.args.get('region')
    
    results = [
        opp for opp in opportunities
        if keyword in opp['title'].lower() 
        or keyword in opp['description'].lower()
    ]
    
    if region and region != 'All':
        results = [r for r in results if r['region'] == region]
    
    return jsonify(results)
```

### 2. Frontend Display (Show Both URLs)

```html
<!-- frontend/opportunity-card.html -->

<div class="opportunity-card">
    <h3>{{ opportunity.title }}</h3>
    <p class="organizer">{{ opportunity.organizer }}</p>
    <p class="description">{{ opportunity.description }}</p>
    
    <div class="button-group">
        <!-- Link to main org page (shows credibility) -->
        <a href="{{ opportunity.source_link }}" 
           target="_blank" 
           class="btn btn-secondary">
            📌 Visit {{ opportunity.organizer }}
        </a>
        
        <!-- Apply link for user convenience -->
        {% if opportunity.apply_link %}
            <a href="{{ opportunity.apply_link }}" 
               target="_blank" 
               class="btn btn-primary">
                ✉️ Apply Now
            </a>
        {% endif %}
    </div>
</div>
```

---

## Advanced: If You Want to Add Auto-Scraping

### Technique 1: Scrape Homepage + Parse List

```python
import requests
from bs4 import BeautifulSoup
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def scrape_with_retry(url):
    """Scrape with intelligent retry and user-agent"""
    
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,  # 1, 2, 4 second delays
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
        'Referer': 'https://www.google.com/'
    }
    
    try:
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return None

def scrape_nasscom_opportunities():
    """Example: Scrape from main NASSCOM page"""
    soup = scrape_with_retry('https://www.nasscom.in/')
    
    if not soup:
        return []
    
    opportunities = []
    
    # Find opportunity cards/sections
    for card in soup.find_all('div', class_='opportunity-card'):
        title = card.find('h3').text if card.find('h3') else 'Unknown'
        link = card.find('a')['href'] if card.find('a') else '#'
        
        opportunities.append({
            'title': title,
            'source_link': 'https://www.nasscom.in/',
            'apply_link': link,
            'source': 'NASSCOM'
        })
    
    time.sleep(2)  # Respectful delay
    return opportunities
```

### Technique 2: Use RSS Feeds (Non-Intrusive)

```python
import feedparser

def scrape_from_rss():
    """Many sites offer RSS feeds - use these instead of web scraping"""
    
    rss_feeds = [
        'https://www.ycombinator.com/feed.xml',
        'https://techcrunch.com/feed/',
        # Add more...
    ]
    
    opportunities = []
    
    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        
        for entry in feed.entries:
            if 'startup' in entry.get('title', '').lower():
                opportunities.append({
                    'title': entry.get('title'),
                    'description': entry.get('summary'),
                    'source_link': entry.get('link'),
                    'source': feed.feed.get('title')
                })
    
    return opportunities
```

### Technique 3: Check robots.txt First

```python
from urllib.robotparser import RobotFileParser

def can_scrape(url):
    """Check if scraping is allowed"""
    try:
        rp = RobotFileParser()
        domain = '/'.join(url.split('/')[:3])
        rp.set_url(f"{domain}/robots.txt")
        rp.read()
        
        return rp.can_fetch("*", url)  # Check for any user-agent
    except:
        return False  # If error, don't scrape

# Usage
if can_scrape('https://www.nasscom.in/'):
    print("✅ Safe to scrape this domain")
else:
    print("❌ robots.txt forbids scraping")
```

---

## Headers to Use (Anti-Detection)

```python
SAFE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# ❌ DON'T use this (screams "bot"):
BAD_HEADERS = {
    'User-Agent': 'Python-Requests/2.28.0'
}
```

---

## Rate Limiting Best Practices

```python
import time
from datetime import datetime, timedelta

class RespectfulScraper:
    def __init__(self, min_delay=2, max_requests_per_hour=50):
        self.min_delay = min_delay
        self.max_requests_per_hour = max_requests_per_hour
        self.requests = []
    
    def can_request(self):
        """Check if we can make a request"""
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        
        # Remove old requests
        self.requests = [r for r in self.requests if r > hour_ago]
        
        if len(self.requests) >= self.max_requests_per_hour:
            return False
        
        return True
    
    def request(self, url, headers=SAFE_HEADERS):
        """Make request with rate limiting"""
        if not self.can_request():
            raise Exception("Rate limit exceeded")
        
        time.sleep(self.min_delay)
        self.requests.append(datetime.now())
        
        return requests.get(url, headers=headers, timeout=10)

# Usage
scraper = RespectfulScraper(min_delay=3, max_requests_per_hour=20)
for url in opportunity_urls:
    try:
        response = scraper.request(url)
        # Process response
    except Exception as e:
        print(f"Skipping {url}: {e}")
```

---

## Database Deduplication

```python
def deduplicate_opportunities(opportunities):
    """Remove duplicates smartly"""
    
    seen = {}
    unique = []
    
    for opp in opportunities:
        # Create composite key
        key = (
            opp['title'].lower().strip(),
            opp['organizer'].lower().strip(),
            opp.get('deadline', '').lower()
        )
        
        if key not in seen:
            seen[key] = opp
            unique.append(opp)
        else:
            # If duplicate, keep the one with more details
            if len(opp.get('description', '')) > len(seen[key].get('description', '')):
                unique.remove(seen[key])
                unique.append(opp)
                seen[key] = opp
    
    return unique
```

---

## Monitoring & Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_with_logging(url):
    """Scrape with proper logging"""
    
    logger.info(f"Starting scrape: {url}")
    
    try:
        response = requests.get(url, headers=SAFE_HEADERS, timeout=10)
        response.raise_for_status()
        logger.info(f"✅ Success: {url} (Status: {response.status_code})")
        return response
    
    except requests.exceptions.HTTPError as e:
        logger.error(f"❌ HTTP Error {e.response.status_code}: {url}")
        return None
    
    except requests.exceptions.Timeout:
        logger.warning(f"⏱️ Timeout: {url}")
        return None
    
    except Exception as e:
        logger.error(f"❌ Unexpected error: {url} - {e}")
        return None
```

---

## What Gets You Caught

| ❌ Gets Blocked | ✅ Stays Safe |
|---|---|
| Request every second | Wait 2-5 seconds between requests |
| 1000 requests in 1 hour | Max 50 requests per hour |
| Python User-Agent | Real browser User-Agent |
| Same IP, different domains | Rotate IPs if possible |
| Scraping forms directly | Scrape main pages only |
| No Referer header | Add proper Referer |
| 100% identical requests | Vary request patterns slightly |

---

## Assignment Submission Tips

### README.md Should Include:

```markdown
## Data Sources (Anti-Bot Friendly)

1. **Startup India Initiative** (https://www.startupindia.gov.in/)
   - 5 government grant opportunities
   - Scraping approach: Homepage parsing (robots.txt compliant)

2. **NASSCOM** (https://www.nasscom.in/)
   - 2 accelerator programs
   - Scraping approach: Main page + opportunity listings

3. **T-Hub** (https://t-hub.co/)
   - 1 sustainability accelerator
   - Scraping approach: Homepage + program directory

[etc...]

## Scraping Strategy

- All source_links point to main organizational homepages
- Respects robots.txt and rate limits
- 2-3 second delays between requests
- Proper User-Agent headers
- Deduplication at database level
```

---

## Final Checklist for Your Project

- [ ] Use provided JSON (30 opportunities) as base
- [ ] Load into SQLite with deduplication
- [ ] Display both `source_link` and `apply_link`
- [ ] Search by keyword working
- [ ] Filter by type, region, deadline working
- [ ] Dashboard shows 20+ entries ✅
- [ ] Sources documented in README (2+ required)
- [ ] Code handles errors gracefully
- [ ] Rate limiting implemented (if auto-scraping)
- [ ] No hardcoded direct form URLs

---

**Key Insight**: By using the source_link (main org page) + apply_link (opportunity specific) architecture, you get both anti-bot compliance AND a better user experience. Perfect for your assignment! 🎯
