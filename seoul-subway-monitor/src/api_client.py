import requests
import logging
from src.config import SEOUL_API_KEY

class SubwayAPIClient:
    """
    Client for fetching real-time data from Seoul Open Data Plaza API.
    """
    BASE_URL = "http://swopenAPI.seoul.go.kr/api/subway"

    def __init__(self):
        self.api_key = SEOUL_API_KEY
        self.logger = logging.getLogger(__name__)

    def get_realtime_positions(self, line_name):
        """
        Fetch real-time subway positions for a given line.
        
        Args:
            line_name (str): The name of the subway line (e.g., '1호선', '2호선')
            
        Returns:
            list: A list of dictionaries containing real-time position data.
        """
        # API URL format: /api/subway/{KEY}/{TYPE}/{SERVICE}/{START_INDEX}/{END_INDEX}/{LINE_NAME}
        # Fetch up to 100 records
        url = f"{self.BASE_URL}/{self.api_key}/json/realtimePosition/0/100/{line_name}"
        
        try:
            self.logger.info(f"Fetching data for {line_name}...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Check for API-specific error codes or successful data
            if 'realtimePositionList' in data:
                items = data['realtimePositionList']
                self.logger.info(f"Successfully fetched {len(items)} records for {line_name}.")
                return items
            else:
                msg = data.get('RESULT', {}).get('MESSAGE', 'Unknown error')
                if msg == "INFO-000": # Normal (No data?) - actually INFO-000 is usually success, but check response structure
                    # If empty list but success
                    return []
                self.logger.warning(f"No data for {line_name}: {msg}")
                return []
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API Request failed for {line_name}: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Unexpected error for {line_name}: {e}")
            return []
