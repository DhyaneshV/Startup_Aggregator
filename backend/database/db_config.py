import os
from dotenv import load_dotenv
from mongoengine import connect
import logging

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class DatabaseConfig:
    """Handles MongoDB connection configuration."""
    
    @staticmethod
    def connect():
        mongodb_uri = os.getenv('MONGODB_URI')
        if not mongodb_uri:
            logger.error("MONGODB_URI not found in environment variables.")
            return False
            
        try:
            # Connect using mongoengine
            connect(host=mongodb_uri)
            logger.info("Successfully connected to MongoDB Atlas.")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    db_connected = DatabaseConfig.connect()
    if db_connected:
        print("Database connection test passed.")
    else:
        print("Database connection test failed.")
