import os
from dotenv import load_dotenv

def load_config():
    """설정 파일 로드"""
    # .config 파일 로드
    load_dotenv('.config')
    
    # 환경 변수에서 설정값 가져오기
    config = {
        'CAFE_NAME': os.getenv('CAFE_NAME'),
        'CLUB_ID': os.getenv('CLUB_ID'),
        'MENU_ID': os.getenv('MENU_ID'),
        'PERIOD_DAYS': int(os.getenv('PERIOD_DAYS', '1')),  # 기본값 1일
        'NAVER_ID': os.getenv('NAVER_ID'),
        'NAVER_PASSWORD': os.getenv('NAVER_PASSWORD')
    }
    
    # 필수 설정값 확인
    missing_values = [k for k, v in config.items() if v is None]
    if missing_values:
        raise ValueError(f"Missing required config values: {', '.join(missing_values)}")
        
    return config