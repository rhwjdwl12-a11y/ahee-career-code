# CLAUDE.md — Claude Code 작업 가이드

> **이 파일은 Claude Code가 작업을 시작할 때 가장 먼저 읽어야 합니다.**
> 김진화 님의 디자인 톤·작업 워크플로·금지사항이 모두 정리되어 있습니다.

---

## 🧑 사용자 컨텍스트

- **이름:** 김진화
- **소속:** Ahee (아희) — 4인 팀의 기획·디자인·AI 담당
- **환경:** WSL (Ubuntu, 사용자명 `openclaw`), 호스트 `DESKTOP-PEM1QRT`
- **선호 도구:** Node.js (npm), Python 3, Playwright, python-pptx
- **소통 스타일:** 매우 짧고 효율적. "계속", "다시", "해줘" 같은 단어로 의도를 전달하시는 편. 의도를 빠르게 파악해서 진행하는 게 중요.

---

## 🎨 절대 지켜야 할 디자인 톤

### 컬러 (변경 금지)
```css
--ahee: #FF3366;          /* 메인 액센트 — 마젠타 */
--ink: #0A0A0A;           /* 잉크 — 거의 블랙 */
--bg: #FAFAF8;            /* 배경 — 따뜻한 오프화이트 */
--line: #ECECEC;          /* 라인 — 옅은 회색 */
--ink-2: #2A2A2A;         /* 보조 텍스트 */
--ink-3: #6B6B6B;         /* 메타 텍스트 */
```

**RIASEC 코드별 컬러 (참고용, 결과 차트에서 사용):**
```css
R: #E85A4F  I: #4F77E8  A: #9B59E8
S: #2EBA6A  E: #F39C12  C: #16A2A8
```

### 폰트
| 용도 | 폰트 | weight |
|---|---|---|
| 영문 헤드/숫자 | Inter Tight | 800/900 |
| 한글 본문 | Pretendard | 500/700/800 |
| 라벨·메타 | JetBrains Mono | 400/500 |

**CDN:**
```html
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" rel="stylesheet">
```

### 시그니처 요소 (절대 빠뜨리지 말 것)
1. **마젠타 마침표** — 큰 헤드라인 끝에 `<span style="color:var(--ahee)">.</span>`
2. **mono 라벨 + ● 닷** — `● career persona / E2` 형식
3. **거대 워터마크** — `opacity: 0.04`, 페이지 뒤에 옅게 (Inter Tight 200pt+)
4. **document no.** — 우측 상단 `ACC-2026-0001` 같은 형식
5. **다크 강조 블록** — 핵심 카드는 `background: #0A0A0A`로 강조
6. **인용 사이드보더** — `border-left: 2px solid var(--ahee); padding-left`
7. **점 구분자** — 메타 정보에 ` · ` 또는 `●` 사용

### 자주 하는 실수 (반복 금지)
- ❌ 영문 헤드라인에 Pretendard 사용 → ✅ 반드시 Inter Tight
- ❌ 마젠타 색상을 다른 톤으로 — `#E63946`, `#FF3B5C` 같은 비슷한 색 쓰지 말 것 → ✅ 정확히 `#FF3366`
- ❌ 둥근 모서리(border-radius) 큰 값 → ✅ 거의 0 또는 매우 작게 (1-3px)
- ❌ 그라데이션 남발 → ✅ 단색이 기본, 그라데이션은 카드 배경 등 특수 경우만
- ❌ 작은 영문 mono 라벨 남발해서 한글이 작게 보이게 → ✅ 한글 14px+ 우선
- ❌ 컬러 남발 → ✅ 흰 배경 + 잉크 + 마젠타 단색이 기본
- ❌ 헤드라인 끝 마침표 누락 → ✅ 반드시 마젠타 점

---

## 🔧 핵심 워크플로

### PDF 생성 (가장 자주 함)
```bash
# 카드 PDF (특정 페르소나)
python scripts/build_card.py --persona E2 --theme dark

# 14개 페르소나 × 2 톤 = 28개 PDF 일괄
python scripts/build_card.py --all

# A4 결과지
python scripts/build_report.py --persona E2
```

### 폰트 로딩 안정화 (필수)
Playwright로 PDF 생성 시 한글/Inter Tight 폰트가 로드되기 전에 PDF가 만들어지면 텍스트가 깨짐. 반드시:
```python
await page.goto(url, wait_until="networkidle")
await page.wait_for_timeout(800)  # 폰트 로딩 마진
```

### PDF 사이즈
- 카드: `width="105mm", height="148mm"` (A6)
- 결과지: `width="210mm", height="297mm"` (A4)
- `prefer_css_page_size=True` 옵션 사용 (HTML의 `@page` 룰 존중)

---

## 📂 데이터 구조

### `data/personas.json`
14개 페르소나가 `personas` 객체에 저장. 각 페르소나는:
```json
{
  "code": "E",
  "name": "Driver",
  "ko": "기회 추진형",
  "slogan": "...",
  "traits": ["#리더십", ...],
  "strength": "...",
  "pitfall": "...",
  "match": "...",
  "advice": "...",
  "growth": "...",
  "jobs": [["직무명", 적합도%], ...]
}
```

**페르소나 매칭은 1·2위 코드 조합으로 결정**. `matchingRules` 참조.

### `data/questions_v03.json`
24문항. 각 문항 `{id, code, text}`. 코드는 R/I/A/S/E/C 중 하나.

### `data/questions_v02.json`
100문항. v03보다 `facet` 필드 추가 (예: `"리더십·설득"`).

---

## 🚫 절대 하지 말 것

1. **임상·심리치료 표현 사용 금지** — "심리검사", "진단", "치료" 등의 단어는 의료 영역. "흥미 탐색", "커리어 코드"로.
2. **상용 검사 도구 베끼기 금지** — MBTI, DISC, StrengthsFinder의 명칭·구조 직접 사용 금지. RIASEC만 OK (공개 도메인).
3. **개인정보 수집 시 동의 없이 진행 금지** — 학교 단위 운영 시 학생 동의서 필수.
4. **사용자 메모리에 민감 정보 저장 금지** — 비밀번호, 학생 신상 등.
5. **마젠타 톤 임의 변경 금지** — `#FF3366`은 Ahee의 정체성.
6. **page-break-after 빠뜨리지 말 것** — 다중 페이지 HTML에서 PDF 변환 시 페이지 분리 안 됨.

---

## 🎯 작업 시 의사결정 기준

김진화 님이 결정하지 않은 디자인 디테일을 만났을 때:

1. **여백 vs 빽빽함** → 여백을 더 (Ahee는 미니멀)
2. **컬러 추가 vs 단색 유지** → 단색 유지 (마젠타 1개로 충분)
3. **헤드라인 강조 추가 vs 단순화** → 단순화 (마젠타 점 하나로 끝)
4. **장식 요소 추가 vs 제거** → 제거 (현대카드는 본질만)
5. **폰트 사이즈 키울지 줄일지** → 한글은 키우고(가독성), 영문 라벨은 줄임

확신이 없으면 **김진화 님께 한 번 물어보고 가는 것이 빠름** (1번 묻고 정답 내는 게, 3번 수정하는 것보다 효율적).

---

## 💬 김진화 님 의사소통 스타일에 맞추기

- "계속" / "ㅇㅇ" / "다시" → 직전 작업의 자연스러운 다음 단계 진행
- "해줘" / "만들어줘" → 바로 산출물 만들기 (긴 설명 X)
- "왜 안 돼" / "잘 안 보여" → 즉시 점검하고 짧게 답변
- 짧은 답이 와도 차분하게 의도 파악하고 진행. 길게 묻거나 확인하지 말 것.
- **결과물이 우선**, 설명은 짧게.

---

## 🔗 관련 자료

- 메인 보고서 톤 레퍼런스: 가천대 직무박람회 결과보고서 (`gachon-report-redesign_v1.0.zip`)
- 김진화 님의 기존 스킬: `html-ppt-maker`, `ppt-redesign`, `excel-dashboard`, `seojeong-poster-style`
- Ahee 자체 톤은 위 스킬들의 학교 컬러 대신 **마젠타(#FF3366)** 를 메인으로 사용

---

**이 파일은 살아있는 문서입니다.** 김진화 님이 새로운 디자인 결정·금지사항을 알려주시면 여기에 추가하세요.
