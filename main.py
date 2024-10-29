from naver_cafe_crawler import NaverCafeCrawler
from datetime import datetime
from config import load_config

def main():
    # 카페 정보 설정
    config = load_config()

    CAFE_NAME = config['CAFE_NAME']
    CLUB_ID = config['CLUB_ID']
    MENU_ID = config['MENU_ID']
    PERIOD_DAYS = config['PERIOD_DAYS']
    
    # 네이버 로그인 정보
    NAVER_ID = config['NAVER_ID']
    NAVER_PASSWORD = config['NAVER_PASSWORD']
    
    crawler = None
    
    try:
        print("크롤러를 초기화하는 중...")
        crawler = NaverCafeCrawler(
            cafe_name=CAFE_NAME,
            club_id=CLUB_ID,
            menu_id=MENU_ID,
            period_days=PERIOD_DAYS,
            debug_mode=True  # 크롤링 과정을 확인하려면 True
        )
        
        # 로그인
        if not crawler.login(NAVER_ID, NAVER_PASSWORD):
            raise Exception("로그인에 실패했습니다.")
        
        # 게시글 크롤링
        print("게시글을 수집하는 중...")
        articles = crawler.crawl_articles()
        
        # 결과 저장
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"naver_cafe_articles_{current_time}.xlsx"
        
        print(f"수집된 게시글을 저장하는 중...")
        crawler.save_to_excel(articles, filename)
        
        print(f"\n크롤링이 완료되었습니다.")
        print(f"총 {len(articles)}개의 게시글이 수집되었습니다.")
        
    except Exception as e:
        print(f"\n에러가 발생했습니다: {str(e)}")
        
    finally:
        if crawler:
            print("\n크롤러를 종료합니다...")
            crawler.close()

if __name__ == "__main__":
    main()