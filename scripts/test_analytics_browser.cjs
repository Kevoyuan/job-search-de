const assert = require('node:assert/strict');
const fs = require('node:fs');
const {resolve} = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
(async()=>{
  const browser=await chromium.launch({headless:true});
  try {
    const page=await browser.newPage({viewport:{width:1440,height:1000}});
    const errors=[];page.on('pageerror',e=>errors.push(e.message));
    await page.goto(pathToFileURL(resolve(process.argv[2]||'job-hunt-workbench.html')).href);
    await page.locator('#analyticsViewButton').click();
    await page.locator('[data-time-scope]').selectOption('all');
    assert.ok(await page.locator('#analyticsView').isVisible());
    assert.equal(await page.locator('#tableView').isVisible(),false);
    assert.equal(await page.locator('#jobViewControls').isVisible(),false);
    assert.equal(await page.locator('.analytics-radar').count(),0);
    assert.equal(await page.locator('[data-action="tab"]').count(),2);
    const pure=await page.evaluate(()=>{
      const a={analytics:{cities:['Munich','Munich'],role:'Backend',technologies:[{name:'Java'}]}};
      const b={analytics:{cities:['Berlin'],role:'Backend',technologies:[{name:'JavaScript'}]}};
      const c={analytics:{}};
      return {cities:countFacet([a,b,c],'cities'),cross:matrixCount([a,b,c],'cities','Munich','role','Backend'),unknown:facetValues(c,'role')};
    });
    assert.equal(pure.cities.find(x=>x[0]==='Munich')[1],1);
    assert.equal(pure.cross,1);assert.deepEqual(pure.unknown,['__unknown__']);
    const detailed=await page.evaluate(()=>{
      const jobs=[{analytics:{cities:[],locationTags:['__location_remote__'],technologies:[],technologyStatus:'language_only'}},
        {analytics:{cities:['Berlin','Munich'],locationTags:['Berlin','Munich','__location_multiple__'],technologies:[{name:'Python',category:'languages'}],technologyGroups:['languages'],technologyStatus:'specific'}},
        {analytics:{technologies:[],technologyStatus:'no_description'}}];
      const d=distributionData(jobs,'technologies');
      return {remote:facetValues(jobs[0],'cities'),multiple:facetValues(jobs[1],'cities'),known:d.known,missing:d.missing,missingReasons:d.missingEntries.map(([v])=>v),groups:facetValues(jobs[1],'technologyGroups')};
    });
    assert.deepEqual(detailed.remote,['__location_remote__']);
    assert.ok(detailed.multiple.includes('__location_multiple__'));
    assert.deepEqual(detailed.known,[['Python',1]]);assert.equal(detailed.missing,2);
    assert.ok(detailed.missingReasons.includes('__tech_language_only__'));
    assert.ok(detailed.missingReasons.includes('__tech_no_description__'));
    assert.deepEqual(detailed.groups,['languages']);

    await page.locator('[data-action="tab"][data-key="distribution"]').click();
    await page.locator('[data-distribution]').selectOption('cities');
    // Native type-ahead selection must preserve focus across the local redraw.
    await page.selectOption('#langSelector','en');
    await page.locator('[data-distribution]').focus();
    await page.keyboard.press('i');
    assert.equal(await page.locator('[data-distribution]').inputValue(),'industry');
    assert.ok(await page.locator('[data-distribution]').evaluate(el=>el===document.activeElement));
    await page.locator('[data-distribution]').selectOption('cities');
    await page.locator('#lf-distribution').scrollIntoViewIfNeeded();
    await page.locator('#lf-distribution .analytics-bar').first().waitFor();
    await page.evaluate(()=>document.fonts.ready);
    assert.ok(await page.evaluate(()=>[...document.fonts].some(f=>f.family==='Inter'&&f.status==='loaded')));
    const tickCounts=await page.locator('#lf-distribution .analytics-bar').evaluateAll(rows=>rows.map(row=>({value:Number(row.dataset.count),ticks:row.querySelectorAll('.lf-tick').length})));
    assert.ok(tickCounts.every(row=>row.value===row.ticks),'each tick represents exactly one job');
    assert.ok(tickCounts.length<=8,'F5 frame has at most eight rows');
    await page.locator('[data-action="facet"][data-key="cities"][data-value="Berlin"]').click();
    const berlin=await page.evaluate(()=>JOBS.filter(j=>facetValues(j,'cities').includes('Berlin')).length);
    assert.equal(await page.locator('.analytics-count').textContent(),String(berlin));
    await page.evaluate(()=>{addAnalyticsFacet('cities','Munich');filterJobs();});
    assert.equal(await page.evaluate(()=>analyticsVisibleJobs.length),await page.evaluate(()=>JOBS.filter(j=>facetValues(j,'cities').some(c=>['Berlin','Munich'].includes(c))).length));
    await page.evaluate(()=>{addAnalyticsFacet('role','Backend');filterJobs();});
    assert.ok(await page.evaluate(()=>analyticsVisibleJobs.every(j=>j.analytics.role==='Backend')));
    await page.locator('[data-action="jobs"]').click();
    assert.equal(await page.locator('#jobsTableBody tr.job-row:visible').count(),await page.evaluate(()=>analyticsVisibleJobs.length));
    await page.locator('#analyticsViewButton').click();
    await page.evaluate(()=>resetAllFilters());
    await page.locator('[data-disclosure="distribution-values"]').evaluate(el=>el.open=true);
    await page.locator('[data-action="tab"][data-key="cross"]').click();
    assert.equal(await page.locator('[data-disclosure="matrix-options"]').evaluate(el=>el.open),false,'exact values disclosure does not accidentally open matrix controls');
    await page.locator('#lf-matrix').scrollIntoViewIfNeeded();
    await page.locator('#lf-matrix .analytics-cell').first().waitFor();
    const areas=await page.locator('#lf-matrix .analytics-cell').evaluateAll(cells=>cells.map(cell=>Number(cell.querySelector('.lf-bubble').getAttribute('r'))**2/Number(cell.dataset.count)));
    assert.ok(areas.every(area=>Math.abs(area-areas[0])<1e-8),'circle area is proportional to count');
    await page.locator('#lf-matrix .analytics-cell').first().focus();
    await page.keyboard.press('Enter');
    assert.equal(await page.evaluate(()=>Object.keys(analyticsFilters).length),2);
    await page.evaluate(()=>resetAllFilters());
    await page.locator('.analytics-cell').first().click();
    assert.equal(await page.evaluate(()=>Object.keys(analyticsFilters).length),2);
    await page.locator('#analyticsFilters [data-action="reset"]').click();
    assert.equal(await page.evaluate(()=>Object.keys(analyticsFilters).length),0);
    // Matrix multi-selection does not close the chooser or steal keyboard focus.
    await page.locator('[data-cross]').selectOption('roleTech');
    const rows=page.locator('[data-matrix="roleTech"][data-side="rows"]');
    await rows.evaluate(el=>el.closest('details').open=true);
    await rows.selectOption({index:0});
    assert.ok(await rows.isVisible());
    assert.equal(await page.evaluate(()=>analyticsMatrixSelection.roleTech.rows.length),1);
    await page.locator('[data-action="tab"][data-key="distribution"]').click();
    for(const lang of ['zh','en','de']) {
      await page.selectOption('#langSelector',lang);
      assert.equal(await page.locator('#analyticsView h1').textContent(),await page.evaluate(()=>ac().title));
      for(const theme of ['notion','dark','obsidian','bauhaus','bento']) {
        await page.selectOption('#themeSelector',theme);
        for(const width of [390,1440,1728]) {
          await page.setViewportSize({width,height:1000});
          await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
          assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`${lang}/${theme}/${width}: page overflow`);
        }
      }
    }
    await page.locator('#searchInput').fill('no-such-job-ever');
    assert.equal(await page.locator('.analytics-count').textContent(),'0');
    assert.equal(await page.locator('#emptyState').isVisible(),false);
    assert.equal(await page.locator('.analytics-bar').count(),0);
    await page.evaluate(()=>resetAllFilters());
    await page.locator('[data-action="detail"]').first().evaluate(el=>el.closest('details').open=true);
    await page.locator('[data-action="detail"]').first().click();
    assert.ok(await page.locator('#jobDetailDrawer').evaluate(el=>el.classList.contains('open')));
    await page.evaluate(()=>closeJobDetail());
    // Stored HTML-like text must never become active markup.
    await page.evaluate(()=>{JOBS[0].analytics.industry='<img src=x onerror=alert(1)>';renderAnalytics();});
    assert.equal(await page.locator('#analyticsView img').count(),0);
    assert.deepEqual(errors,[]);
    console.log('Lieflat charts and analytics checks passed: aggregate math, filters, drilldown, 45 locale/theme/viewport combinations, empty states and safe rendering.');
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exit(1);});
