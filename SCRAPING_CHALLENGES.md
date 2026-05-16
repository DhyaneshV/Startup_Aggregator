# 🛠️ Scraping Challenges & Solutions

Building a robust aggregator for startup opportunities involves overcoming several technical hurdles. Here are the key challenges faced during this project and how they were solved.

## 1. Data Consistency Across Sources
**Challenge**: Different websites use different formats (RSS feeds, HTML, JSON). For example, Dev.to provides an RSS feed, while Hacker News requires direct HTML parsing.
**Solution**: Implemented a modular **Scraper Pattern**. Each source has its own class (`DevtoScraper`, `HackerNewsScraper`) that inherits from a base interface, ensuring they all return data in a standardized format for the database.

## 2. Duplicate Detection
**Challenge**: Multiple platforms often list the same opportunity. Storing duplicates would clutter the dashboard.
**Solution**: Used **Unique Indexes** in MongoDB on the `source_link` field. The `db_handler` uses a try-except block to catch `NotUniqueError`, effectively ignoring any entry that has already been saved.

## 3. Dynamic Filtering
**Challenge**: Users need to filter by Type, Source, and Deadline, but the data from various sources might have missing fields.
**Solution**: 
- **Type Mapping**: Scrapers map source-specific tags to a standard set (Accelerator, Grant, etc.).
- **Backend Querying**: Used `mongoengine` to build a dynamic query object that only applies filters provided by the user via API query parameters.

## 4. Scheduling & Data Freshness
**Challenge**: Startup opportunities expire quickly. Manual runs are inefficient.
**Solution**: Integrated `APScheduler` to create an automated background task that runs the entire scraping pipeline every 24 hours without human intervention.

## 5. Anti-Scraping Measures
**Challenge**: Some sites might block frequent automated requests.
**Solution**: 
- Set proper **User-Agent** headers in all requests to mimic real browser behavior.
- Implemented error handling to skip a source gracefully if it returns a 403 or 429 error, preventing the entire pipeline from crashing.

## 6. Frontend Performance
**Challenge**: Displaying 60+ cards with descriptions can be slow or visually overwhelming.
**Solution**: Used a responsive CSS Grid layout and implemented a "substring" rule on descriptions to keep cards uniform and fast to render.
