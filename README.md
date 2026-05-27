# Ahee Career Code

> 홀랜드 RIASEC 이론 기반 Ahee 자체 커리어 검사 서비스
> 학교 B2B + 개인 B2C 듀얼 마켓 타깃

![status](https://img.shields.io/badge/status-prototype_v0.3-FF3366)
![tone](https://img.shields.io/badge/tone-hyundai_card_×_ahee_magenta-FF3366)
![lang](https://img.shields.io/badge/lang-ko_KR-0A0A0A)

---

## 🎯 무엇을 만들고 있나

같은 RIASEC 엔진 위에 **3가지 다른 제품**:

| 제품 | 형태 | 용도 |
|---|---|---|
| **v0.3 Quick Test** | 24문항 · 3-5분 | SNS 바이럴 입구 · 직무박람회 부스 |
| **v0.2 Full Test** | 100문항 · 10-15분 | 학교 정규 진로 프로그램 |
| **v0.3 Persona Card** | A6 양면 PDF | 인쇄 배포 · 디지털 공유 (14종) |
| **v0.2 Career Report** | A4 3페이지 PDF | 자소서 첨부 · 진로 상담 |

자세한 사용자 흐름은 → [docs/ux_flow.html](docs/ux_flow.html)

---

## 🌐 테스트 배포 + 데이터 수집

**무료 셋업 30분 안에 가능 →** [`deploy/README.md`](deploy/README.md)

```
Vercel 정적 호스팅  +  Google Apps Script 백엔드  +  Google Sheets 수집
       (무료)              (무료, 일 2만 호출)         (무료, 즉시 확인)
```

검사 결과는 익명으로 시트에 저장됩니다 (이름·연락처 미수집). 학생 30명만 모이면 페르소나 분포·문항 이탈률 즉시 분석 가능.

---

## 🚀 빠른 시작

### 환경 요구사항
- Python 3.10+
- Node.js 18+ (검사 페이지 HTML 미리보기용, optional)
- Playwright (PDF 생성용)

### 설치
```bash
# Python 의존성
pip install playwright --break-system-packages
playwright install chromium

# 첫 실행 시 chromium 다운로드 (~150MB)
```

### 사용
```bash
# 1) 검사 페이지 브라우저로 열기 (정적 HTML, 즉시 동작)
open public/v03_test.html   # macOS
xdg-open public/v03_test.html   # Linux
# 또는 그냥 파일 더블클릭

# 2) 카드 PDF 생성 (특정 페르소나)
python scripts/build_card.py --persona E2 --theme dark

# 3) 14개 페르소나 × DARK/LIGHT 전부 일괄 생성 (28개 PDF)
python scripts/build_card.py --all

# 4) v0.2 정규 결과지 PDF 생성 (E2 샘플)
python scripts/build_report.py
```

---

## 📁 디렉토리 구조

```
ahee-career-code/
├── README.md            ← 이 파일
├── CLAUDE.md            ← Claude Code용 작업 가이드 (반드시 먼저 읽기)
├── ROADMAP.md           ← 다음 작업 목록 (현재 v0.3 완료 시점)
│
├── data/                ← 검사 데이터 (JSON)
│   ├── questions_v02.json   ← 100문항 + 22 facet 정의
│   ├── questions_v03.json   ← 24문항
│   └── personas.json        ← 14개 페르소나 + 매칭 규칙
│
├── src/scoring/         ← 채점 알고리즘
│   ├── scoring_v02.js   ← 100문항 채점 (6코드 + facet)
│   └── scoring_v03.js   ← 24문항 채점 + 페르소나 매칭
│
├── public/              ← 정적 HTML (배포 가능)
│   ├── v02_test.html    ← v0.2 인터랙티브 검사
│   └── v03_test.html    ← v0.3 인터랙티브 검사
│
├── templates/           ← PDF 생성용 HTML 템플릿
│   ├── card_dark.html   ← v0.3 카드 (다크 톤, A6)
│   ├── card_light.html  ← v0.3 카드 (라이트, 인쇄용)
│   └── report.html      ← v0.2 결과지 (A4 3페이지)
│
├── scripts/             ← 빌드/유틸 스크립트
│   ├── build_card.py    ← 14개 페르소나 카드 일괄 생성
│   └── build_report.py  ← 정규 결과지 PDF 생성
│
├── docs/                ← 문서·시각화
│   ├── ux_flow.html     ← 전체 UX 흐름도
│   └── samples/         ← 샘플 PDF
│
└── output/              ← 생성된 PDF (gitignore 권장)
    ├── cards/
    └── reports/
```

---

## 🎨 디자인 시스템

**"현대카드 × Ahee 마젠타"** 톤 — 화이트 베이스 + 미니멀

| 요소 | 값 |
|---|---|
| 메인 액센트 | `#FF3366` (Ahee 마젠타) |
| 잉크 | `#0A0A0A` |
| 배경 | `#FAFAF8` |
| 라인 | `#ECECEC` |
| 영문 헤드 | `Inter Tight 800/900` |
| 한글 본문 | `Pretendard 500/700/800` |
| 라벨·메타 | `JetBrains Mono` |

**시그니처 요소:**
- 헤드라인 끝에 마젠타 마침표 (`<span style="color:#FF3366">.</span>`)
- 거대 워터마크 (`opacity:0.04`)
- mono 라벨 + `●` 닷 구분
- 우측 상단 document no.

---

## 📊 현재 상태

| 영역 | 상태 |
|---|---|
| ✅ v0.3 검사 시스템 (24문항) | 동작 |
| ✅ v0.2 검사 시스템 (100문항) | 동작 |
| ✅ v0.3 카드 PDF (DARK/LIGHT) | 동작, E2 샘플 검증 |
| ✅ v0.2 결과지 PDF (A4 3페이지) | 동작, E2 샘플 검증 |
| ✅ 14개 페르소나 데이터 | 작성 완료 |
| ✅ UX 흐름도 | 완성 |
| 🔄 14개 페르소나 카드 일괄 생성 | 스크립트 작성, 검증 필요 |
| ⏳ v0.2 결과지 동적 생성 (응답 → PDF) | 미구현 |
| ⏳ Supabase 백엔드 | 미구현 |
| ⏳ 학교 단위 대시보드 | 미구현 |
| ⏳ AI 자소서 생성 (Claude API) | 미구현 |
| ⏳ 문항 신뢰도 검증 (파일럿) | 미구현 |

다음 작업 → [ROADMAP.md](ROADMAP.md)

---

## 📝 주요 의사결정 기록

1. **공인 검사가 아닌 자체 브랜드 검사** — RIASEC 이론(공개 도메인)을 활용하되, 문항·페르소나는 자체 제작 → 라이선스 자유
2. **"심리검사" 표현 회피** — "흥미 탐색", "커리어 코드"로 표현 → 임상 영역 침범 방지
3. **3중 수익 구조** — 개인 결제(LTV 7만원) + 학교 B2B(200-500만원) + 데이터 자산화
4. **첫 사이클은 데이터 수집 우선** — 문항 신뢰도(Cronbach's α) 검증을 위해 학생 100명 이상 응답 필요
5. **카드 톤은 DARK/LIGHT 둘 다 유지** — DARK는 디지털 공유용, LIGHT는 부스 대량 인쇄용 (잉크 80% 절감)

---

## 🤝 협업·문의

- **사업 책임:** 김진화 (Ahee)
- **회사:** [Ahee](https://www.ahee.co.kr) — 이벤트·MICE·체험학습·여행 전문
- **연락:** 02-430-8542
