import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch()
    for name,vp in [('desk',{'width':1300,'height':1400}),('mob',{'width':390,'height':1600})]:
      pg=await b.new_page(viewport=vp);errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
      await pg.goto('file:///home/claude/fp2026/web/index.html')
      await pg.wait_for_function("document.querySelectorAll('.match').length>0||document.querySelector('.empty')",timeout=60000)
      await pg.click('[data-t="acca"]:visible');await pg.wait_for_timeout(800)
      print(name,errs,(await pg.inner_text('#view'))[:500].replace('\n',' | '))
      await pg.screenshot(path=f'acca_{name}.png')
    await b.close()
asyncio.run(main())
