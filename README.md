# 서울시 생활인구 조회 웹 앱

행정동코드와 날짜를 입력하여 해당 날짜의 시간대별 총생활인구수 추이를 Chart.js로 시각화하는 웹 애플리케이션입니다.

## 프로젝트 구조

```
population/
├── index.html              # 메인 HTML 파일
├── styles.css              # 스타일시트
├── script.js               # JavaScript 로직
├── package.json            # 프로젝트 설정
├── rules.md                # 개발 가이드라인
├── 서울시_생활인구_2023.csv  # 데이터 파일
├── upload_csv.py           # CSV 업로드 스크립트 (참고용)
└── README.md               # 이 파일
```

## 기능

- 행정동코드와 날짜를 입력하여 데이터 조회
- Chart.js를 사용한 시간대별 총생활인구수 꺾은선 그래프 시각화
- 입력값 유효성 검사 및 경고 메시지 표시
- Supabase를 통한 데이터 저장 및 조회

## 시작하기

### 1. CSV 데이터 업로드

#### 방법 1: 변환된 CSV 파일 사용 (권장)

원본 CSV 파일의 한글 헤더를 영어로 변환한 파일을 사용하세요:

```bash
python convert_csv_headers.py
```

이 명령어를 실행하면 `서울시_생활인구_2023_english_headers.csv` 파일이 생성됩니다.

그 다음:
1. [Supabase 대시보드](https://supabase.com/dashboard) 접속
2. `population` 프로젝트 선택
3. Table Editor > `seoul_population` 테이블 선택
4. Insert > "Import Data from CSV" 클릭
5. `서울시_생활인구_2023_english_headers.csv` 파일 업로드

변환된 CSV 파일의 헤더는 다음과 같습니다:
- `date` (날짜)
- `time_hour` (시간대)
- `district_code` (행정동코드)
- `total_population` (총생활인구수)

#### 방법 2: 원본 CSV 파일 직접 업로드

원본 CSV 파일을 직접 업로드하려면 Supabase의 컬럼 매핑 기능을 사용해야 합니다. 하지만 이 방법은 헤더가 한글이어서 호환성 문제가 있을 수 있으므로 방법 1을 권장합니다.

### 2. 로컬 서버 실행

```bash
npm start
```

또는 브라우저에서 `index.html` 파일을 직접 열 수 있습니다.

## 사용 방법

1. 행정동코드를 입력합니다 (예: `1111061500`)
2. 날짜를 선택합니다 (예: `2023-08-26`)
3. "조회" 버튼을 클릭합니다
4. 시간대별 총생활인구수 추이가 그래프로 표시됩니다

## 기술 스택

- **HTML5**: 시맨틱 마크업
- **CSS3**: Flexbox, Grid를 사용한 모던 레이아웃
- **JavaScript (ES6+)**: 모던 JavaScript 기능 사용
- **Chart.js**: 데이터 시각화
- **Supabase**: 백엔드 데이터베이스

## 코드 가이드라인

이 프로젝트는 `rules.md`에 정의된 가이드라인을 따릅니다:

- 시맨틱 HTML5 요소 사용
- ES6+ 기능 (const/let, 화살표 함수)
- 모던 CSS (Flexbox, Grid)
- 접근성 모범 사례
- 관심사 분리 (HTML 구조, CSS 표현, JS 동작)

## 주요 파일 설명

### index.html
- 폼 구조 (행정동코드, 날짜 입력 필드)
- Chart.js 및 Supabase 클라이언트 라이브러리 포함
- 그래프를 표시할 canvas 요소

### script.js
- Supabase 클라이언트 초기화
- 데이터 조회 함수
- 입력값 유효성 검사
- Chart.js 그래프 생성 및 업데이트

### styles.css
- 반응형 레이아웃
- 폼 스타일링
- 알림 메시지 스타일
- 차트 컨테이너 스타일

## 데이터베이스 스키마

```sql
CREATE TABLE seoul_population (
    id BIGSERIAL PRIMARY KEY,
    date DATE NOT NULL,
    time_hour INTEGER NOT NULL CHECK (time_hour >= 0 AND time_hour <= 23),
    district_code BIGINT NOT NULL,
    total_population NUMERIC(12, 1) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## 환경 변수 설정

이 프로젝트는 Supabase 키를 환경 변수로 관리합니다.

### 로컬 개발

로컬 개발을 위해서는 `config.js` 파일을 생성해야 합니다:

1. `config.example.js`를 복사하여 `config.js` 생성:
   ```bash
   cp config.example.js config.js
   ```

2. `config.js` 파일을 열어 실제 Supabase URL과 Anon Key를 입력하세요.

### Vercel 배포

Vercel에 배포할 때는 환경 변수를 설정해야 합니다:

1. Vercel 대시보드 → 프로젝트 → Settings → Environment Variables
2. 다음 환경 변수 추가:
   - `SUPABASE_URL`: Supabase 프로젝트 URL (예: `https://gkklkjoatvbxfekuyvnx.supabase.co`)
   - `SUPABASE_ANON_KEY`: Supabase Anon Key

빌드 시 환경 변수로부터 `config.js` 파일이 자동 생성됩니다.

## 배포

이 프로젝트는 Vercel에 배포할 수 있습니다. 자세한 배포 가이드는 [DEPLOY.md](./DEPLOY.md)를 참고하세요.

### 빠른 배포

1. **Git 저장소에 푸시**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repository-url>
   git push -u origin main
   ```

2. **Vercel에 배포**
   - [Vercel 대시보드](https://vercel.com/dashboard)에서 프로젝트 Import
   - Git 저장소 연결
   - Framework Preset: "Other" 선택
   - **환경 변수 설정** (위의 "환경 변수 설정" 섹션 참고)
   - Deploy 클릭

자세한 내용은 [DEPLOY.md](./DEPLOY.md)를 참고하세요.

## 라이선스

MIT
