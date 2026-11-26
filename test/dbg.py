import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page()
    await pg.goto('file:///home/claude/fp2026/web/index.html');await pg.wait_for_timeout(1500)
    print(await pg.evaluate("[...document.querySelectorAll('.grp')].slice(0,6).map(g=>g.textContent).join(' | ')"))
    print(await pg.evaluate("[...document.querySelectorAll('.match .time')].slice(0,4).map(g=>g.textContent).join(' | ')"))
    await b.close()
asyncio.run(main())
