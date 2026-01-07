import time
import schedule
import logging
from src.api_client import SubwayAPIClient
from src.db_client import SubwayDBClient

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def job():
    """
    Job to fetch data for all lines and insert into DB.
    """
    logger.info("Starting scheduled job...")
    api = SubwayAPIClient()
    db = SubwayDBClient()
    
    # List of lines to monitor
    # Note: '1호선'~'9호선', '신분당선', '경의중앙선', etc. can be added.
    # Starting with Lines 1-9 for standard coverage.
    lines = [f"{i}호선" for i in range(1, 10)]
    
    total_records = 0
    for line in lines:
        data = api.get_realtime_positions(line)
        if data:
            db.insert_data(data)
            total_records += len(data)
            
    logger.info(f"Job completed. Total records processed: {total_records}")

def main():
    logger.info("Starting Seoul Subway Monitor System...")
    
    # Schedule the job every 1 minute
    schedule.every(1).minutes.do(job)
    
    # Run once immediately on startup
    try:
        job()
    except Exception as e:
        logger.error(f"Error during initial job execution: {e}")
    
    # Loop
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            break
        except Exception as e:
            logger.error(f"Scheduler error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
