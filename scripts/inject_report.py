# -*- coding: utf-8 -*-
"""
검사 결과 화면에 확장 리포트(양면 강점·함정 / NCS 역량 / 직무 자격증·기업 / 예시 이력서)를
주입한다. report_content.json을 HTML에 인라인 임베드하고 렌더 함수·HTML 섹션·CSS를 추가.
대상: public/v03_test.html, public/v02_test.html (자기완결형 정적 파일 유지).
재실행 안전: 이미 주입돼 있으면(MARKER 존재) 건너뜀.
"""
import json, sys, io
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rc = json.load(open(ROOT / "data" / "report_content.json", encoding="utf-8"))["personas"]
DATA_JS = json.dumps(rc, ensure_ascii=False)

MARKER = "/* __AHEE_REPORT_EXTRAS__ */"

CSS = """
/* __AHEE_REPORT_EXTRAS_CSS__ */
.twoface-note{border-left:2px solid var(--ahee);padding:10px 0 10px 14px;margin:0 0 20px;font-size:13.5px;line-height:1.65;color:var(--ink-2)}
.twoface-note b{color:var(--ink);font-weight:700}
.match-meta{font-family:var(--mono);font-size:10px;color:var(--ink-4);letter-spacing:.02em;line-height:1.5;margin-top:6px}
.match-meta b{color:var(--ahee);font-weight:500}
.ncs-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media (max-width:560px){.ncs-grid{grid-template-columns:1fr}}
.ncs-col{padding:18px;border:1px solid var(--line);background:var(--surface)}
.ncs-col.strong{background:var(--ink);border-color:var(--ink)}
.ncs-head{font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);margin-bottom:12px;display:flex;align-items:center;gap:6px}
.ncs-head .dot{color:var(--ahee)}
.ncs-col.strong .ncs-head{color:rgba(255,255,255,.55)}
.ncs-item{padding:9px 0;border-top:1px solid var(--line)}
.ncs-col.strong .ncs-item{border-top-color:rgba(255,255,255,.14)}
.ncs-item:first-child{border-top:none}
.ncs-name{font-weight:700;font-size:14px;margin-bottom:3px;color:var(--ink)}
.ncs-col.strong .ncs-name{color:#fff}
.ncs-desc{font-size:12.5px;line-height:1.55;color:var(--ink-2)}
.ncs-col.strong .ncs-desc{color:rgba(255,255,255,.75)}
.resume-tip{font-size:12px;color:var(--ink-3);border-left:2px solid var(--ahee);padding-left:12px;margin-bottom:16px;line-height:1.6}
.resume-tip b{color:var(--ink-2)}
.resume-box{border:1px solid var(--line-2);background:var(--surface)}
.resume-top{background:var(--ink);color:#fff;padding:18px 20px;display:flex;justify-content:space-between;align-items:flex-end}
.resume-top .rt-name{font-weight:800;font-size:22px;letter-spacing:-.03em}
.resume-top .rt-name .punct{color:var(--ahee)}
.resume-top .rt-target{font-family:var(--mono);font-size:10px;color:rgba(255,255,255,.6);letter-spacing:.06em;text-transform:uppercase;margin-top:6px}
.resume-top .rt-code{font-family:var(--eng);font-weight:900;font-size:22px;letter-spacing:-.04em}
.resume-in{padding:18px 20px}
.resume-blk{margin-bottom:16px}
.resume-blk:last-child{margin-bottom:0}
.rb-label{font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);margin-bottom:8px;display:flex;align-items:center;gap:5px}
.rb-label .dot{color:var(--ahee)}
.r-headline2{font-weight:700;font-size:15px;line-height:1.5;color:var(--ink)}
.r-skills{display:flex;flex-wrap:wrap;gap:6px}
.r-skills .tag{padding:4px 10px;border:1px solid var(--line-2);font-size:12px;font-weight:500;color:var(--ink-2)}
.r-skills .tag.hot{background:var(--ahee);color:#fff;border-color:var(--ahee);font-weight:600}
.r-exp{position:relative;padding-left:16px;padding-bottom:12px;border-left:1px solid var(--line-2)}
.r-exp:last-child{padding-bottom:0}
.r-exp::before{content:'';position:absolute;left:-4px;top:3px;width:7px;height:7px;border-radius:50%;background:var(--ahee)}
.r-exp .e-role{font-weight:700;font-size:14px;color:var(--ink)}
.r-exp .e-org{font-size:12.5px;color:var(--ink-3);font-weight:500}
.r-exp .e-period{font-family:var(--mono);font-size:10px;color:var(--ink-4);float:right}
.r-exp ul{list-style:none;margin-top:6px;padding:0}
.r-exp ul li{font-size:13px;line-height:1.5;color:var(--ink-2);padding-left:14px;position:relative;margin-bottom:4px}
.r-exp ul li::before{content:'';position:absolute;left:0;top:7px;width:5px;height:5px;background:var(--ink)}
.r-exp ul li .num{color:var(--ahee);font-weight:700}
.r-oneline{font-size:13.5px;color:var(--ink-2);line-height:1.5}
"""

def sections_html(ncs_num, resume_num):
    return ("""
      <!-- __AHEE_REPORT_EXTRAS_HTML__ -->
      <div class="section">
        <div class="section-label">section %s · ncs 직업기초능력</div>""" % ncs_num + """
        <h3>채용시장이 보는 당신의 역량</h3>
        <div class="ncs-grid">
          <div class="ncs-col strong">
            <div class="ncs-head"><span class="dot">●</span> 강한 역량 · TOP 3</div>
            <div id="ncs-strong"></div>
          </div>
          <div class="ncs-col">
            <div class="ncs-head"><span class="dot">●</span> 보완 역량 · CHECK 3</div>
            <div id="ncs-weak"></div>
          </div>
        </div>
      </div>

      <div class="section">
        <div class="section-label">section """ + str(resume_num) + """ · sample resume</div>
        <h3>이력서, 이렇게 써보세요</h3>
        <div class="resume-tip">이건 <b id="resume-persona"></b> 페르소나에 맞춘 예시입니다. ○○ 부분에 본인의 실제 경험·수치를 넣으세요.</div>
        <div class="resume-box">
          <div class="resume-top">
            <div>
              <div class="rt-name">○○○<span class="punct">.</span></div>
              <div class="rt-target" id="resume-target"></div>
            </div>
            <div style="text-align:right">
              <div style="font-family:var(--mono);font-size:9px;color:rgba(255,255,255,.4);letter-spacing:.08em;text-transform:uppercase;margin-bottom:3px">career code</div>
              <div class="rt-code" id="resume-code"></div>
            </div>
          </div>
          <div class="resume-in">
            <div class="resume-blk"><div class="rb-label"><span class="dot">●</span> headline</div><div class="r-headline2" id="resume-headline"></div></div>
            <div class="resume-blk"><div class="rb-label"><span class="dot">●</span> core skills</div><div class="r-skills" id="resume-skills"></div></div>
            <div class="resume-blk"><div class="rb-label"><span class="dot">●</span> experience</div><div id="resume-exp"></div></div>
            <div class="resume-blk"><div class="rb-label"><span class="dot">●</span> one-line</div><div class="r-oneline" id="resume-oneline"></div></div>
          </div>
        </div>
      </div>

""")

FUNC_JS = """%s
var REPORT_CONTENT = %s;
function renderReportExtras(r){
  try{
    var rc = REPORT_CONTENT[r.personaKey]; if(!rc) return;
    var p = r.persona;
    var $ = function(id){return document.getElementById(id);};
    if(rc.twoFace && $('d-twoface')) $('d-twoface').innerHTML = rc.twoFace;
    // 직무 자격증·기업
    var ml = $('match-list');
    if(ml){ var items = ml.querySelectorAll('.match-item');
      (rc.jobsMeta||[]).forEach(function(m,i){ if(items[i]){
        var d=document.createElement('div'); d.className='match-meta';
        d.innerHTML='<b>자격증</b> '+m.certs+' &nbsp;|&nbsp; <b>기업</b> '+m.companies;
        items[i].appendChild(d);} });
    }
    // NCS
    var nh=function(n){return '<div class="ncs-item"><div class="ncs-name">'+n.name+'</div><div class="ncs-desc">'+n.desc+'</div></div>';};
    if($('ncs-strong')) $('ncs-strong').innerHTML=(rc.ncsStrong||[]).map(nh).join('');
    if($('ncs-weak')) $('ncs-weak').innerHTML=(rc.ncsWeak||[]).map(nh).join('');
    // 이력서
    var rs=rc.resume||{};
    var code = (r.ranked && r.ranked.length) ? r.ranked.slice(0,3).map(function(x){return x.code;}).join('') : r.personaKey;
    if($('resume-persona')) $('resume-persona').textContent='The '+p.name+' ('+p.ko+')';
    if($('resume-target')) $('resume-target').textContent='target · '+(rs.target||'');
    if($('resume-code')) $('resume-code').textContent=code;
    if($('resume-headline')) $('resume-headline').innerHTML=(rs.headline||'').replace(/\\n/g,'<br>');
    if($('resume-skills')) $('resume-skills').innerHTML=(rs.skills||[]).map(function(s,i){return '<span class="tag'+(i<2?' hot':'')+'">'+s+'</span>';}).join('');
    if($('resume-exp')) $('resume-exp').innerHTML=(rs.experience||[]).map(function(e){return '<div class="r-exp"><span class="e-period">'+e.period+'</span><div class="e-role">'+e.role+'<span class="e-org"> \\u00b7 '+e.org+'</span></div><ul>'+(e.bullets||[]).map(function(b){return '<li>'+b+'</li>';}).join('')+'</ul></div>';}).join('');
    if($('resume-oneline')) $('resume-oneline').textContent=rs.oneLine||'';
  }catch(err){ if(window.console) console.error('[report extras]', err); }
}
""" % (MARKER, DATA_JS)


def inject(path, cfg):
    s = path.read_text(encoding="utf-8")
    if MARKER in s:
        print("  skip (already injected):", path.name); return
    n = len(s)
    SECTIONS_HTML = sections_html(cfg["ncs_num"], cfg["resume_num"])

    # 1) CSS before </style>
    assert s.count("</style>") >= 1, path.name + " no </style>"
    s = s.replace("</style>", CSS + "\n</style>", 1)

    # 2) data + function before renderResult
    anchor = "function renderResult(r) {"
    assert s.count(anchor) == 1, path.name + " renderResult anchor"
    s = s.replace(anchor, FUNC_JS + "\n" + anchor, 1)

    # 3) call renderReportExtras after renderResult(result)
    call_anchor = "renderResult(result);\n  showScreen('screen-result');"
    assert s.count(call_anchor) == 1, path.name + " call anchor"
    s = s.replace(call_anchor, "renderResult(result);\n  renderReportExtras(result);\n  showScreen('screen-result');", 1)

    # 4) two-face note after profile headline
    h3 = cfg["headline_h3"]
    assert s.count(h3) == 1, path.name + " profile headline anchor"
    s = s.replace(h3, h3 + '\n        <div class="twoface-note" id="d-twoface"></div>', 1)

    # 5) insert NCS + resume sections after people-grid
    people = '<div class="people-grid" id="people-grid"></div>\n      </div>'
    assert s.count(people) == 1, path.name + " people anchor"
    s = s.replace(people, people + "\n" + SECTIONS_HTML, 1)

    # 6) bump reliability label to keep ascending
    rf, rt = cfg["reliability_from"], cfg["reliability_to"]
    assert s.count(rf) == 1, path.name + " reliability label"
    s = s.replace(rf, rt, 1)

    path.write_text(s, encoding="utf-8")
    print("  injected:", path.name, "(+%d bytes)" % (len(s) - n))


CONFIG = {
    "v03_test.html": {
        "headline_h3": '<h3 id="detail-headline">당신은 어떤 사람일까요</h3>',
        "ncs_num": "05", "resume_num": "06",
        "reliability_from": "section 05 · reliability benchmark",
        "reliability_to": "section 07 · reliability benchmark",
    },
    "v02_test.html": {
        "headline_h3": '<h3 id="d-headline">당신은 어떤 사람일까요</h3>',
        "ncs_num": "07", "resume_num": "08",
        "reliability_from": "section 07 · reliability benchmark",
        "reliability_to": "section 09 · reliability benchmark",
    },
}

if __name__ == "__main__":
    for f, cfg in CONFIG.items():
        p = ROOT / "public" / f
        if p.exists():
            print("processing", f)
            try:
                inject(p, cfg)
            except AssertionError as e:
                print("  FAILED:", e)
        else:
            print("  missing:", f)
