from database import OpportunityDatabase
from scraper import StartupScraper

def main():
    db = OpportunityDatabase()
    scraper = StartupScraper()
    
    # Define some keywords to get a diverse set of real data
    keywords = ["funding", "grant", "accelerator", "hackathon", "startup"]
    regions = ["", "USA", "India", "Europe"]
    
    total_added = 0
    for keyword in keywords:
        for region in regions:
            print(f"Fetching data for {keyword} in {region}...")
            results = scraper.run_all(keyword=keyword, region=region)
            added = db.insert_many(results)
            total_added += added
            print(f"Added {added} new entries for {keyword} {region}.")
    
    print(f"Population complete. Total new entries added: {total_added}")
    print(f"Database Stats: {db.get_stats()}")

if __name__ == "__main__":
    main()
