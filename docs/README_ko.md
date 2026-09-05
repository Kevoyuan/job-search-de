# 🇩🇪 job-search-de — 독일 전 직군 맞춤형 채용 공고 자동화 및 평가 파이프라인

<p align="center">
  <a href="../README.md"><b>English</b></a> •
  <a href="README_de.md"><b>Deutsch</b></a> •
  <a href="README_zh.md"><b>中文</b></a> •
  <a href="README_ja.md"><b>日本語</b></a> •
  <a href="README_ko.md"><b>한국어</b></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Agent%20Skill-Ready-blue.svg?style=flat-square" alt="Agent Skill" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="License" />
</p>

`job-search-de` 는 AI 에이전트(Antigravity, Claude Code, Cursor, OpenClaw, Gemini CLI 등)를 위한 지원자 중립형 독일 테크/AI 채용 파이프라인 자동화 스킬입니다.

---

## 왜 job-search-de 인가

| 비교 항목 | 기존 채용 플랫폼 (LinkedIn / StepStone / Indeed) | `job-search-de` 파이프라인 |
|---|---|---|
| **공고 최신성 및 신뢰도** | 30%~50%가 마감된 유령 공고 또는 헤드헌터 중복 게시물 | **100% 실시간 검증 완료** (기업 공식 ATS API 직수집 + Schema.org 실시간 검증) |
| **개인정보 보호** | 이력서 데이터가 외부 클라우드 데이터베이스에 업로드됨 | **100% 로컬 프라이빗** (데이터는 로컬 `<workdir>/.job-search/` 에만 보관) |
| **매칭 스코어링 신뢰도** | 단순 키워드 매칭으로 인한 오매칭 빈번 | **2단계 근거 기반 스코어링** (실제 이력서 팩트만을 인용, 허위 매칭 차단) |
| **지원 및 파이프라인 관리** | 번거로운 수동 엑셀 정리 및 북마크 분실 | **4테마 반응형 워크벤치** (칸반 보드, 다차원 필터, 단축키, 원클릭 피치 복사) |
| **AI 에이전트 연동** | 최신 AI 워크플로우와 단절됨 | **네이티브 Agent Skill 지원** (Antigravity, Claude Code, Cursor, OpenClaw 완벽 호환) |

---

## 데모 및 인터페이스

### 4가지 디자인 테마 실시간 전환 (0 토큰 순수 CSS)
> **Notion Craft (감성 문서)**, **Linear Obsidian (다크 모드)**, **Bauhaus Grid (바우하우스 미니멀)**, **Bento Quartz (모던 글래스)** 4가지 테마를 0 토큰으로 실시간 전환. 숫자 키 <kbd>1</kbd> / <kbd>2</kbd> / <kbd>3</kbd> / <kbd>4</kbd> 로 즉시 전환.

![Workbench 테마 전환 데모](images/theme-switcher.gif)

---

### 1. 인터랙티브 테이블 데이터베이스 뷰
> 실시간 지원 현황 추적, 다차원 조합 필터, 공고 신선도 확인, 정밀 적합도 점수 산출.

![Workbench 테이블 뷰](images/workbench-table.png)

---

### 2. 채용 파이프라인 칸반 뷰
> 드래그 앤 드롭 지원 라이프사이클 관리 (지원 대기, 지원 완료, 면접 진행, 오퍼 수령, 아카이브).

![Workbench 칸반 뷰](images/workbench-kanban.png)

---

### 3. 로컬 지원자 프로필 및 규칙 설정 드로어
> 프라이버시 중심 아키텍처: 개인 이력 및 채용 선호도는 로컬 `.job-search/` 에만 안전하게 보관.

![Workbench 설정 드로어](images/workbench-config-drawer.png)

---

### 4. 종합 시장 분석 리포트
> 프랑크푸르트, 뮌헨, 베를린, 독일 원격 등 지역별 심층 JD 매칭 분석 리포트 자동 생성.

![시장 분석 리포트](images/report-overview.png)

---

## 주요 기능 및 특징

- **개인정보 보호 및 데이터 분리**：Skill 로직과 지원자 데이터의 엄격한 분리. 개인 이력 및 조건 설정은 로컬 `<workdir>/.job-search/` 에만 보관.
- **4가지 고품격 비주얼 테마**：**Notion Craft**, **Linear Obsidian (다크 모드)**, **Bauhaus Grid**, **Bento Quartz** 를 0 토큰으로 실시간 전환.
- **강력한 키보드 단축키 내비게이션**：<kbd>J</kbd>/<kbd>K</kbd> 이동, <kbd>Enter</kbd> 상세 펼치기, <kbd>O</kbd> 공식 채용공고 이동, <kbd>/</kbd> 빠른 검색, <kbd>1</kbd>/<kbd>2</kbd>/<kbd>3</kbd>/<kbd>4</kbd> 테마 전환.
- **원클릭 지원 맞춤형 피치(Pitch) 복사**：검증된 JD 매칭 근거를 기반으로 완성도 높은 커버레터 도입부를 즉시 생성하여 클립보드에 복사.
- **빠른 프리셋 필터 칩**：`Fit ≥ 85`, `프랑크푸르트 지역`, `100% 원격`, `영어 전용`, `지원 대기 공고` 1초 원클릭 필터링.
- **ATS 공식 API 직접 연동**：Greenhouse, Lever, Ashby, SmartRecruiters, Personio, Workable 공식 API로부터 최신 공고 직수집.
- **자동 실시간 유효성 검증 파이프라인**：URL 생존 확인, HTTP 상태 코드 및 Schema.org JSON-LD 메타데이터 자동 파싱.
- **2단계 근거 기반 정밀 스코어링**：
  - **Stage 1 (빠른 스크리닝)**：필수 자격 미달 및 경력 요건 즉시 필터링.
  - **Stage 2 (심층 JD-이력 매칭)**：실제 후보자 근거 사실만을 인용하여 허위 매칭 완전 차단.
- **인터랙티브 워크벤치**：칸반 보드, 테이블 뷰, Notion 양방향 동기화를 지원하는 경량 HTML/JS UI.
- **런타임 버전 확인 및 자동 업데이트**：GitHub 최신 릴리스를 자동 감지하여 상태 뱃지(`v1.1.1`) 표시.

---

### 파이프라인 워크플로우

```text
               지원자 제출 자료 (이력서, 포트폴리오, 경력 기술서)
                                      │
                                      ▼
                      [1. 온보딩 및 프로필 사실 추출]
                                      │ (생성: .job-search/profile.md & preferences.md)
                                      ▼
                        [2. 멀티 채널 채용공고 수집]
                     기업 공식 ATS 직수집 + 타겟 지역 검색
                                      │
                                      ▼
                      [3. 데이터 정제 및 실시간 유효성 검증]
                    Schema.org JSON-LD + HTTP 상태 코드 체크
                                      │
                                      ▼
                      [4. 2단계 근거 기반 정밀 적합도 평가]
                    필수 조건 필터링 ➔ 이력서 팩트 일대일 매칭
                                      │
                                      ▼
                      [5. 최종 분석 리포트 및 워크벤치 제공]
              시장 분석 리포트 + 인터랙티브 HTML 워크벤치 + Notion
```

---

## 시스템 아키텍처

> 🌐 **인터랙티브 아키텍처 다이어그램**: [**`architecture.html`**](architecture.html) ([Archify](https://github.com/tt-a1i/archify) 쇼케이스 표준 적용. 다크/라이트 테마 전환, 데이터 경로 추적, 가이드 챕터, 전체 화면 프레젠테이션, 벡터 파일 내보내기 지원).

![job-search-de 시스템 아키텍처](images/architecture.png)

`job-search-de`는 **완전 격리형·프라이버시 우선의 5단계 파이프라인 아키텍처**를 채택합니다:

1. **로컬 기밀 샌드박스 (`.job-search/`)**: 후보자 중립 설계. 모든 이력서와 포트폴리오는 로컬의 `.job-search/profile.md`, `preferences.md`, `settings.ini`에만 저장되며 외부 클라우드로 전송되지 않습니다.
2. **공식 ATS 다채널 수집 엔진**: Greenhouse, Ashby, Lever, SmartRecruiters, Personio, Workable 등의 공식 ATS 엔드포인트에 직접 연결하여 만료 공고 및 중개 플랫폼 노이즈를 완벽 차단.
3. **구조화 검증 및 정규화 파이프라인**: HTTP 상태 코드 및 Schema.org JSON-LD 메타데이터(`datePosted`, `validThrough`, 채용 상태)를 실시간 분석하여 공고 신선도를 엄격히 분류.
4. **2단계 정밀 근거 스코어링 코어**: 신뢰할 수 없는 외부 JD로부터의 프롬프트 주입 공격을 차단하고, `profile.md`의 검증된 팩트만을 인용하여 AI 환각(Hallucination) 점수를 원천 방지.
5. **다양한 테마 워크벤치 및 리포트 전달**: 지역별 종합 리포트, Notion 양방향 동기화, 4가지 전용 테마를 갖춘 독립형 클라이언트 워크벤치(File System Access API를 통한 직접 저장 지원)를 제공.

---

## 디렉터리 구조

```text
job-search-de/
├── SKILL.md                  # Agent Skill 진입점 및 운영 규칙
├── README.md                 # 메인 프로젝트 문서 (영어)
├── VERSION                   # 시맨틱 버전 정의 (예: 1.1.1)
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
│   ├── bump_version.py       # 버전 자동 업데이트 스크립트
│   ├── check_update.py       # 업스트림 버전 확인 스크립트
│   ├── update_skill.sh       # 원클릭 스킬 업데이트 스크립트
│   ├── download.sh           # ATS API 배치 다운로더
│   ├── parse_ats.py          # ATS 데이터 파서 및 정규화
│   ├── verify_urls.py        # Schema.org JSON-LD 메타데이터 추출
│   ├── verify.sh             # 채용 URL 및 메타데이터 유효성 검증
│   ├── build_workbench.py    # 워크벤치 HTML 빌더
│   ├── test_ats_universal.py # ATS 파서 회귀 테스트 슈트
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
    ├── architecture.html     # 인터랙티브 시스템 아키텍처 다이어그램 (Archify)
    ├── architecture.json     # 아키텍처 정의 사양서
    └── images/               # 데모 스크린샷, 아키텍처 다이어그램 및 애니메이션 GIF
```

---

## 빠른 시작

### 1. Skill 설치
```bash
npx skills add Kevoyuan/job-search-de -g
```

### 2. 이력서 배치
작업 폴더에 이력서 파일(`resume.pdf`, `CV.md` 등)을 넣습니다.

### 3. AI 에이전트에 지시
AI 어시스턴트(Antigravity, Claude Code, Cursor, OpenClaw)에 요청하세요:

> **"내 이력서에 맞는 프랑크푸르트, 뮌헨 또는 독일 전역 원격 AI 엔지니어 채용 공고를 찾아줘."**

---

## 지원 명령어 목록

| 명령어 | 설명 |
|---|---|
| `/refresh` | **전체 검색 갱신**: 최신 ATS 공고 재수집, 링크 유효성 검증, 스코어링 및 워크벤치 갱신. |
| `/update-skill` | **Skill 자동 업데이트**: GitHub 최신 버전 코드를 자동으로 가져옵니다. |
| `/match <url / jd>` | **단일 공고 즉시 평가**: 특정 공고 URL 또는 JD 텍스트를 프로필과 즉시 매칭 평가. |
| `/tailor <id / url>` | **맞춤 이력서 및 커버레터 생성**: 검증된 근거 기반 독일식 지원 서류 생성. |
| `/sync` | **Notion 동기화**: Notion 채용 지원 현황 데이터베이스와 양방향 동기화. |
| `/digest` | **데일리 다이제스트**: 최근 24~48시간 내 신규 고적합도 공고 TOP 5 요약. |

---

## 설정 및 개인정보 관리

모든 개인 데이터와 조건 설정은 로컬 `.job-search/` 디렉터리에만 안전하게 보관됩니다:

<details>
<summary><b>설정 예시 <code>.job-search/preferences.md</code> 및 <code>settings.ini</code></b></summary>

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

## 자주 묻는 질문 (FAQ)

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

## 라이선스

[MIT License](LICENSE) 에 따라 배포됩니다.
