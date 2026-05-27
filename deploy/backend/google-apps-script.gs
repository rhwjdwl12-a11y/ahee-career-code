/**
 * Ahee Career Code — 응답 수집 백엔드
 * Google Apps Script + Google Sheets
 *
 * 셋업 5분 안내는 deploy/backend/SETUP.md 참고
 *
 * 시트 구조 (자동 생성):
 *   submittedAt | version | personaKey | mainCode | secondCode | hollandCode |
 *   gap12 | intensity | differentiation | gender | grade | school |
 *   totalSec | avgSec | suspicious | scoresR/I/A/S/E/C | extras_VAL/RISK/DIG/GLB |
 *   facets (JSON) | responses (JSON) | userAgent
 */

const SHEET_NAME = 'responses';

// 시트 자동 생성 + 헤더
function ensureSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
    sheet.appendRow([
      'submittedAt', 'version', 'personaKey', 'mainCode', 'secondCode', 'hollandCode',
      'gap12', 'intensity', 'differentiation',
      'gender', 'grade', 'school',
      'totalSec', 'avgSec', 'suspicious',
      'R', 'I', 'A', 'S', 'E', 'C',
      'VAL', 'RISK', 'DIG', 'GLB',
      'facets', 'responses', 'userAgent'
    ]);
    sheet.getRange(1, 1, 1, 28).setFontWeight('bold').setBackground('#0A0A0A').setFontColor('#FFFFFF');
    sheet.setFrozenRows(1);
  }
  return sheet;
}

// POST 핸들러 — 검사 페이지에서 fetch로 호출
function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const sheet = ensureSheet();
    const p = data.percentScores || {};
    const x = data.extraScores || {};
    const q = data.quality || {};

    sheet.appendRow([
      new Date().toISOString(),
      data.version || '',
      data.personaKey || '',
      data.mainCode || '',
      data.secondCode || '',
      data.hollandCode || '',
      data.gap12 ?? '',
      data.intensity || '',
      data.differentiation || '',
      data.meta?.gender || '',
      data.meta?.grade || '',
      data.meta?.school || '',
      q.totalSec ?? '',
      q.avgSec ?? '',
      q.suspicious ?? '',
      p.R ?? '', p.I ?? '', p.A ?? '', p.S ?? '', p.E ?? '', p.C ?? '',
      x.VAL ?? '', x.RISK ?? '', x.DIG ?? '', x.GLB ?? '',
      JSON.stringify(data.facetScores || {}),
      JSON.stringify(data.responses || {}),
      data.userAgent || ''
    ]);

    return ContentService
      .createTextOutput(JSON.stringify({ ok: true, id: sheet.getLastRow() }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ ok: false, error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// GET — 헬스체크용
function doGet() {
  return ContentService
    .createTextOutput(JSON.stringify({
      ok: true,
      service: 'ahee-career-code',
      ts: new Date().toISOString()
    }))
    .setMimeType(ContentService.MimeType.JSON);
}

// 수동 테스트
function testSubmit() {
  const fake = {
    postData: {
      contents: JSON.stringify({
        version: 'test',
        personaKey: 'E2',
        mainCode: 'E', secondCode: 'C', hollandCode: 'ECS',
        gap12: 12, intensity: '명확함', differentiation: '주력 코드형',
        meta: { gender: 'F', grade: '대3', school: '서정대' },
        quality: { totalSec: 540, avgSec: 4.4, suspicious: false },
        percentScores: { R: 45, I: 62, A: 51, S: 70, E: 82, C: 75 },
        extraScores: { VAL: 65, RISK: 58, DIG: 72, GLB: 40 },
        facetScores: { 'E::추진력·결과': 88 },
        responses: { 1: 4, 2: 3 },
        userAgent: 'test'
      })
    }
  };
  Logger.log(doPost(fake).getContent());
}
