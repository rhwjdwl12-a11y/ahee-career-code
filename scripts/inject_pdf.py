# -*- coding: utf-8 -*-
"""
검사 결과 화면에 '결과 PDF 다운로드' 기능을 주입한다.
- html2pdf.js (CDN) 로 클라이언트에서 바로 PDF 저장 (폰/PC, 백엔드 불필요)
- 결과 헤더 아래에 마젠타 버튼 추가
- pdf-mode CSS: 버튼·변형 토글 등 비인쇄 요소 숨김 + .accent 그라데이션을 단색으로 강제(html2canvas 호환)
대상: public/v03_test.html, public/v02_test.html. 재실행 안전(마커).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKER = "/* __AHEE_PDF_DL__ */"

CDN = "https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.2/html2pdf.bundle.min.js"

CSS = """
/* __AHEE_PDF_DL_CSS__ */
body.pdf-mode .screen,body.pdf-mode .container{max-width:none !important;padding-left:0 !important;padding-right:0 !important;margin:0 !important;width:100% !important}
body.pdf-mode .result{max-width:none !important;margin:0 !important;padding:14px 16px 0 16px !important}
.pdf-dl-btn{display:flex;align-items:center;justify-content:center;gap:8px;width:100%;margin:0 0 18px;padding:15px;background:var(--ahee);color:#fff;border:none;font-family:var(--sans);font-weight:700;font-size:15px;letter-spacing:-.01em;cursor:pointer;transition:filter .15s}
.pdf-dl-btn .ic{font-family:var(--mono);font-weight:400}
.pdf-dl-btn:hover{filter:brightness(.95)}
.pdf-dl-btn:disabled{opacity:.6;cursor:default}
body.pdf-mode .variants,body.pdf-mode .actions,body.pdf-mode .result-cta,body.pdf-mode footer,body.pdf-mode .submit-banner,body.pdf-mode .pdf-dl-btn,body.pdf-mode .diff-note{display:none !important}
body.pdf-mode .accent{background:none !important;-webkit-background-clip:initial !important;background-clip:initial !important;-webkit-text-fill-color:var(--ahee) !important;color:var(--ahee) !important}
body.pdf-mode .section,body.pdf-mode .card,body.pdf-mode .detail-card,body.pdf-mode .resume-box,body.pdf-mode .ncs-col,body.pdf-mode .person-card,body.pdf-mode .match-item{page-break-inside:avoid}
"""

BUTTON = ('\n        <button class="pdf-dl-btn" id="pdf-dl-btn">'
          '<span class="ic">↓</span> 결과 PDF 다운로드</button>')

SCRIPT = """
<script src="%s"></script>
<script>%s
(function(){
  function go(){
    var btn=document.getElementById('pdf-dl-btn'); if(!btn) return;
    btn.addEventListener('click', function(){
      var el=document.querySelector('.result'); if(!el) return;
      if(typeof html2pdf==='undefined'){ alert('PDF 모듈을 불러오는 중입니다. 잠시 후 다시 눌러주세요.'); return; }
      var key='result'; var wm=document.getElementById('card-watermark');
      if(wm && wm.textContent) key=wm.textContent.trim();
      var prev=btn.innerHTML; btn.disabled=true; btn.innerHTML='PDF 만드는 중\\u2026';
      document.body.classList.add('pdf-mode');
      try{ window.scrollTo(0,0); }catch(e){}
      var opt={ margin:[6,6,8,6], filename:'Ahee_커리어코드_'+key+'.pdf',
        image:{type:'jpeg',quality:0.96},
        html2canvas:{scale:2,useCORS:true,backgroundColor:'#ffffff',windowWidth:760,scrollX:0,scrollY:0,x:0,y:0},
        jsPDF:{unit:'mm',format:'a4',orientation:'portrait'},
        pagebreak:{mode:['css','legacy']} };
      function done(){ document.body.classList.remove('pdf-mode'); btn.disabled=false; btn.innerHTML=prev; }
      html2pdf().set(opt).from(el).save().then(done).catch(function(err){ if(window.console)console.error('[pdf]',err); done(); alert('PDF 저장 중 문제가 생겼어요. 다시 시도해주세요.'); });
    });
  }
  if(document.readyState!=='loading') go(); else document.addEventListener('DOMContentLoaded', go);
})();
</script>
""" % (CDN, MARKER)

ANCHOR_BTN = '<div class="submit-banner" id="submit-banner" style="display:none"></div>'


def inject(path):
    s = path.read_text(encoding="utf-8")
    if MARKER in s:
        print("  skip (already injected):", path.name); return
    n = len(s)

    assert s.count("</style>") >= 1, path.name + " no </style>"
    s = s.replace("</style>", CSS + "\n</style>", 1)

    assert s.count(ANCHOR_BTN) == 1, path.name + " submit-banner anchor"
    s = s.replace(ANCHOR_BTN, ANCHOR_BTN + BUTTON, 1)

    assert s.count("</body>") == 1, path.name + " </body>"
    s = s.replace("</body>", SCRIPT + "\n</body>", 1)

    path.write_text(s, encoding="utf-8")
    print("  injected:", path.name, "(+%d bytes)" % (len(s) - n))


if __name__ == "__main__":
    for f in ["v03_test.html", "v02_test.html"]:
        p = ROOT / "public" / f
        if p.exists():
            print("processing", f)
            try:
                inject(p)
            except AssertionError as e:
                print("  FAILED:", e)
        else:
            print("  missing:", f)
