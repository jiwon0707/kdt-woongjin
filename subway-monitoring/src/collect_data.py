import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

SEOUL_DATA_API_KEY = os.getenv("SEOUL_DATA_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not all([SEOUL_DATA_API_KEY, SUPABASE_URL, SUPABASE_KEY]):
    print("Error: Missing environment variables. Please check .env file.")
    exit(1)

# Initialize Supabase Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

SUBWAY_LIST = [
    '1호선', '2호선', '3호선', '4호선', '5호선', '6호선', '7호선', '8호선', '9호선',
    '경의중앙선', '공항철도', '경춘선', '수인분당선', '신분당선', '우이신설선', 'GTX-A'
]

def fetch_subway_data(subway_name):
    # API 요청 인자
    KEY = SEOUL_DATA_API_KEY
    TYPE = 'json'
    SERVICE = 'realtimePosition'
    START_INDEX = 0
    END_INDEX = 100 
    
    # URL Encoding handled by requests automatically for params, but here it's path param
    # requests doesn't automatically urlencode path components if inserted like this, so we rely on python execution environment utf-8
    # If issues arise, we might need urllib.parse.quote
    
    url = f"http://swopenapi.seoul.go.kr/api/subway/{KEY}/{TYPE}/{SERVICE}/{START_INDEX}/{END_INDEX}/{subway_name}"

    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        
        if 'realtimePositionList' in data and data['realtimePositionList']:
            return data['realtimePositionList']
        else:
            if 'RESULT' in data and data['RESULT']['CODE'] != 'INFO-000':
                 # INFO-000 is usually success, but sometimes empty list comes with INFO-200 (no data)
                 # print(f"[{subway_name}] Message: {data['RESULT']['MESSAGE']}")
                 pass
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"[{subway_name}] API Error: {e}")
        return []
    except json.JSONDecodeError:
        print(f"[{subway_name}] Error decoding JSON")
        return []

def map_data_to_schema(item):
    try:
        return {
            "line_id": item.get("subwayId"),
            "line_name": item.get("subwayNm"),
            "station_id": item.get("statnId"),
            "station_name": item.get("statnNm"),
            "train_number": item.get("trainNo"),
            "last_received_date": item.get("lastRecptnDt"),
            "last_received_time": item.get("recptnDt"),
            "direction_type": int(item.get("updnLine")) if item.get("updnLine") is not None else None,
            "destination_station_id": item.get("statnTid"),
            "destination_station_name": item.get("statnTnm"),
            "train_status": int(item.get("trainSttus")) if item.get("trainSttus") is not None else None,
            "is_express": int(item.get("directAt")) if item.get("directAt") is not None else None,
            "is_last_train": int(item.get("lstcarAt")) if item.get("lstcarAt") is not None else None,
            # created_at is handled by DB default
        }
    except ValueError as e:
        print(f"Error mapping item: {item} - {e}")
        return None

def insert_data(data_list):
    if not data_list:
        return

    try:
        # Supabase-py insert
        response = supabase.table("subway_realtime_positions").insert(data_list).execute()
        # response.data contains the inserted data
        # print(f"Successfully inserted {len(response.data)} rows.") # Verbose off
        if len(data_list) > 0:
             print(f"Successfully inserted {len(data_list)} rows.")
             
    except Exception as e:
        print(f"Supabase Insert Error: {e}")

def main():
    print(f"Starting data collection... {datetime.now()}")
    
    total_collected = 0
    
    for subway in SUBWAY_LIST:
        raw_data = fetch_subway_data(subway)
        if raw_data:
            mapped_data = [map_data_to_schema(item) for item in raw_data if item is not None]
            # Filter out Nones if mapping failed
            mapped_data = [d for d in mapped_data if d is not None]
            
            if mapped_data:
                insert_data(mapped_data)
                total_collected += len(mapped_data)
    
    print(f"Total {total_collected} records processed.")

if __name__ == "__main__":
    main()
