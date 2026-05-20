# Engineering Challenges: Building a Reliable Scraper Pipeline

Building AURA required overcoming several technical hurdles, particularly around data integrity and the aggressive anti-scraping measures implemented by modern platforms. Below is a detailed breakdown of the primary challenges I faced and the architectural decisions I made to solve them.

### 1. Bypassing Bot Detection (The 403 Forbidden Problem)
**Challenge:** Early in development, my scrapers for TechCrunch and Reddit were frequently flagged as bots, resulting in `403 Forbidden` errors or permanent IP blocks. Standard `requests.get()` calls were insufficient for these high-traffic platforms.

**Solution:**
- **Header Rotation & Mimicry:** I implemented a custom `User-Agent` rotation strategy and included essential headers (like `Accept-Language` and `Referer`) to mimic a standard browser fingerprint.
- **API-First Pivot:** To improve reliability, I shifted from raw HTML scraping to structured data sources where available, such as utilizing the Algolia API for Hacker News and the official Articles API for Dev.to.
- **Exponential Backoff:** I implemented a `RATE_LIMIT_DELAY` between requests to ensure the pipeline adheres to source server policies and avoids triggering rate-limiters.

### 2. Eliminating Data Redundancy
**Challenge:** Startup opportunities are often cross-posted across multiple platforms (e.g., the same grant might appear on both Dev.to and Reddit). This led to a cluttered dashboard with duplicate entries.

**Solution:**
- **Atomic Deduplication:** I implemented a strict deduplication layer at the database level using a **Unique Index** on the `source_link` field in MongoDB. 
- **Upsert Logic:** The ingestion pipeline uses an "upsert" mechanism. If a scraper finds an existing link, the system updates the record's metadata (like tags or description) instead of creating a new entry, ensuring a single source of truth for every opportunity.

### 3. Normalizing Chaotic Temporal Data
**Challenge:** Platforms use wildly different ways to represent deadlines. I encountered everything from relative dates ("3 days ago") and ISO strings to non-standard text like "Rolling Basis" or "Apply ASAP." This made it impossible to build an "Expiring Soon" filter initially.

**Solution:**
- **Hybrid Storage Model:** I architected a dual-field system in my MongoDB schema. The `deadline` field stores a searchable Python `datetime` object, while the `deadline_text` field preserves the original human-readable string.
- **Sanitized Parsing:** I built a normalization script that attempts to parse strings into valid dates but defaults to `None` (for "Rolling") if parsing fails, preventing "fake" dates from breaking the timeline logic.

### 4. Search Performance at Scale
**Challenge:** Storing data in flat JSON files worked for the MVP, but as the index grew to 80+ real-time entries, searching via standard string matching became noticeably slow and imprecise.

**Solution:**
- **Text Indexing:** I migrated the core storage to **MongoDB Atlas** and implemented **Full-Text Indexes** on the `title` and `description` fields. This allowed me to support high-performance keyword searches with relevance ranking, drastically improving the discovery experience.
