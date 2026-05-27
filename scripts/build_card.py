"""
build_card.py
-----------------
v0.3 페르소나 카드 PDF 일괄 생성 스크립트

사용법:
  # 모든 페르소나 생성 (28개 PDF: 14개 × DARK/LIGHT)
  python scripts/build_card.py --all

  # 특정 페르소나만
  python scripts/build_card.py --persona E2

  # 톤 지정
  python scripts/build_card.py --persona E2 --theme dark

요구사항:
  pip install playwright --break-system-packages
  playwright install chromium  (최초 1회)
"""

import asyncio
import argparse
import json
import re
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
TEMPLATE_DIR = ROOT / "templates"
OUTPUT_DIR = ROOT / "output" / "cards"

# 페르소나 데이터 로드
with open(DATA_DIR / "personas.json", "r", encoding="utf-8") as f:
    PERSONA_DATA = json.load(f)


def render_template(template_html: str, persona_key: str) -> str:
    """카드 HTML 템플릿에 페르소나 데이터 주입."""
    p = PERSONA_DATA["personas"][persona_key]
    persona_idx = list(PERSONA_DATA["personas"].keys()).index(persona_key) + 1
    total = len(PERSONA_DATA["personas"])
    code_name = PERSONA_DATA["codeNames"][p["code"]]

    # 슬로건은 줄바꿈 보존
    slogan_html = p["slogan"]
    if "\\n" in slogan_html:
        slogan_html = slogan_html.replace("\\n", "<br>")

    traits_html = "".join(f'<span class="trait">{t}</span>' for t in p["traits"])

    # 직무 매칭 5개 (job match)
    jobs_html_rows = ""
    for i, (name, pct) in enumerate(p["jobs"][:5], 1):
        jobs_html_rows += f"""
          <div class="match-item">
            <div class="match-rank">{i:02d}</div>
            <div class="match-name">{name}</div>
            <div class="match-bar"><div class="match-fill" style="width:{pct}%"></div></div>
            <div class="match-pct">{pct}<span class="unit">%</span></div>
          </div>"""

    # 템플릿은 E2 기준 하드코딩이라 placeholder를 치환
    out = template_html
    out = re.sub(r'<div class="watermark">E2</div>', f'<div class="watermark">{persona_key}</div>', out)
    out = re.sub(r'no\. 011 / 014', f'no. {persona_idx:03d} / {total:03d}', out)
    out = re.sub(r'● career persona / E2', f'● career persona / {persona_key}', out)
    out = re.sub(r'<div class="name">The <span class="accent">Driver</span>.*?</div>',
                 f'<div class="name">The <span class="accent">{p["name"]}</span><span class="punct">.</span></div>', out)
    out = re.sub(r'<div class="en">기회 추진형</div>', f'<div class="en">{p["ko"]}</div>', out)
    out = re.sub(r'<div class="slogan">.*?</div>',
                 f'<div class="slogan">{slogan_html}</div>', out, flags=re.DOTALL)
    out = re.sub(r'<div class="traits"[^>]*>.*?</div>',
                 f'<div class="traits">{traits_html}</div>', out, flags=re.DOTALL)
    out = re.sub(r'<div class="v">E · 기업형</div>', f'<div class="v">{p["code"]} · {code_name}</div>', out)
    out = re.sub(r'<div class="v">사업개발 · PM</div>',
                 f'<div class="v">{p["jobs"][0][0]} · {p["jobs"][1][0]}</div>', out)
    # 뒷면 코드 태그
    out = re.sub(r'<div class="code-tag">E2</div>', f'<div class="code-tag">{persona_key}</div>', out)
    # 뒷면 페르소나 이름
    out = re.sub(r'<div class="name">\s*<span class="accent">Driver</span>\s*</div>',
                 f'<div class="name">The <span class="accent">{p["name"]}</span></div>', out)
    # 뒷면 4가지 인사이트
    out = re.sub(r'<div class="detail-body">기회를 발견하고 빠르게 실행하는.*?</div>',
                 f'<div class="detail-body">{p["strength"]}</div>', out, count=1, flags=re.DOTALL)
    out = re.sub(r'<div class="detail-body">준비 부족인 상태에서.*?</div>',
                 f'<div class="detail-body">{p["pitfall"]}</div>', out, count=1, flags=re.DOTALL)
    out = re.sub(r'<div class="detail-body">I형\(분석\) · C형\(체계\) 페르소나가.*?</div>',
                 f'<div class="detail-body">{p["match"]}</div>', out, count=1, flags=re.DOTALL)
    out = re.sub(r'<div class="detail-body">"성과를 숫자로".*?</div>',
                 f'<div class="detail-body">{p["advice"]}</div>', out, count=1, flags=re.DOTALL)
    # 뒷면 직무 매칭 (기존 5개 행을 통째로 치환)
    out = re.sub(r'<div class="match-list">.*?</div>\s*</div>\s*<div class="foot">',
                 f'<div class="match-list">{jobs_html_rows}</div></div><div class="foot">',
                 out, flags=re.DOTALL)

    return out


async def build_one(persona_key: str, theme: str = "dark"):
    """페르소나 1개 PDF 생성."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    template_file = TEMPLATE_DIR / f"card_{theme}.html"
    template_html = template_file.read_text(encoding="utf-8")
    rendered = render_template(template_html, persona_key)

    # 임시 HTML 저장 → Playwright가 file:// 로 읽음
    tmp_html = OUTPUT_DIR / f"_tmp_{persona_key}_{theme}.html"
    tmp_html.write_text(rendered, encoding="utf-8")

    p = PERSONA_DATA["personas"][persona_key]
    safe_name = re.sub(r'[^a-zA-Z0-9]', '', p["name"])
    pdf_out = OUTPUT_DIR / f"card_{persona_key}_{safe_name}_{theme}.pdf"

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"file://{tmp_html.absolute()}", wait_until="networkidle")
        await page.wait_for_timeout(600)
        await page.pdf(
            path=str(pdf_out),
            width="105mm", height="148mm",
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            print_background=True,
            prefer_css_page_size=True,
        )
        await browser.close()

    tmp_html.unlink()  # 임시 파일 정리
    print(f"  ✓ {pdf_out.name}")
    return pdf_out


async def build_all(theme: str = "both"):
    """14개 페르소나 × (DARK/LIGHT) 일괄 생성."""
    themes = ["dark", "light"] if theme == "both" else [theme]
    keys = list(PERSONA_DATA["personas"].keys())
    print(f"\n페르소나 {len(keys)}개 × 톤 {len(themes)}개 = {len(keys) * len(themes)}개 PDF 생성")
    print(f"출력: {OUTPUT_DIR}\n")

    for t in themes:
        print(f"[{t.upper()}]")
        for k in keys:
            await build_one(k, t)
    print(f"\n✓ 완료. {OUTPUT_DIR.absolute()}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="모든 페르소나 생성")
    parser.add_argument("--persona", type=str, help="특정 페르소나 키 (예: E2, S1)")
    parser.add_argument("--theme", type=str, default="both", choices=["dark", "light", "both"])
    args = parser.parse_args()

    if args.all:
        asyncio.run(build_all(args.theme))
    elif args.persona:
        if args.theme == "both":
            for t in ["dark", "light"]:
                asyncio.run(build_one(args.persona, t))
        else:
            asyncio.run(build_one(args.persona, args.theme))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
