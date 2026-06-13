# Ahee Career Code — 배포 가이드

테스트 배포 + 데이터 수집까지 30분 안에 끝나는 셋업입니다.

---

## 📦 전체 흐름

```
1️⃣  Google Sheets 백엔드     → 5분  (이 폴더 backend/SETUP.md)
2️⃣  검사 페이지에 URL 연결    → 1분  (SUBMIT_URL 한 줄 교체)
3️⃣  GitHub에 푸시            → 5분  (이 문서 ↓)
4️⃣  Vercel 배포             → 5분  (이 문서 ↓)
5️⃣  공개 URL로 학생 응답 수집 → 즉시 시작
```

---

## 🚀 1단계 — GitHub Repository 만들기

이미 GitHub 계정이 있으시면 5분:

```bash
# 프로젝트 폴더에서
cd /mnt/c/Users/home/Desktop/ahee-career-code

# Git 초기화 (아직 안 했으면)
git init
git add .
git commit -m "v0.5: data collection ready"

# GitHub에서 새 repo 만들기 (private 권장):
#   https://github.com/new
#   Name: ahee-career-code
#   Visibility: Private
#
# 그 다음 (YOUR_USERNAME 본인 GitHub ID로):
git remote add origin https://github.com/YOUR_USERNAME/ahee-career-code.git
git branch -M main
git push -u origin main
```

---

## 🌐 2단계 — Vercel 배포

1. [vercel.com/signup](https://vercel.com/signup) — **GitHub 계정으로 가입** (무료)
2. 대시보드 → **Add New → Project**
3. 방금 만든 `ahee-career-code` 선택 → **Import**
4. 다음 설정 (대부분 자동 인식):
   - **Framework Preset**: `Other`
   - **Root Directory**: `.` (기본값)
   - **Build Command**: 비워두기
   - **Output Directory**: `public`
   - **Install Command**: 비워두기
5. **Deploy** 클릭 → 30초~1분 대기
6. ✅ 완료! `https://ahee-career-code-xxx.vercel.app` 형태의 URL 받음

### 배포된 페이지
- `/`        → 검사 선택 랜딩 (빠른·정밀·행동스타일)
- `/quick`   → v03 퀵 흥미검사 (31문항)
- `/full`    → v02 풀 흥미검사 (122문항)
- `/disc`    → DISC 행동스타일 검사 (40블록 강제선택)

---

## 🔁 3단계 — 코드 수정 후 자동 재배포

GitHub `main` 브랜치에 push만 하면 Vercel이 자동으로 다시 배포합니다:

```bash
git add .
git commit -m "문항 손질"
git push
```

대시보드에서 30초 안에 새 버전 반영.

---

## 🌐 4단계 — 커스텀 도메인 (선택)

Ahee 공식 도메인이 있으시면:
1. Vercel 프로젝트 → **Settings → Domains**
2. `test.ahee.co.kr` 같은 서브도메인 추가
3. 안내된 CNAME 레코드를 도메인 관리 페이지(가비아·후이즈)에 추가
4. 5분~30분 내 SSL까지 자동 적용

---

## 📊 5단계 — 응답 수집 시작

준비됐다면 공개 URL을 다음 채널에 뿌리세요:

| 채널 | 효율 | 비고 |
|---|---|---|
| 인스타 스토리 (Ahee 계정) | ⭐⭐⭐⭐ | 카드 디자인이 그대로 캡처돼서 바이럴 잘 됨 |
| 학교 진로팀에 메일 | ⭐⭐⭐⭐⭐ | 30~100명 단위 응답 빠르게 수집 |
| 카톡 단톡방 (학생) | ⭐⭐⭐ | 자발성 낮음, 친구·후배 동원 |
| 트위터·스레드 | ⭐⭐ | Z세대 도달, 응답률 낮음 |
| 학교 게시판·홍보 | ⭐⭐⭐ | 시간 걸림 |

### 목표 응답 수
- **30명**: 최소 디버깅 — 페르소나 분포 확인, 문항 이탈률 체크
- **100명**: Cronbach's α 계산 → 신뢰도 자체 발표 가능
- **300명**: 14페르소나 군집 분석 → 페르소나 통폐합·신설 판단 근거
- **500명+**: 학교 영업 시 신뢰도 자료로 제시 가능

---

## 🛠 6단계 — 시트에서 응답 확인

`backend/SETUP.md`에서 만든 Google Sheets를 열면:
- 응답 1건마다 1행 추가
- 페르소나·점수·메타데이터 즉시 확인
- 피벗 테이블로 분포·평균 즉시 계산 가능

### 추천 분석 (학생 30명 기준)
1. 페르소나 분포 → 14개 중 잘 안 나오는 페르소나 = 통폐합 후보
2. 평균 응답 시간 → 2초 미만 응답자 비율 (응답 품질 지표)
3. mainCode 1·2위 격차 평균 → 변별도 통계
4. R/I/A/S/E/C 평균 → 한국 학생 일반 분포 확인

---

## ⚠️ 자주 묻는 트러블슈팅

**Q. Vercel 배포 후 검사가 안 보여요**
- `vercel.json`의 `outputDirectory: public`이 맞는지 확인
- Vercel 대시보드 → **Settings → General → Build & Development**에서도 동일 설정

**Q. 응답이 시트에 안 쌓여요**
- 검사 페이지에서 F12 → Console에 `SUBMIT_URL`이 비어있다는 경고가 있는지 확인
- `SUBMIT_URL` 값이 `/exec`로 끝나야 함 (`/dev` 아님)
- Apps Script에서 **배포 → 배포 관리 → 액세스 권한이 "모든 사용자"인지** 확인

**Q. 검사 페이지에 CORS 오류**
- 정상입니다. GAS `no-cors` 모드라 응답은 못 읽지만 시트에는 저장됨
- 시트 새로고침해서 새 행이 들어왔는지 확인

**Q. 모바일에서 검사 화면이 잘려요**
- 두 페이지 다 반응형 적용됨. 안 되면 캐시 비우기 (Ctrl+Shift+R)

---

## 💡 다음 단계 권장

배포·수집 안정화되면:
1. **이메일·카톡 결과 발송** — Resend + 서버리스 함수 (1-2일)
2. **결과지 PDF 다운로드** — 현재 build_report.py 활용
3. **percentile 자동 계산** — 100명 모이면 결과 화면에 "상위 OO%" 활성화
4. **A/B 테스트** — Vercel preview 배포로 문항 변형 시험
