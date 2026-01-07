from supabase import create_client, Client
import logging
from src.config import SUPABASE_URL, SUPABASE_KEY

class SubwayDBClient:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        if SUPABASE_URL and SUPABASE_KEY:
            try:
                self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
            except Exception as e:
                self.logger.error(f"Failed to initialize Supabase client: {e}")
                self.supabase = None
        else:
            self.supabase = None
            self.logger.error("Supabase credentials missing. DB operations will fail.")

    def insert_data(self, data_list):
        """
        Transform and insert data into realtime_subway_positions table.
        """
        if not self.supabase or not data_list:
            return

        records = []
        for item in data_list:
            try:
                # Safe boolean conversion
                is_last_str = str(item.get("lstcarAt", "0"))
                is_last = True if is_last_str == '1' else False
                
                # Transform keys to match DB schema
                record = {
                    "line_id": item.get("subwayId"),
                    "line_name": item.get("subwayNm"),
                    "station_id": item.get("statnId"),
                    "station_name": item.get("statnNm"),
                    "train_number": item.get("trainNo"),
                    "last_rec_date": item.get("lastRecptnDt"),
                    "last_rec_time": item.get("recptnDt"),
                    "direction_type": item.get("updnLine"),
                    "dest_station_id": item.get("statnTid"),
                    "dest_station_name": item.get("statnTnm"),
                    "train_status": item.get("trainSttus"),
                    "is_express": item.get("directAt"),
                    "is_last_train": is_last,
                }
                records.append(record)
            except Exception as e:
                self.logger.warning(f"Error parsing item {item}: {e}")
                continue
        
        if not records:
            return

        try:
            response = self.supabase.table("realtime_subway_positions").insert(records).execute()
            self.logger.info(f"Successfully inserted {len(records)} records.")
        except Exception as e:
            self.logger.error(f"Failed to insert data into Supabase: {e}")
