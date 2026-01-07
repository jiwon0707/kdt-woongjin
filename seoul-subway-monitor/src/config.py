import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수 할당
SEOUL_API_KEY = os.getenv("SEOUL_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# 필수 환경 변수 검증
if not SEOUL_API_KEY:
    print("경고: .env 파일에 SEOUL_API_KEY가 설정되지 않았습니다.")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("경고: .env 파일에 Supabase 접속 정보(URL 또는 KEY)가 설정되지 않았습니다.")
