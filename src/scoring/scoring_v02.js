/**
 * RIASEC 채점 로직 v0.3
 * Ahee 자체 검사 — Full Test
 *
 * 변경점 (v0.3):
 * - 역문항(reverse) 처리: 응답값 6-r 환산
 * - 보조 척도 (VAL/RISK/DIG/GLB) 별도 점수
 *
 * 입력: responses { 1: 4, 2: 3, ..., 122: 5 }
 * 출력: 채점 결과 (코드별 점수, 백분율, 상위 3코드, 메인 코드, 보조 척도)
 */

function scoreRIASEC(responses, questionnaire) {
  const items = questionnaire.items;
  const riasecCodes = ['R', 'I', 'A', 'S', 'E', 'C'];
  const extraCodes = ['VAL', 'RISK', 'DIG', 'GLB'];

  // 1) RIASEC 6코드 합산 (역문항 환산 포함)
  const rawScores = { R: 0, I: 0, A: 0, S: 0, E: 0, C: 0 };
  const counts = { R: 0, I: 0, A: 0, S: 0, E: 0, C: 0 };

  // 보조 척도 합산
  const extraRaw = {};
  const extraCount = {};
  extraCodes.forEach(c => { extraRaw[c] = 0; extraCount[c] = 0; });

  // facet 합산 (페르소나 분기용)
  const facetRaw = {};
  const facetCount = {};

  items.forEach(item => {
    let r = responses[item.id];
    if (r == null) return;
    if (item.reverse) r = 6 - r;

    if (riasecCodes.includes(item.code)) {
      rawScores[item.code] += r;
      counts[item.code] += 1;
      if (item.facet) {
        const key = `${item.code}::${item.facet}`;
        facetRaw[key] = (facetRaw[key] || 0) + r;
        facetCount[key] = (facetCount[key] || 0) + 1;
      }
    } else if (extraCodes.includes(item.code)) {
      extraRaw[item.code] += r;
      extraCount[item.code] += 1;
    }
  });

  // 2) 백분율 환산
  const normalize = (sum, n) => (n > 0 ? Math.round(((sum - n) / (n * 4)) * 100) : 0);

  const percentScores = {};
  riasecCodes.forEach(code => { percentScores[code] = normalize(rawScores[code], counts[code]); });

  const facetScores = {};
  Object.keys(facetRaw).forEach(k => { facetScores[k] = normalize(facetRaw[k], facetCount[k]); });

  const extraScores = {};
  extraCodes.forEach(c => { extraScores[c] = normalize(extraRaw[c], extraCount[c]); });

  // 3) 상위 3코드
  const ranked = riasecCodes
    .map(code => ({ code, score: percentScores[code] }))
    .sort((a, b) => {
      if (b.score !== a.score) return b.score - a.score;
      return riasecCodes.indexOf(a.code) - riasecCodes.indexOf(b.code);
    });

  const topThree = ranked.slice(0, 3).map(r => r.code);
  const hollandCode = topThree.join('');
  const mainCode = topThree[0];
  const mainScore = percentScores[mainCode];

  // 4) 강도·변별도
  let intensity;
  if (mainScore >= 75) intensity = '뚜렷함';
  else if (mainScore >= 55) intensity = '명확함';
  else if (mainScore >= 35) intensity = '경향성 있음';
  else intensity = '약함';

  const gap12 = ranked[0].score - ranked[1].score;
  let differentiation;
  if (gap12 >= 20) differentiation = '단일 코드형';
  else if (gap12 >= 10) differentiation = '주력 코드형';
  else differentiation = '복합 코드형';

  return {
    rawScores,
    percentScores,
    facetScores,
    extraScores,
    ranked,
    topThree,
    hollandCode,
    mainCode,
    intensity,
    differentiation,
    profile: questionnaire.codeProfiles ? questionnaire.codeProfiles[mainCode] : null,
    completedAt: new Date().toISOString()
  };
}

function validateResponses(responses, questionnaire) {
  const totalItems = questionnaire.items.length;
  const answered = Object.keys(responses).length;
  const missing = [];

  questionnaire.items.forEach(item => {
    if (responses[item.id] == null) missing.push(item.id);
  });

  return {
    valid: missing.length === 0,
    answered,
    total: totalItems,
    missing,
    message: missing.length === 0
      ? '모든 문항에 응답했습니다'
      : `${missing.length}개 문항이 남았습니다 (${missing.slice(0, 5).join(', ')}${missing.length > 5 ? '...' : ''})`
  };
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { scoreRIASEC, validateResponses };
}
