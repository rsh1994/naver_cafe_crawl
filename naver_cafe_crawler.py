from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import pandas as pd
import re
import os
import ssl
import chromedriver_autoinstaller

class NaverCafeCrawler:
    def __init__(self, cafe_name, club_id, menu_id, period_days=365, debug_mode=False):
        self.cafe_name = cafe_name
        self.club_id = club_id
        self.menu_id = menu_id
        self.period_days = period_days
        self.debug_mode = debug_mode
        self.base_url = f"https://cafe.naver.com/{cafe_name}"
        
        # SSL 설정
        ssl._create_default_https_context = ssl._create_unverified_context
        
        # 브라우저 설정
        self.driver = self._setup_driver()
        self.target_date = datetime.now() - timedelta(days=period_days)
        
    def _setup_driver(self):
        chrome_options = webdriver.ChromeOptions()
        if not self.debug_mode:
            chrome_options.add_argument('--headless')
            
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--allow-insecure-localhost')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        chromedriver_autoinstaller.install()
        return webdriver.Chrome(options=chrome_options)

    def login(self, id, password):
        """네이버 로그인"""
        try:
            print("로그인 시도 중...")
            self.driver.get("https://nid.naver.com/nidlogin.login")
            time.sleep(2)
            
            if self.debug_mode:
                print("디버그 모드: 수동 로그인을 위해 대기 중...")
                input("로그인을 완료한 후 Enter 키를 눌러주세요...")
            else:
                self.driver.execute_script(f"document.getElementsByName('id')[0].value='{id}'")
                self.driver.execute_script(f"document.getElementsByName('pw')[0].value='{password}'")
                self.driver.find_element(By.ID, "log.login").click()
                time.sleep(2)
            
            print("로그인 완료")
            return True
        except Exception as e:
            print(f"로그인 실패: {str(e)}")
            return False

    def parse_date(self, date_str):
        """날짜 문자열 파싱"""
        try:
            now = datetime.now()
            if ':' in date_str:  # 오늘 날짜 (HH:MM)
                hour, minute = map(int, date_str.split(':'))
                return datetime(now.year, now.month, now.day, hour, minute)
            else:  # YYYY.MM.DD. 형식
                date_str = date_str.rstrip('.')
                return datetime.strptime(date_str, '%Y.%m.%d')
        except Exception as e:
            print(f"날짜 파싱 에러: {e}, 입력값: {date_str}")
            return None

    def get_article_content(self, article_id):
        """게시글 상세 내용 추출"""
        try:
            article_url = f"{self.base_url}/ArticleRead.nhn?clubid={self.club_id}&articleid={article_id}&boardtype=L"
            self.driver.get(article_url)
            time.sleep(2)
            
            # iframe으로 전환
            self.driver.switch_to.frame("cafe_main")
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # 본문 내용 추출
            content = ""
            main_content = soup.select_one('.se-main-container')
            if main_content:
                content = main_content.get_text(strip=True)
            else:
                content_div = soup.select_one('.article_container')
                if content_div:
                    content = content_div.get_text(strip=True)
            
            return content
        except Exception as e:
            print(f"내용 추출 에러: {e}")
            return None

    def crawl_articles(self):
        """게시글 크롤링 실행"""
        articles = []
        page = 1
        continue_crawling = True
        
        while continue_crawling:
            try:
                print(f"\n페이지 {page} 크롤링 중...")
                
                # 게시글 목록 페이지 접속
                page_url = f"{self.base_url}?iframe_url=/ArticleList.nhn?search.clubid={self.club_id}&search.menuid={self.menu_id}&search.boardtype=L&search.page={page}"
                self.driver.get(page_url)
                time.sleep(2)
                
                # iframe으로 전환
                self.driver.switch_to.frame("cafe_main")
                
                # 게시글 목록 파싱
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                
                # 모든 tr 태그 선택
                all_rows = soup.select('div.article-board > table > tbody > tr')
                
                # 공지사항과 일반 게시글 분리
                article_rows = []
                for row in all_rows:
                    # 상단 고정 공지는 제외
                    parent_div = row.find_parent('div', id='upperArticleList')
                    if parent_div:
                        continue
                        
                    # board-notice 클래스가 있는 일반 공지도 제외
                    if 'board-notice' in row.get('class', []):
                        continue
                        
                    article_rows.append(row)
                
                print(f"발견된 일반 게시글 수: {len(article_rows)}")
                
                if not article_rows:
                    print("더 이상 게시글이 없습니다.")
                    break
                
                found_articles = False
                for row in article_rows:
                    try:
                        # 제목 추출
                        title_element = row.select_one('a.article')
                        if not title_element:
                            continue
                            
                        title = title_element.get_text(strip=True)
                        href = title_element['href']
                        article_id = href.split('articleid=')[1].split('&')[0]
                        
                        # 날짜와 조회수
                        date_element = row.select_one('.td_date')
                        view_element = row.select_one('.td_view')
                        
                        if not date_element or not view_element:
                            continue
                            
                        date_str = date_element.text.strip()
                        views = view_element.text.strip()
                        
                        post_date = self.parse_date(date_str)
                        if not post_date:
                            continue
                            
                        # 기간 체크 (일반 게시글만)
                        if post_date < self.target_date:
                            print(f"기간 초과: {date_str}")
                            continue_crawling = False
                            break
                        
                        # 게시글 상세 내용
                        content = self.get_article_content(article_id)
                        
                        articles.append({
                            'title': title,
                            'content': content,
                            'date': post_date,
                            'views': views,
                            'article_id': article_id
                        })
                        
                        found_articles = True
                        print(f"게시글 추출 완료: {title} ({date_str}, 조회수: {views})")
                        
                    except Exception as e:
                        print(f"게시글 처리 중 에러: {e}")
                        continue
                
                if not found_articles:
                    print("이 페이지에서 추출할 게시글이 없습니다.")
                    break
                
                page += 1
                time.sleep(1)
                
            except Exception as e:
                print(f"페이지 처리 중 에러: {e}")
                if self.debug_mode:
                    print("상세 에러:", e)
                    print("현재 URL:", self.driver.current_url)
                break
        
        return articles

    def save_to_excel(self, articles, filename):
        """크롤링 결과를 엑셀로 저장"""
        if not articles:
            print("저장할 게시글이 없습니다.")
            return
            
        try:
            df = pd.DataFrame(articles)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date', ascending=False)
            
            if not os.path.exists('results'):
                os.makedirs('results')
            
            output_path = os.path.join('results', filename)
            df.to_excel(output_path, index=False)
            print(f"결과가 {output_path}에 저장되었습니다.")
            
        except Exception as e:
            print(f"엑셀 저장 중 에러: {e}")

    def close(self):
        """크롤러 종료"""
        if self.debug_mode:
            input("크롤러를 종료하려면 Enter 키를 눌러주세요...")
        self.driver.quit()