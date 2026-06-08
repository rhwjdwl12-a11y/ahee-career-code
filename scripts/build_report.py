"""
build_report.py
-----------------
v0.2 정규 결과지 (A4 3페이지) PDF 생성 스크립트

현재 버전은 E2 The Driver 샘플 결과를 사용. 추후 실제 응답 데이터를
받아서 동적으로 생성하도록 확장 예정 (P2 - 자동 결과지).

사용법:
  python scripts/build_report.py [--persona E2]

출력: output/reports/report_{personaKey}.pdf
"""

import asyncio
import argparse
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = ROOT / "templates"
OUTPUT_DIR = ROOT / "output" / "reports"


async def build_report(persona_key: str = "E2"):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    template_file = TEMPLATE_DIR / "report.html"
    pdf_out = OUTPUT_DIR / f"report_{persona_key}.pdf"

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page(viewport={"width": 794, "height": 1123})
        await page.goto(f"file://{template_file.absolute()}", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        await page.pdf(
            path=str(pdf_out),
            width="210mm", height="297mm",
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            print_background=True,
            prefer_css_page_size=True,
        )
        await browser.close()

    print(f"[OK] {pdf_out}")
    return pdf_out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--persona", type=str, default="E2")
    args = parser.parse_args()
    asyncio.run(build_report(args.persona))


if __name__ == "__main__":
    main()
