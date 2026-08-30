# 🇩🇪 job-search-de — 독일 AI / 테크 채용 탐색 및 근거 기반 평가 파이프라인

<p align="center">
  <a href="../README.md"><b>English</b></a> •
  <a href="README_de.md"><b>Deutsch</b></a> •
  <a href="README_zh.md"><b>中文</b></a> •
  <a href="README_ja.md"><b>日本語</b></a> •
  <a href="README_ko.md"><b>한국어</b></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Agent%20Skill-지원됨-blue.svg?style=flat-square" alt="Agent Skill" />
  <img src="https://img.shields.io/badge/타겟%20시장-독일%20AI%2FTech-emerald.svg?style=flat-square" alt="Target Market" />
  <img src="https://img.shields.io/badge/평가%20방식-근거%20기반-purple.svg?style=flat-square" alt="Scoring Mode" />
  <img src="https://img.shields.io/badge/라이선스-MIT-green.svg?style=flat-square" alt="License" />
</p>

독일 내 AI 및 테크 분야 채용 공고를 자동으로 탐색, 검증, 2단계 근거 기반 평가, 리포트 생성 및 워크벤치 관리를 수행하는 AI 에이전트 전용 스킬입니다.

---

## 🥊 왜 기존 채용 플랫폼 대신 `job-search-de` 인가

| 비교 항목 | 기존 채용 플랫폼 (LinkedIn / StepStone / Indeed) | 🇩🇪 `job-search-de` 파이프라인 |
|---|---|---|
| **공고 최신성 및 신뢰도** | 30%~50%가 마감된 유령 공고 또는 헤드헌터 중복 게시물 | **100% 실시간 검증 완료** (기업 공식 ATS API 직수집 + Schema.org 실시간 검증) |
| **개인정보 보호** | 이력서 데이터가 외부 클라우드 데이터베이스에 업로드됨 | **100% 로컬 프라이빗** (데이터는 로컬 `<workdir>/.job-search/` 에만 보관) |
| **매칭 스코어링 신뢰도** | 단순 키워드 매칭으로 인한 오매칭 빈번 | **2단계 근거 기반 스코어링** (실제 이력서 팩트만을 인용, 허위 매칭 차단) |
| **지원 및 파이프라인 관리** | 번거로운 수동 엑셀 정리 및 북마크 분실 | **4테마 반응형 워크벤치** (칸반 보드, 다차원 필터, 단축키, 원클릭 피치 복사) |
| **AI 에이전트 연동** | 최신 AI 워크플로우와 단절됨 | **네이티브 Agent Skill 지원** (Antigravity, Claude Code, Cursor, OpenClaw 완벽 호환) |

---

## 📸 데모 및 인터페이스

### 🎨 4가지 맞춤형 테마 실시간 전환 (0 토큰 순수 CSS)
> **Notion Craft**, **Linear Obsidian**, **Bauhaus Grid**, **Bento Quartz** 4가지 테마 실시간 전환.

![Workbench 테마 전환 데모](images/theme-switcher.gif)

---

### 1. 노션(Notion) 스타일 인터랙티브 워크벤치 (테이블 뷰)
> 실시간 지원 상태 추적, 다차원 필터링, 공고 신선도 확인, 정밀 적합도 점수 산출.

![워크벤치 테이블 뷰](images/workbench-table.png)

---

### 2. 채용 지원 파이프라인 칸반(Kanban) 보드
> 지원 진행 단계별 라이프사이클 관리 (지원 예정, 지원 완료, 면접 진행 중, 최종 합격, 보관).

![워크벤치 칸반 뷰](images/workbench-kanban.png)

---

### 3. 로컬 지원자 프로필 및 환경설정 드로어
> 지원자 중립 및 프라이버시 보호 아키텍처: 개인 이력, 필수 제약 조건, 희망 근무지 설정은 작업 디렉터리의 `.job-search/`에 안전하게 보관됩니다.

![환경설정 드로어](images/workbench-config-drawer.png)

---

### 4. 독일 AI 채용 시장 분석 종합 리포트
> 프랑크푸르트, 뮌헨, 베를린, 전독일 원격(Remote) 등 지역별 공고 분석과 직무 기술서(JD)와 지원자 이력 간의 정밀 근거 매칭.

![분석 리포트](images/report-overview.png)

---

## 🌟 주요 기능

- 🎯 **프라이버시 우선 & 지원자 중립 구조**: 스킬 엔진과 개인 데이터가 분리되어 있으며, 지원자 정보는 로컬의 `<workdir>/.job-search/`에만 저장됩니다.
- 🔍 **주요 ATS 직접 연동**: Greenhouse, Lever, Ashby, SmartRecruiters, Personio, Workable 등의 채용 API에서 직접 공고를 수집하여 불필요한 중개 사이트의 오류를 방지합니다.
- ⚡ **자동 검증 및 공고 신선도 확인**: 실시간 URL 상태 확인, HTTP 응답 코드 및 Schema.org JSON-LD 메타데이터(`datePosted`, `validThrough`) 자동 추출.
- 📊 **정밀한 2단계 근거 기반 매칭 점수**:
  - **Stage 1 (빠른 스크리닝)**: 직급, 제외 조건, 필수 제약 조건 기반 필터링.
  - **Stage 2 (심층 매칭)**: 필수 요구조건과 우대사항을 분리하여 지원자 프로필의 실제 사실만을 인용하여 객관적 점수 산출.
- 🗂️ **인터랙티브 워크벤치 UI**: 모던 HTML/JS 기반 테이블/칸반 뷰, 필터 프리셋, 노션 데이터베이스 상태 동기화 지원.
- 📑 **다국어 분석 리포트 생성**: 지역별, 스택별로 정리된 구조화된 Markdown 및 HTML 리포트 자동 생성.

---

## 🔄 워크플로우

```text
             지원자 서류 (이력서 / LinkedIn / 포트폴리오)
                            │
                            ▼
               [1. 온보딩 및 프로필 생성]
                            │ (.job-search/profile.md 및 preferences.md 생성)
                            ▼
                 [2. 다채널 채용 공고 탐색]
              ATS 직접 수집 ＋ 지역별 보완 검색
                            │
                            ▼
                 [3. 데이터 정규화 및 검증]
             Schema.org JSON-LD ＋ HTTP 상태 검증
                            │
                            ▼
               [4. 2단계 근거 기반 적합도 평가]
              기본 필터링 ➔ JD 요구사항 대조 분석
                            │
                            ▼
                 [5. 리포트 생성 및 전달]
         경영진 리포트 ＋ 인터랙티브 워크벤치 ＋ 노션 동기화
```

---

## 📁 디렉터리 구조

```text
job-search-de/
├── SKILL.md                  # Agent Skill 진입점 및 운영 규칙
├── README.md                 # 메인 프로젝트 문서 (영어)
├── VERSION                   # 시맨틱 버전 정의 (예: 1.1.0)
├── assets/
│   └── config-template/      # 설정 템플릿
│       ├── profile.md        # 검증된 지원자 프로필 템플릿
│       ├── preferences.md    # 채용 선호도 및 타겟 제약 조건
│       └── settings.ini      # 스코어링 임계값 및 검색 윈도우
├── configs/
│   ├── boards.txt            # 모니터링 대상 ATS 기업 목록
│   ├── keywords.txt          # 검색 키워드 매트릭스
│   └── profile.md            # 참조 프로필 사양
├── references/
│   ├── configuration.md      # 설정 계약 사양서
│   ├── onboarding.md         # 지원자 온보딩 가이드
│   ├── resume-parser.md      # 이력서 근거 추출 규격
│   ├── scoring.md            # 2단계 근거 기반 평가 기준
│   └── workbench.md          # 워크벤치 통합 및 테마 규격
├── scripts/
│   ├── bump_version.py       # Auto semantic version bumper
│   ├── check_update.py       # 업스트림 버전 확인 스크립트
│   ├── update_skill.sh       # 원클릭 스킬 업데이트 스크립트
│   ├── download.sh           # ATS API 배치 다운로더
│   ├── parse_ats.py          # ATS 데이터 파서 및 정규화
│   ├── verify.sh             # 채용 URL 및 메타데이터 유효성 검증
│   ├── init_config.py        # 로컬 설정 템플릿 초기화
│   ├── build_html.sh         # 워크벤치 패키징 빌드 스크립트
│   └── fix_html.py           # HTML 리포트 데이터 인젝터
├── templates/
│   ├── agent_prompt_common.md# 표준화된 프롬프트 블록
│   ├── report_skeleton.md    # 경영진 리포트 템플릿
│   └── search_queries.md     # 검색 쿼리 합성 매트릭스
└── docs/
    ├── README_zh.md          # 중국어 문서 (中文)
    ├── README_de.md          # 독일어 문서 (Deutsch)
    ├── README_ja.md          # 일본어 문서 (日本語)
    ├── README_ko.md          # 한국어 문서 (현재 파일)
    └── images/               # 데모 스크린샷 및 애니메이션 GIF
```

---

## 🚀 빠른 시작 (3단계 초간편 워크플로우)

### 1. 스킬 설치
```bash
npx skills add Kevoyuan/job-search-de -g
```

### 2. 이력서 파일 배치
작업 폴더에 이력서 또는 프로필 파일(`resume.pdf`, `CV.md`, LinkedIn 내보내기 파일 등)을 넣어둡니다.

### 3. AI 에이전트에게 지시
AI 어시스턴트(Antigravity, Claude Code, Cursor 등)에게 자연어로 명령하세요:

> **"내 이력서에 맞는 독일(프랑크푸르트, 뮌헨 또는 원격 근무) AI/ML 엔지니어 채용 공고를 찾아서 분석 리포트와 워크벤치를 만들어줘."**

AI 에이전트가 백그라운드에서 모든 파이프라인을 자동 수행합니다:
1. 📄 **프로필 자동 생성**: 이력서를 파싱하여 로컬 `.job-search/profile.md` 작성.
2. 🔍 **실시간 공고 탐색**: Greenhouse, Lever, Ashby, Personio 등 공식 ATS에서 직접 수집.
3. ⚡ **유효성 검증**: URL 링크 상태 및 Schema.org 게시 날짜 실시간 확인.
4. 📊 **근거 기반 평가**: 직무 요구사항과 이력서 사실을 대조하여 정밀 적합도 산출.
5. 🗂️ **결과물 생성**: 종합 분석 리포트 발행 및 인터랙티브 HTML 워크벤치 자동 업데이트.

<details>
<summary><b>🛠️ 개발자용 수동 CLI 명령어 (선택 사항)</b></summary>

스크립트를 직접 실행하려는 경우:

```bash
# 설정 템플릿 초기화
python3 ~/.agents/skills/job-search-de/scripts/init_config.py --workdir .

# ATS 채용 공고 다운로드 및 파싱
bash ~/.agents/skills/job-search-de/scripts/download.sh --workdir .
python3 ~/.agents/skills/job-search-de/scripts/parse_ats.py --today $(date +%Y-%m-%d) --workdir .

# URL 유효성 검증
bash ~/.agents/skills/job-search-de/scripts/verify.sh urls.txt
```
</details>

---

## ⚡ 주요 명령어 (Commands)

AI 에이전트 대화창에서 다음 명령어를 직접 사용할 수 있습니다:

| 명령어 | 기능 설명 |
|---|---|
| `/refresh` | **신규 공고 전체 새로고침**: ATS 일괄 수집, 링크 검증, 2단계 적합도 평가 및 워크벤치/리포트 자동 업데이트. |
| `/update-skill` | **스킬 자동 업데이트**: GitHub 최신 버전을 확인하고 `npx skills update job-search-de -g` 실행. |
| `/match <URL 또는 JD>` | **단일 공고 즉시 매칭**: 임의의 채용 링크나 JD 텍스트를 입력받아 프로필 근거 기반 즉시 평가. |
| `/tailor <ID 또는 URL>` | **맞춤형 이력서 & 커버레터 생성**: 실제 검증된 경력을 기반으로 해당 직무 맞춤 이력서 불릿포인트 및 독일어 자기소개서(Anschreiben) 작성. |
| `/sync` | **노션 상태 동기화**: 로컬 워크벤치와 노션(Notion) 채용 데이터베이스 간 지원 상태 양방향 동기화. |
| `/digest` | **60초 일일 브리핑**: 최근 24~48시간 동안 새로 등록된 최상위 매칭 공고 Top 5 요약. |

---

## ⚙️ 프라이빗 설정 관리 (`.job-search/`)

모든 지원자 개인 데이터와 조건 설정은 로컬 `.job-search/` 디렉터리에만 안전하게 보관됩니다:

<details>
<summary><b>📂 설정 예시 <code>.job-search/preferences.md</code> 및 <code>settings.ini</code></b></summary>

```markdown
# 타겟 채용 선호도 (.job-search/preferences.md)

- **타겟 직무:** Senior AI Engineer, Machine Learning Engineer
- **타겟 지역:** 프랑크푸르트 지역, 독일 전역 (100% 원격)
- **최소 적합도 점수:** 75
- **어학 요건:** 비즈니스 영어 (기초 독일어)
```

```ini
# 검색 및 전달 설정 (.job-search/settings.ini)
[scoring]
fit_threshold = 75
require_direct_ats = true

[delivery]
workbench_language = ko
auto_open_browser = true
```
</details>

---

## ❓ 자주 묻는 질문 (FAQ)

<details>
<summary><b>1. 유료 LinkedIn API나 별도 스크래핑 키가 필요한가요?</b></summary>

**전혀 필요하지 않습니다.** 채용 기업이 공식적으로 운영하는 공개 ATS 엔드포인트(Greenhouse, Lever, Ashby, SmartRecruiters, Personio, Workable)에 직접 연결합니다.
</details>

<details>
<summary><b>2. 제 이력서나 개인정보가 외부 서버로 전송되나요?</b></summary>

**절대 전송되지 않습니다.** 이력서 파싱, 사실 근거 매칭, 워크벤치 생성 등 모든 과정이 사용자의 로컬 에이전트 세션 내에서만 이루어집니다.
</details>

<details>
<summary><b>3. 타겟 도시나 검색 조건을 맞춤형으로 변경할 수 있나요?</b></summary>

**가능합니다.** 로컬의 `.job-search/preferences.md` 또는 `.job-search/settings.ini` 파일만 수정하시면 됩니다.
</details>

---

## 📄 라이선스

[MIT 라이선스](LICENSE)에 따라 배포됩니다.
