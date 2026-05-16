import json
import logging
from backend.database.db_config import DatabaseConfig
from backend.database.db_handler import OpportunityDB

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def upload_from_file(file_path):
    """Reads a JSON file and uploads the entries to MongoDB."""
    # 1. Connect to Database
    if not DatabaseConfig.connect():
        logger.error("Could not connect to database.")
        return

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            logger.error("JSON file must contain a list of objects.")
            return

        total_added = 0
        db_handler = OpportunityDB()

        for item in data:
            success, message = db_handler.add_opportunity(item)
            if success:
                total_added += 1
        
        logger.info(f"Manual upload finished. Total added: {total_added}")
    
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
    except json.JSONDecodeError:
        logger.error(f"Failed to decode JSON from {file_path}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Create a template file if it doesn't exist
    template_path = 'manual_data.json'
    try:
        with open(template_path, 'x') as f:
            template = [
                {
                    "title": "Example Opportunity",
                    "opportunity_type": "Grant",
                    "organizer": "Example Org",
                    "location": "Remote",
                    "region": "India",
                    "deadline": "2026-12-31",
                    "source_link": "https://example.com/apply",
                    "source": "Manual",
                    "description": "Short description here.",
                    "eligibility": "Startups only.",
                    "ai_tags": ["AI", "SaaS"]
                }
            ]
            json.dump(template, f, indent=4)
            print(f"Created template file: {template_path}. Please fill it and run the script again.")
    except FileExistsError:
        # If it exists, try to upload it
        upload_from_file(template_path)
