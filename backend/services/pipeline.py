import logging
from backend.database.db_config import DatabaseConfig
from backend.database.db_handler import OpportunityDB
from backend.scrapers.devto_scraper import DevtoScraper
from backend.scrapers.hackernews_scraper import HackerNewsScraper
from backend.scrapers.techcrunch_scraper import TechCrunchScraper
from backend.scrapers.reddit_scraper import RedditScraper
from backend.services.alert_service import AlertService

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataPipeline:
    def __init__(self):
        self.db_handler = OpportunityDB()
        self.scrapers = [
            DevtoScraper(),
            HackerNewsScraper(),
            TechCrunchScraper(),
            RedditScraper()
        ]

    def run(self):
        """Runs the entire pipeline: Scraping -> Database Storage -> Alerts."""
        logger.info("Starting Data Pipeline...")

        # 1. Connect to Database
        if not DatabaseConfig.connect():
            logger.error("Pipeline aborted: Could not connect to database.")
            return

        total_added = 0
        total_duplicates = 0
        new_opportunities = []

        # 2. Run Scrapers
        for scraper in self.scrapers:
            source_name = scraper.__class__.__name__
            logger.info(f"Running scraper: {source_name}")
            
            try:
                items = scraper.scrape()
                logger.info(f"Scraped {len(items)} items from {source_name}")
                
                # 3. Store in Database
                for item in items:
                    success, message = self.db_handler.add_opportunity(item)
                    if success:
                        total_added += 1
                        new_opportunities.append(item)
                    elif message == "Duplicate":
                        total_duplicates += 1
            except Exception as e:
                logger.error(f"Error running scraper {source_name}: {e}")

        # 4. Send Alerts for new matches
        if new_opportunities:
            logger.info(f"Triggering alerts for {len(new_opportunities)} new opportunities.")
            AlertService.send_alerts(new_opportunities)

        logger.info(f"Pipeline finished. Total added: {total_added}, Duplicates skipped: {total_duplicates}")

if __name__ == "__main__":
    pipeline = DataPipeline()
    pipeline.run()
