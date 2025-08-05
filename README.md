# 🤖 Jambro Chatbot 제작 가이드 

Streamlit을 사용한 **Jambro Chatbot** 웹 애플리케이션입니다. Together AI의 다양한 모델을 활용하여 자연스러운 대화를 제공합니다.

## ✨ 주요 기능

- 🤖 **다양한 AI 모델 지원**
  - 한국어 특화: `exaone-3-5-32b-instruct`, `exaone-deep-32b`
  - 영어 특화: `Llama-3.3-70B-Instruct-Turbo-Free`
- 💬 **실시간 대화**
  - 자연스러운 채팅 인터페이스
  - 대화 히스토리 자동 저장
- 🔒 **보안 기능**
  - API 키 안전 관리 (세션 종료 시 자동 삭제)
  - 비밀번호 형태로 API 키 입력
- 🛠️ **편의 기능**
  - 대화 초기화
  - 대화 내용 텍스트 파일로 내보내기
  - API 연결 테스트
- 📱 **반응형 디자인**
  - 모바일/데스크톱 최적화
  - 직관적인 사이드바 설정

## 🚀 시작하기

### 1. API 키 발급
1. [Together AI 웹사이트](https://together.ai/) 방문
2. 계정 생성 또는 로그인
3. Dashboard → API Keys 섹션에서 새 API 키 생성

### 2. 앱 실행
```bash
# 의존성 설치
pip install -r requirements.txt

# 앱 실행
streamlit run together_ui.py
```

### 3. 사용법
1. 사이드바에서 API 키 입력
2. 원하는 AI 모델 선택
3. 질문을 입력하고 대화 시작!

## 🌐 배포

### Streamlit Cloud
- **장점:**
  - 🚀 **간편한 배포**: GitHub 저장소 연결만으로 자동 배포
  - 🔄 **자동 업데이트**: 코드 변경 시 자동으로 재배포
  - 💰 **무료 플랜**: 개인 프로젝트에 충분한 무료 사용량
  - 🛠️ **Streamlit 최적화**: Streamlit 앱에 특화된 환경
  - 📊 **내장 모니터링**: 앱 사용량 및 성능 추적

- **제약사항:**
  - 📦 **패키지 제한**: 일부 시스템 패키지 설치 불가
  - 💾 **메모리 제한**: 무료 플랜은 1GB RAM 제한
  - ⏱️ **실행 시간**: 30분 후 자동 슬립 모드
  - 🌍 **지역 제한**: 서버 위치 선택 불가
  - 🔒 **환경 변수**: Streamlit Cloud 대시보드에서만 설정 가능

### Vercel
- **장점:**
  - ⚡ **빠른 로딩**: 글로벌 CDN으로 전 세계 빠른 접속
  - 🔧 **유연한 설정**: `vercel.json`으로 상세 설정 가능
  - 🎨 **커스텀 도메인**: 자체 도메인 연결 지원
  - 📱 **모바일 최적화**: 자동 모바일 최적화
  - 🔄 **Git 연동**: GitHub/GitLab/Bitbucket 자동 배포

- **제약사항:**
  - 🐍 **Python 제한**: Serverless 환경으로 인한 제약
  - ⏰ **함수 타임아웃**: 10초 제한 (Hobby 플랜)
  - 💾 **메모리 제한**: 1024MB RAM 제한
  - 🔌 **포트 제한**: 특정 포트만 사용 가능
  - 🛠️ **추가 설정**: Streamlit 앱을 위한 별도 설정 필요

### 배포 추천

**Streamlit Cloud 추천:**
- 🎯 **빠른 프로토타이핑**이 필요한 경우
- 🧪 **AI/ML 프로젝트** 테스트용
- 👥 **팀 협업**이 중요한 경우
- 💰 **비용 효율성**을 우선하는 경우

**Vercel 추천:**
- 🌍 **글로벌 사용자**를 대상으로 하는 경우
- 🎨 **커스텀 도메인**이 필요한 경우
- ⚡ **빠른 로딩 속도**가 중요한 경우
- 🔧 **고급 설정**이 필요한 경우

## 📦 기술 스택

- **Frontend**: Streamlit 1.32.0
- **AI API**: Together AI
- **Language**: Python 3.8+
- **Deployment**: Streamlit Cloud / Vercel

## 🔧 설정 옵션

### AI 모델 선택
- **한국어 추천**: `exaone-3-5-32b-instruct`
- **영어 추천**: `Llama-3.3-70B-Instruct-Turbo-Free`

### API 설정
- 최대 토큰: 1000 (한글기준 1000자자)
- 온도: 0.7 (직설적 답변 (객관적) ~ 창의적 답변 (주관적))
- Top-p: 0.7 (일반적 답변 ~ 다양한 답변)
- 반복 패널티: 1.1 (1.0 : 답변 반복 패널티 없음, 1.1이상 : 반복 패널티 부여여)

## 📝 사용 팁

- **구체적인 질문**을 하면 더 정확한 답변을 받을 수 있어요
- **한국어 질문**에는 exaone 모델을, **영어 질문**에는 llama 모델을 추천합니다
- API 키는 **절대 공유하지 마세요** - 보안을 위해 세션 종료 시 자동 삭제됩니다

## 🤝 git으로 배포하기 

```powershell (관리자 권한)
# 1. 저장소 포크 후 클론
git clone https://github.com/your-username/repository-name.git
cd repository-name

# 2. 기능 브랜치 생성
git checkout -b feature/AmazingFeature

# 3. 변경사항 커밋
git add .
git commit -m "Add: 새로운 기능 추가"

# 4. 원격 저장소에 푸시
git push origin feature/AmazingFeature
```

### 다음 단계
1. GitHub에서 포크된 저장소로 이동
2. "Compare & pull request" 버튼 클릭
3. PR 설명 작성 후 제출

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

---

**Jambro Chatbot**과 함께 더 스마트한 대화를 시작해보세요! 🚀 