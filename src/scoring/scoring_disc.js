/**
 * Ahee Behavior Style (DISC) v0.1 채점 로직
 * 강제선택(ipsative) — 각 블록에서 most(+1)·least(-1) 선택
 *
 * 입력
 *   responses: { [blockId]: { most: 'D'|'I'|'S'|'C', least: 'D'|'I'|'S'|'C' } }
 *   blocks:    [{ id, opts: [{ t, axis }] }]   (axis 검증용, 없어도 동작)
 *
 * 채점
 *   - mostCount[axis], leastCount[axis] 집계
 *   - net[axis] = most - least  → 순위 결정
 *   - percent[axis] = net을 0~100으로 선형 변환 (균형=50)
 *   - primary / secondary / blendKey 산출, 변별도(gap) 계산
 */

const DISC_AXES = ['D', 'I', 'S', 'C'];

function scoreDISC(responses, totalBlocks) {
  const mostCount = { D: 0, I: 0, S: 0, C: 0 };
  const leastCount = { D: 0, I: 0, S: 0, C: 0 };

  let answered = 0;
  Object.keys(responses || {}).forEach(blockId => {
    const r = responses[blockId];
    if (!r || !r.most || !r.least) return;
    if (r.most === r.least) return; // 같은 항목을 most/least로 동시 선택 — 무효
    mostCount[r.most] += 1;
    leastCount[r.least] += 1;
    answered += 1;
  });

  const N = totalBlocks || answered || 1;

  const net = {}, percent = {};
  DISC_AXES.forEach(a => {
    net[a] = mostCount[a] - leastCount[a];
    // net 범위 [-N, +N] → [0, 100], 균형(0) = 50
    percent[a] = Math.max(0, Math.min(100, Math.round(((net[a] + N) / (2 * N)) * 100)));
  });

  // 순위: net 내림차순, 동률은 D>I>S>C 고정 순서
  const ranked = DISC_AXES
    .map(a => ({ axis: a, net: net[a], most: mostCount[a], least: leastCount[a], percent: percent[a] }))
    .sort((x, y) => y.net - x.net || DISC_AXES.indexOf(x.axis) - DISC_AXES.indexOf(y.axis));

  const primary = ranked[0].axis;
  const secondary = ranked[1].axis;
  const blendKey = primary + secondary;

  // 변별도: 1·2위 net 격차
  const gap12 = ranked[0].net - ranked[1].net;
  let pattern;
  if (gap12 >= 8) pattern = '뚜렷한 단일형';
  else if (gap12 >= 4) pattern = '주력 스타일형';
  else if (gap12 >= 2) pattern = '복합 스타일형';
  else pattern = '경계 스타일형';

  return {
    mostCount,
    leastCount,
    net,
    percent,
    ranked,
    primary,
    secondary,
    blendKey,
    gap12,
    pattern,
    answered,
    completedAt: new Date().toISOString()
  };
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { scoreDISC, DISC_AXES };
}
