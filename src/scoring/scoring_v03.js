/**
 * Ahee Career Card v0.4 채점 로직
 * 31문항 → 6코드 점수 + facet sub-score → 페르소나 매칭
 *
 * 변경점 (v0.4):
 * - 역문항(reverse) 처리: 응답값을 6-r 로 환산
 * - facet 기반 페르소나 분기: 같은 코드 내 페르소나는 primaryFacet 점수로 분기
 * - 동률 시 mainCode + secondCode 폴백
 */

function normalize(rawSum, count) {
  return count > 0 ? Math.round(((rawSum - count) / (count * 4)) * 100) : 0;
}

function scoreV03(responses, questionnaire, personaData) {
  const items = questionnaire.items;
  const codes = ['R', 'I', 'A', 'S', 'E', 'C'];

  // 1) 역문항 환산 + 코드별 합산 + facet별 합산
  const raw = {}, counts = {};
  const facetRaw = {}, facetCount = {};
  codes.forEach(c => { raw[c] = 0; counts[c] = 0; });

  items.forEach(item => {
    let r = responses[item.id];
    if (r == null) return;
    if (item.reverse) r = 6 - r;

    raw[item.code] += r;
    counts[item.code] += 1;

    if (item.facet) {
      const key = `${item.code}::${item.facet}`;
      facetRaw[key] = (facetRaw[key] || 0) + r;
      facetCount[key] = (facetCount[key] || 0) + 1;
    }
  });

  // 2) 백분율 환산
  const percentScores = {};
  codes.forEach(c => { percentScores[c] = normalize(raw[c], counts[c]); });

  const facetScores = {};
  Object.keys(facetRaw).forEach(k => {
    facetScores[k] = normalize(facetRaw[k], facetCount[k]);
  });

  // 3) 코드 정렬
  const ranked = codes
    .map(c => ({ code: c, score: percentScores[c] }))
    .sort((a, b) => b.score - a.score || codes.indexOf(a.code) - codes.indexOf(b.code));

  const mainCode = ranked[0].code;
  const secondCode = ranked[1].code;

  // 4) 페르소나 매칭 — facet 우선
  const personaKey = pickPersona(mainCode, secondCode, facetScores, personaData);
  const persona = personaKey ? personaData.personas[personaKey] : null;

  return {
    rawScores: raw,
    percentScores,
    facetScores,
    ranked,
    mainCode,
    secondCode,
    personaKey,
    persona,
    completedAt: new Date().toISOString()
  };
}

/**
 * mainCode 코드 안에 있는 페르소나들 중 primaryFacet 점수가 가장 높은 것을 고른다.
 * facet 정보가 부족하거나 동률이면 fallbackBySecondCode로 폴백.
 */
function pickPersona(mainCode, secondCode, facetScores, personaData) {
  const candidates = Object.entries(personaData.personas)
    .filter(([, p]) => p.code === mainCode);

  if (candidates.length === 1) return candidates[0][0];

  // facet 기반 점수
  const scored = candidates.map(([key, p]) => {
    const facetKey = `${mainCode}::${p.primaryFacet}`;
    const score = facetScores[facetKey];
    return { key, score: score == null ? -1 : score };
  });

  scored.sort((a, b) => b.score - a.score);

  // 1위와 2위 facet 격차가 충분히 크면 facet 결과 채택 (5점 이상)
  if (scored.length >= 2 && scored[0].score - scored[1].score >= 5 && scored[0].score >= 0) {
    return scored[0].key;
  }

  // facet 동률·근소 차이 → secondCode 폴백 사용
  const rules = personaData.matchingRules.fallbackBySecondCode || [];
  for (const rule of rules) {
    if (rule.mainCode !== mainCode) continue;
    if (rule.secondaryCodes === 'default') return rule.personaKey;
    if (Array.isArray(rule.secondaryCodes) && rule.secondaryCodes.includes(secondCode)) {
      return rule.personaKey;
    }
  }

  // 최종 폴백
  return scored[0].key;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { scoreV03, pickPersona };
}
