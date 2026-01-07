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
                self.logger.error(f"Supabase 클라이언트 초기화 실패: {e}")
                self.supabase = None
        else:
            self.supabase = None
            self.logger.error("Supabase 인증 정보 누락. DB 작업이 실패할 것입니다.")

    def insert_data(self, data_list):
        """
        데이터를 변환하여 realtime_subway_positions 테이블에 삽입합니다.
        """
        if not self.supabase or not data_list:
            return

        records = []
        for item in data_list:
            try:
                # 불리언 타입으로 안전하게 변환
                is_last_str = str(item.get("lstcarAt", "0"))
                is_last = True if is_last_str == '1' else False
                
                # DB 스키마에 맞춰 키 이름 변환
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
                self.logger.warning(f"항목 파싱 오류 {item}: {e}")
                continue
        
        if not records:
            return

        try:
            response = self.supabase.table("realtime_subway_positions").insert(records).execute()
            self.logger.info(f"{len(records)}건의 데이터가 성공적으로 삽입되었습니다.")
        except Exception as e:
            self.logger.error(f"Supabase 데이터 삽입 실패: {e}")
