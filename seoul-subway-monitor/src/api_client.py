import requests
import logging
from src.config import SEOUL_API_KEY

class SubwayAPIClient:
    """
    서울 열린데이터 광장 API로부터 실시간 지하철 위치 데이터를 수집하는 클라이언트 클래스.
    """
    BASE_URL = "http://swopenAPI.seoul.go.kr/api/subway"

    def __init__(self):
        self.api_key = SEOUL_API_KEY
        self.logger = logging.getLogger(__name__)

    def get_realtime_positions(self, line_name):
        """
        주어진 호선명에 대한 실시간 열차 위치 정보를 조회합니다.
        
        Args:
            line_name (str): 조회할 호선명 (예: '1호선', '2호선')
            
        Returns:
            list: 실시간 열차 위치 정보가 담긴 딕셔너리 리스트.
        """
        # API URL 형식: /api/subway/{KEY}/{TYPE}/{SERVICE}/{START_INDEX}/{END_INDEX}/{LINE_NAME}
        # 한 번에 최대 100건 조회
        url = f"{self.BASE_URL}/{self.api_key}/json/realtimePosition/0/100/{line_name}"
        
        try:
            self.logger.info(f"{line_name} 데이터 수집 중...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # API 응답 상태 확인 및 데이터 추출
            if 'realtimePositionList' in data:
                items = data['realtimePositionList']
                self.logger.info(f"{line_name} 데이터 {len(items)}건 수집 성공.")
                return items
            else:
                msg = data.get('RESULT', {}).get('MESSAGE', '알 수 없는 오류')
                if msg == "INFO-000": # 정상 (데이터 없음) - INFO-000은 보통 정상이지만 데이터가 없을 때도 반환될 수 있음
                    # 리스트가 비어있지만 성공인 경우
                    return []
                self.logger.warning(f"{line_name} 데이터 없음: {msg}")
                return []
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"{line_name} API 요청 실패: {e}")
            return []
        except Exception as e:
            self.logger.error(f"{line_name} 예상치 못한 오류 발생: {e}")
            return []
