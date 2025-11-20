# Vercel 배포 가이드

이 프로젝트를 Vercel에 배포하는 방법을 안내합니다.

## 사전 준비

1. **Git 저장소 준비**
   - GitHub, GitLab, 또는 Bitbucket에 프로젝트를 푸시해야 합니다.
   - 아직 Git 저장소가 없다면 다음 명령어로 초기화하세요:

   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-repository-url>
   git push -u origin main
   ```

2. **Vercel 계정 생성**
   - [Vercel](https://vercel.com)에 가입하세요 (GitHub 계정으로 간편 가입 가능)

## 배포 방법

### 방법 1: Vercel 웹 대시보드 사용 (권장)

1. [Vercel 대시보드](https://vercel.com/dashboard)에 로그인
2. "Add New..." → "Project" 클릭
3. Git 저장소 선택 또는 Import
4. 프로젝트 설정:
   - **Framework Preset**: Other
   - **Root Directory**: `./` (기본값)
   - **Build Command**: `npm run build` (자동으로 설정됨)
   - **Output Directory**: `./` (기본값)
   - **Install Command**: (비워두기)
5. **환경 변수 설정** (아래 "환경 변수 설정" 섹션 참고)
6. "Deploy" 버튼 클릭
7. 배포 완료 후 제공되는 URL로 접속

### 방법 2: Vercel CLI 사용

1. **Vercel CLI 설치**
   ```bash
   npm install -g vercel
   ```

2. **로그인**
   ```bash
   vercel login
   ```

3. **프로젝트 배포**
   ```bash
   vercel
   ```

4. **프로덕션 배포**
   ```bash
   vercel --prod
   ```

## 환경 변수 설정 (필수)

이 프로젝트는 Supabase 키를 환경 변수로 관리합니다. **배포 전에 반드시 환경 변수를 설정해야 합니다.**

### Vercel 환경 변수 설정 방법

1. **Vercel 대시보드 접속**
   - 프로젝트 선택 → Settings → Environment Variables

2. **환경 변수 추가**
   다음 두 개의 환경 변수를 추가하세요:
   
   | 변수 이름 | 값 예시 | 설명 |
   |---------|--------|------|
   | `SUPABASE_URL` | `https://gkklkjoatvbxfekuyvnx.supabase.co` | Supabase 프로젝트 URL |
   | `SUPABASE_ANON_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` | Supabase Anon Key |
   
   - **Environment**: Production, Preview, Development 모두 선택 (또는 필요에 따라 선택)
   - "Save" 클릭

3. **Supabase 키 확인 방법**
   - [Supabase 대시보드](https://supabase.com/dashboard) 접속
   - 프로젝트 선택 → Settings → API
   - "Project URL"과 "anon public" 키를 복사

### 빌드 프로세스

빌드 시 `build-config.js` 스크립트가 실행되어:
- 환경 변수로부터 `config.js` 파일을 자동 생성
- 생성된 `config.js`는 배포에 포함됨

### 로컬 개발

로컬 개발을 위해서는 `config.js` 파일을 수동으로 생성해야 합니다:

```bash
# config.example.js를 복사
cp config.example.js config.js

# config.js 파일을 열어 실제 값 입력
```

## 커스텀 도메인 설정

1. Vercel 대시보드 → 프로젝트 → Settings → Domains
2. 원하는 도메인 입력
3. DNS 설정 안내에 따라 도메인을 연결

## 자동 배포

Git 저장소와 연결하면:
- `main` 브랜치에 푸시할 때마다 자동으로 프로덕션 배포
- 다른 브랜치에 푸시하면 프리뷰 배포

## 문제 해결

### 배포 실패 시

1. **빌드 로그 확인**: Vercel 대시보드에서 배포 로그 확인
2. **환경 변수 확인**: `SUPABASE_URL`과 `SUPABASE_ANON_KEY`가 올바르게 설정되었는지 확인
3. **로컬 테스트**: `npm run build`로 빌드가 성공하는지 확인
4. **파일 확인**: 모든 필요한 파일이 Git에 포함되어 있는지 확인

### Supabase 키를 인식하지 못하는 경우

다음 사항을 확인하세요:

1. **환경 변수 설정 확인**
   - Vercel 대시보드 → Settings → Environment Variables
   - `SUPABASE_URL`과 `SUPABASE_ANON_KEY`가 올바르게 설정되었는지 확인
   - 환경 변수 이름이 정확한지 확인 (대소문자 구분)

2. **빌드 로그 확인**
   - Vercel 배포 로그에서 `build-config.js` 실행 여부 확인
   - "✓ config.js generated successfully" 메시지 확인

3. **재배포**
   - 환경 변수 설정 후 "Redeploy" 클릭하여 재배포

### CORS 오류

Supabase에서 CORS 설정이 필요할 수 있습니다:
1. Supabase 대시보드 → Settings → API
2. "Allowed Origins"에 Vercel 도메인 추가

## 참고 자료

- [Vercel 공식 문서](https://vercel.com/docs)
- [정적 사이트 배포 가이드](https://vercel.com/docs/deployments/overview)

