import time
import schedule
import logging
from src.api_client import SubwayAPIClient
from src.db_client import SubwayDBClient

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def job():
    """
    모든 호선에 대한 데이터를 수집하고 DB에 저장하는 작업 함수.
    """
    logger.info("예약된 작업을 시작합니다...")
    api = SubwayAPIClient()
    db = SubwayDBClient()
    
    # 모니터링할 호선 목록
    # 참고: '1호선'~'9호선', '신분당선', '경의중앙선' 등 추가 가능
    # 기본 커버리지를 위해 1호선부터 9호선까지 포함
    lines = [f"{i}호선" for i in range(1, 10)]
    
    total_records = 0
    for line in lines:
        data = api.get_realtime_positions(line)
        if data:
            db.insert_data(data)
            total_records += len(data)
            
    logger.info(f"작업 완료. 총 처리된 레코드 수: {total_records}")

def main():
    logger.info("서울 지하철 모니터링 시스템을 시작합니다...")
    
    # 1분마다 job 함수 실행 예약
    schedule.every(1).minutes.do(job)
    
    # 시작 시점에도 한 번 즉시 실행
    try:
        job()
    except Exception as e:
        logger.error(f"초기 실행 중 오류 발생: {e}")
    
    # 무한 루프
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            logger.info("스케줄러를 정지합니다...")
            break
        except Exception as e:
            logger.error(f"스케줄러 오류: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
