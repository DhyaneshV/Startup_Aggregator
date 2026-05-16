import logging
import time
from apscheduler.schedulers.background import BackgroundScheduler
from backend.services.pipeline import DataPipeline

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_automation():
    """Function to be executed by the scheduler."""
    logger.info("Automatic pipeline run started...")
    pipeline = DataPipeline()
    pipeline.run()
    logger.info("Automatic pipeline run completed.")

if __name__ == "__main__":
    # 1. Initialize Scheduler
    scheduler = BackgroundScheduler()
    
    # 2. Add job: Run every 24 hours
    scheduler.add_job(run_automation, 'interval', hours=24)
    
    # 3. Start Scheduler
    scheduler.start()
    logger.info("Scheduler started. Pipeline will run every 24 hours.")
    
    # 4. Optional: Run once immediately on start
    run_automation()

    # 5. Keep the main thread alive
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Scheduler stopped.")
