// Physical SVG sizing and full-label regression coverage, including real collections.
const assert=require('node:assert/strict');
const {resolve}=require('node:path');
const {pathToFileURL}=require('node:url');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
(async()=>{
 const browser=await chromium.launch();
 try {
  const page=await browser.newPage({reducedMotion:'reduce'});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(pathToFileURL(resolve(process.argv[2]||'job-hunt-workbench.html')).href+'#analysis');
  await page.locator('[data-time-scope]').selectOption('all');
  await page.locator('[data-distribution]').selectOption('cities');
  await page.evaluate(()=>document.fonts.ready);
  // Include long words and mixed scripts without changing production fixture files.
  await page.evaluate(()=>{const j=JOBS[0];j.analytics.industry='Forschung und Entwicklung / 超长行业名称 / CloudInfrastructureEngineering';});
  for(const width of [390,1440,1728,320]){
   await page.setViewportSize({width,height:1000});
   for(const lang of ['zh','en','de']){
    await page.selectOption('#langSelector',lang);
    for(const theme of ['notion','dark','obsidian','bauhaus','bento']){
     await page.selectOption('#themeSelector',theme);
     for(const key of ['cities','industry','role','technologies','workModel']){
      await page.locator('[data-action="tab"][data-key="distribution"]').click();
      await page.locator('[data-distribution]').selectOption(key);
      await page.locator('#lf-distribution').scrollIntoViewIfNeeded();
      await page.waitForFunction(()=>document.querySelector('#lf-distribution text'));
      const result=await page.locator('#lf-distribution').evaluate(svg=>{
       const box=svg.getBoundingClientRect(),view=svg.viewBox.baseVal;
       return {scale:box.width/view.width,font:[...svg.querySelectorAll('text')].map(n=>parseFloat(getComputedStyle(n).fontSize)),outside:[...svg.querySelectorAll('text')].some(n=>{const b=n.getBBox();return b.x<-.5||b.x+b.width>view.width+.5||b.y<-.5||b.y+b.height>view.height+.5;})};
      });
      assert.ok(Math.abs(result.scale-1)<.01,`${width}/${lang}/${theme}/${key} scaled SVG`);
      assert.ok(result.font.every(n=>n>=12),`${width}/${lang}/${theme}/${key} legible labels: ${result.font}`);
      assert.equal(result.outside,false,`${width}/${lang}/${theme}/${key} clipped label`);
     }
     await page.locator('[data-action="tab"][data-key="cross"]').click();
     for(const key of ['locationRole','roleTech']){
      await page.locator('[data-cross]').selectOption(key);
      await page.locator('#lf-matrix').scrollIntoViewIfNeeded();
      await page.waitForFunction(()=>document.querySelector('#lf-matrix text'));
      assert.ok(await page.locator('#lf-matrix').evaluate(svg=>Math.abs(svg.getBoundingClientRect().width/svg.viewBox.baseVal.width-1)<.01));
      assert.equal(await page.locator('#lf-matrix text[transform]').count(),0,'horizontal column labels');
      assert.ok(await page.locator('#lf-matrix').evaluate(svg=>[...svg.querySelectorAll('text')].every(n=>{const b=n.getBBox(),v=svg.viewBox.baseVal;return b.x>=-.5&&b.x+b.width<=v.width+.5&&b.y>=-.5&&b.y+b.height<=v.height+.5;})),'matrix label bounds');
      assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'document reflow');
     }
    }
   }
  }
  await page.setViewportSize({width:390,height:600});
  const scroll=page.locator('#lf-matrix').locator('..');
  await scroll.evaluate(el=>el.scrollLeft=0);await scroll.focus();await page.keyboard.press('ArrowRight');
  await page.waitForFunction(()=>document.querySelector('#lf-matrix').parentElement.scrollLeft>0);
  await page.locator('[data-action="tab"][data-key="distribution"]').click();
  await page.setViewportSize({width:1440,height:1000});
  await page.locator('[data-distribution]').selectOption('cities');
  await page.locator('#analyticsView').scrollIntoViewIfNeeded();
  const gap=await page.evaluate(()=>document.querySelector('#lf-distribution').getBoundingClientRect().top-document.querySelector('#analyticsView').getBoundingClientRect().top);
  assert.ok(gap<260,`compact header: ${gap}`);
  // 200% desktop zoom: CSS zoom emulates the physical layout/reflow constraint.
  await page.evaluate(()=>document.documentElement.style.zoom='2');
  await page.waitForTimeout(100);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'200% reflow');
  assert.deepEqual(errors,[]);
  console.log('Analytics layout passed: physical SVG scale, full label bounds, 3 locales, 5 themes, 4 widths, keyboard scrolling and 200% reflow.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1);});
