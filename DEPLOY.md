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
   - **Build Command**: (비워두기 - 정적 사이트이므로 빌드 불필요)
   - **Output Directory**: `./` (기본값)
   - **Install Command**: (비워두기)
5. "Deploy" 버튼 클릭
6. 배포 완료 후 제공되는 URL로 접속

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

## 환경 변수 설정 (필요시)

현재 프로젝트는 Supabase URL과 API 키가 코드에 하드코딩되어 있습니다. 보안을 위해 환경 변수로 관리하는 것을 권장합니다:

1. Vercel 대시보드 → 프로젝트 → Settings → Environment Variables
2. 다음 환경 변수 추가:
   - `VITE_SUPABASE_URL` (또는 `NEXT_PUBLIC_SUPABASE_URL`)
   - `VITE_SUPABASE_ANON_KEY` (또는 `NEXT_PUBLIC_SUPABASE_ANON_KEY`)

그 후 `script.js`에서 환경 변수를 사용하도록 수정:
```javascript
const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || 'https://gkklkjoatvbxfekuyvnx.supabase.co';
const SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || 'your-key-here';
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
2. **로컬 테스트**: `npm start`로 로컬에서 정상 작동 확인
3. **파일 확인**: 모든 필요한 파일이 Git에 포함되어 있는지 확인

### CORS 오류

Supabase에서 CORS 설정이 필요할 수 있습니다:
1. Supabase 대시보드 → Settings → API
2. "Allowed Origins"에 Vercel 도메인 추가

## 참고 자료

- [Vercel 공식 문서](https://vercel.com/docs)
- [정적 사이트 배포 가이드](https://vercel.com/docs/deployments/overview)

