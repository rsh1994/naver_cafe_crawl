# 네이버 카페 크롤러

네이버 카페의 특정 게시판의 게시글을 수집하는 크롤러입니다. 지정된 기간 동안의 게시글 제목, 내용, 작성일, 조회수를 수집하여 엑셀 파일로 저장합니다.

## 주요 기능

- 네이버 카페 게시판 크롤링
- 공지사항 제외 기능
- 기간 설정을 통한 선택적 수집
- 게시글 제목, 내용, 작성일, 조회수 수집
- 엑셀 파일로 결과 저장

## 필요 사항

- Python 3.7 이상
- Chrome 브라우저

## 설치 방법

1. 저장소 클론
```bash
git clone [repository_url]
cd [repository_name]
```

2. 가상환경 생성 및 활성화
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

3. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

## 설정 방법

1. `.config.example` 파일을 `.config`로 복사
```bash
cp .config.example .config
```

2. `.config` 파일 수정
```ini
CAFE_NAME=카페이름
CLUB_ID=카페ID
MENU_ID=게시판ID
PERIOD_DAYS=1
NAVER_ID=네이버아이디
NAVER_PASSWORD=네이버비밀번호
```

### 설정값 설명
- `CAFE_NAME`: 카페 URL의 도메인 이름 (예: joonggonara)
- `CLUB_ID`: 카페의 고유 ID
- `MENU_ID`: 게시판의 고유 ID
- `PERIOD_DAYS`: 크롤링할 기간 (일 단위)
- `NAVER_ID`: 네이버 로그인 아이디
- `NAVER_PASSWORD`: 네이버 로그인 비밀번호

### 카페/게시판 ID 찾는 방법
1. 해당 게시판 페이지 접속
2. URL 확인:
   - `clubid=숫자`: 카페 ID
   - `menuid=숫자`: 게시판 ID

## 사용 방법

1. 프로그램 실행
```bash
python main.py
```

2. 결과 확인
- 크롤링된 데이터는 `results` 폴더에 엑셀 파일로 저장됩니다.
- 파일명 형식: `naver_cafe_articles_YYYYMMDD_HHMMSS.xlsx`

## 주의사항

- 네이버 카페 회원 로그인이 필요합니다.
- 해당 게시판의 읽기 권한이 있어야 합니다.
- 과도한 크롤링은 서버에 부담을 줄 수 있으니 적절한 간격을 두고 사용해주세요.
- 크롤링한 데이터의 저작권과 개인정보 보호에 유의해주세요.

## 파일 구조

```
.
├── README.md
├── requirements.txt
├── .config.example
├── .gitignore
├── main.py
├── config.py
├── naver_cafe_crawler.py
└── results/
    └── naver_cafe_articles_[timestamp].xlsx
```

## requirements.txt

```
selenium
beautifulsoup4
pandas
chromedriver-autoinstaller
python-dotenv
openpyxl
```

## 라이선스

MIT License

## 문의사항

이슈를 통해 문의해주세요.