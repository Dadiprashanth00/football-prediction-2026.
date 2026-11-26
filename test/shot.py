import sys,asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch()
    for name,vp in [('desk',{'width':1400,'height':950}),('mob',{'width':390,'height':844})]:
      pg=await b.new_page(viewport=vp)
      errs=[]
      pg.on('pageerror',lambda e:errs.append(str(e)))
      pg.on('console',lambda m:errs.append('console:'+m.text) if m.type=='error' else None)
      await pg.goto('file:///home/claude/fp2026/web/index.html')
      await pg.wait_for_timeout(2500)
      await pg.screenshot(path=f'/home/claude/fp2026/test/{name}_today.png')
      n=await pg.evaluate("document.querySelectorAll('.match').length")
      print(name,'cards',n,'errs',errs[:5])
      await pg.click('.match')
      await pg.wait_for_timeout(600)
      await pg.screenshot(path=f'/home/claude/fp2026/test/{name}_sheet.png')
      await pg.screenshot(path=f'/home/claude/fp2026/test/{name}_sheet_full.png',full_page=False)
      await pg.keyboard.press('Escape')
      for t in ['table','acc','res']:
        await pg.click(f'[data-t="{t}"]:visible') if name=='desk' else await pg.click(f'nav.bot [data-t="{t}"]')
        await pg.wait_for_timeout(400)
        await pg.screenshot(path=f'/home/claude/fp2026/test/{name}_{t}.png')
      print(name,'errs after',errs[:5])
    await b.close()
asyncio.run(main())
