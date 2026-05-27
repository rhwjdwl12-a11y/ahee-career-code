# Google Apps Script 백엔드 — 5분 셋업

응답 데이터를 김진화 님 구글 시트로 받는 무료 백엔드입니다.

---

## 🚀 1단계 — 구글 시트 생성

1. [drive.google.com](https://drive.google.com) → **새로 만들기 → Google 스프레드시트**
2. 시트 이름: `Ahee Career Code 응답` (편한 이름 아무거나)
3. **URL을 어딘가 메모해 두세요** — 응답 확인용

---

## 🛠 2단계 — Apps Script 코드 붙여넣기

1. 위 시트에서 **확장 프로그램 → Apps Script** 클릭
2. 기본 `Code.gs` 내용 전부 삭제
3. **이 폴더의 `google-apps-script.gs` 내용을 통째로 복사 → 붙여넣기**
4. 좌측 상단 프로젝트 이름을 `Ahee Backend` 같은 걸로 변경
5. **💾 저장** (Ctrl+S)

---

## 🌐 3단계 — 웹 앱으로 배포

1. 우측 상단 **배포 → 새 배포**
2. 톱니바퀴 ⚙️ → **웹 앱** 선택
3. 다음과 같이 설정:
   - **설명**: `Ahee Career Code 응답 수집 v1`
   - **실행 권한**: `나` (본인 구글 계정)
   - **액세스 권한**: `모든 사용자` (익명도 POST 가능해야 함)
4. **배포** 클릭
5. 권한 승인 — 처음 한 번 구글 OAuth 동의 화면이 뜸. "고급 → 안전하지 않음으로 이동 → 허용"
6. **웹 앱 URL 복사** — 형식: `https://script.google.com/macros/s/AKfyc.../exec`

---

## 🔌 4단계 — 검사 페이지에 URL 연결

검사 페이지 (`public/v02_test.html`, `public/v03_test.html`) 각각의 `<script>` 시작 부분에서:

```js
const SUBMIT_URL = ''; // ← 여기에 위에서 복사한 웹 앱 URL 붙여넣기
```

이걸:
```js
const SUBMIT_URL = 'https://script.google.com/macros/s/AKfyc.../exec';
```

로 바꾸면 끝.

---

## ✅ 5단계 — 동작 확인

1. 검사 페이지를 브라우저로 열기
2. 검사 1회 끝까지 진행 → "결과 보고서 받기"
3. 시트로 돌아가 새로고침 → **`responses` 시트가 자동 생성되고 한 행이 추가되어 있어야 정상**
4. 컬럼 헤더: `submittedAt`, `personaKey`, `mainCode`, ..., `responses` (JSON)

---

## 🧪 백엔드만 따로 테스트하기

Apps Script 편집기에서:
1. 함수 선택 드롭다운 → `testSubmit` 고르기
2. **▶ 실행**
3. `responses` 시트에 테스트 행 1줄 추가됐는지 확인

---

## 📊 수집된 데이터 활용

시트의 컬럼:
- **기본**: `submittedAt`, `personaKey`, `mainCode`, `secondCode`, `hollandCode`, `intensity`, `differentiation`
- **응답자**: `gender`, `grade`, `school` (선택 입력)
- **응답 품질**: `totalSec`, `avgSec`, `suspicious` (1초 미만 다답 의심)
- **6코드 점수**: `R` ~ `C`
- **보조 척도**: `VAL`, `RISK`, `DIG`, `GLB` (v02만)
- **세부**: `facets` (JSON), `responses` (JSON, 문항별 1-5 응답)
- **메타**: `userAgent`

### 분석 시작 — 학생 30명 모이면

피벗 테이블로 즉시 분석 가능:
- 페르소나별 분포 (14개 중 어디가 많이 나오는지 → 군집 검증)
- 평균 응답 시간 vs 페르소나
- 학년·성별 별 페르소나 분포
- 6코드 평균 점수 (모집단 percentile 기준 만들기)

100명 모이면 Cronbach's α 계산 → 결과지에 자체 신뢰도 발표 가능.

---

## 🚨 한 가지 주의

- Apps Script `doPost`는 무료지만 **일일 호출 제한 ~20,000건**. 학교 단위 운영 시 충분.
- 응답이 시트에만 쌓이고 어디로도 전송 안 됨 (개인정보 보호).
- 응답자 IP는 수집하지 않음.

---

## 🔁 코드 업데이트할 때

`google-apps-script.gs`를 수정했으면:
1. Apps Script 편집기에서 코드 갱신
2. **배포 → 배포 관리 → ✏️ 수정 → 버전: 새 버전 → 배포**
3. 같은 URL이 유지되니 검사 페이지 코드는 안 바꿔도 됨
