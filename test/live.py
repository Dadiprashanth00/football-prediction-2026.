import asyncio
from playwright.async_api import async_playwright
JS='''()=>{const m={id:'es1',comp:'CL',home:'Club Brugge',away:'Liverpool',utc:new Date(Date.now()-75*60000).toISOString(),status:'LIVE',minute:'60',hg:0,ag:1};
const P=FPT.predict(m,{});
const S={st:{h:{possessionPct:58,totalShots:11,shotsOnTarget:4,blockedShots:4,wonCorners:6,accurateCrosses:4,accuratePasses:300,passPct:.82,yellowCards:1,redCards:0,foulsCommitted:6},a:{possessionPct:42,totalShots:6,shotsOnTarget:3,blockedShots:1,wonCorners:2,accurateCrosses:2,accuratePasses:210,passPct:.78,yellowCards:2,redCards:1,foulsCommitted:9}},
events:[{min:"13'",type:'Goal',side:'a',text:'Goal! Club Brugge 0, Liverpool 1.'},{min:"55'",type:'Red Card',side:'a',text:'Red card for a Liverpool player'}],
comm:[{min:48,kind:'sot',side:'h'},{min:50,kind:'corner',side:'h'},{min:52,kind:'shot',side:'h'},{min:57,kind:'shot',side:'a'},{min:58,kind:'sot',side:'h'}],detail:"60'",state:'in',period:2};
document.body.innerHTML='<div class="sheet on" style="position:static;transform:none;width:760px">'+FPT.liveSection(m,P,S)+'</div>';
const L=FPT.liveAnalysis(m,P,S);return JSON.stringify({p1:L.p1,px:L.px,p2:L.p2,sum:L.p1+L.px+L.p2,next:[L.nextH,L.nextNone,L.nextA],mom:L.mom,ctrl:L.ctrl,proj:L.proj})}'''
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':800,'height':1500})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto('file:///home/claude/fp2026/test/t.html');await pg.wait_for_timeout(1500)
    print(await pg.evaluate(JS));print('errs',errs)
    await pg.screenshot(path='live.png',full_page=True)
    await b.close()
asyncio.run(main())
