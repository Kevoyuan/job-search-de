const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const file = path.resolve(process.argv[2]);
const screenshots = process.argv[3];
(async () => {
  const browser = await chromium.launch({headless: true});
  try {
    const context = await browser.newContext({viewport: {width: 1440, height: 1000}, timezoneId: 'Europe/Berlin', reducedMotion: 'reduce'});
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    await page.goto(pathToFileURL(file).href);
    await page.evaluate(() => {
      switchLanguage('en');
      const fixture = {company:'Test company', title:'Tracking fixture', score:85, scoreStage:'evidence', eligibility:{status:'NOT_EXCLUDED'}, url:'https://example.test',reason:'Python experience',gap:'Confirm language',jd:'Python',salary:'Not recorded'};
      JOBS.splice(0, JOBS.length, ...['legacy','due','future','offer','unverified'].map(id => ({...fixture,id, title:id, scoreStage:id==='unverified'?'unverified':'evidence'})));
      localStorage.setItem('job_status_legacy','prep');
      localStorage.setItem('job_note_legacy','Existing note');
      localStorage.setItem('job_note_orphan','Orphan note');
      writeApplication('due',{status:'applied',followUpOn:trackingToday()});
      writeApplication('future',{status:'applied',followUpOn:'2099-01-01'});
      writeApplication('offer',{status:'offer',followUpOn:'2020-01-01'});
      renderJobs();
    });
    assert.deepEqual(await page.evaluate(() => Object.fromEntries(Object.entries(todayActionGroups()).map(([k,v])=>[k,v.map(j=>j.id)]))), {due:['due'],prep:['legacy'],review:[]});
    await page.locator('#todayActions button').filter({hasText:'legacy'}).click();
    assert.equal(await page.locator('#jobNotesInput').inputValue(), 'Existing note');
    await page.locator('#statusBtn-applied').click();
    assert.equal(await page.locator('#application-appliedOn').inputValue(), await page.evaluate(()=>trackingToday()));
    await page.locator('#application-appliedOn').fill('2026-11-10');
    await page.locator('#application-appliedOn').dispatchEvent('change');
    await page.locator('#application-followUpOn').fill('2026-11-12');
    await page.locator('#application-followUpOn').dispatchEvent('change');
    await page.locator('#application-contact').fill('Recruiter <script>unsafe</script>');
    await page.locator('#application-contact').dispatchEvent('change');
    await page.locator('#jobNotesInput').fill('Updated note');
    assert.equal(await page.locator('#applicationHistory li').count(),1);
    assert.equal(await page.locator('#trackingDetailNotice').textContent(),'Saved in this browser');
    await page.evaluate(()=>closeJobDetail());
    const downloadEvent = page.waitForEvent('download');
    await page.locator('[data-tracking="export"]').click();
    const download = await downloadEvent;
    const backup = JSON.parse(fs.readFileSync(await download.path(), 'utf8'));
    assert.equal(backup.records.legacy.notes,'Updated note');
    assert.equal(backup.records.orphan.notes,'Orphan note');
    assert.equal(backup.records.legacy.appliedOn,'2026-11-10');
    await page.reload();
    assert.equal(await page.evaluate(()=>applicationRecord('legacy').contact),'Recruiter <script>unsafe</script>');
    const freshContext = await browser.newContext();
    const fresh = await freshContext.newPage();
    await fresh.goto(pathToFileURL(file).href);
    fresh.on('dialog', d=>d.accept());
    await fresh.locator('#applicationImport').setInputFiles({name:'applications.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(backup))});
    await fresh.waitForFunction(()=>document.getElementById('trackingNotice').textContent === trackingText().restored);
    assert.equal(await fresh.evaluate(()=>applicationRecord('legacy').notes),'Updated note');
    await fresh.evaluate(()=>writeApplication('legacy',{notes:'Keep existing'}));
    await fresh.locator('#applicationImport').setInputFiles({name:'applications.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(backup))});
    await fresh.waitForFunction(()=>document.getElementById('trackingNotice').textContent === trackingText().restored);
    assert.equal(await fresh.evaluate(()=>applicationRecord('legacy').notes),'Keep existing');
    const before = await fresh.evaluate(()=>localStorage.getItem(TRACKING_KEY));
    await fresh.locator('#applicationImport').setInputFiles({name:'bad.json',mimeType:'application/json',buffer:Buffer.from('{invalid')});
    await fresh.waitForFunction(()=>document.getElementById('trackingNotice').textContent === trackingText().invalid);
    assert.equal(await fresh.evaluate(()=>localStorage.getItem(TRACKING_KEY)),before);
    await freshContext.close();
    for (const lang of ['zh','en','de']) {
      await page.evaluate(lang=>switchLanguage(lang),lang);
      assert.equal(await page.locator('#todayTitle').textContent(), await page.evaluate(()=>trackingText().title));
      for (const width of [1440,390]) {
        await page.setViewportSize({width,height:900});
        assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`overflow ${lang} ${width}`);
        await page.evaluate(()=>openJobDetail(JOBS[0]));
        await page.locator('#application-contact').waitFor({state:'visible'});
        assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
        await page.evaluate(()=>closeJobDetail());
      }
    }
    if (screenshots) {
      fs.mkdirSync(screenshots,{recursive:true});
      await page.evaluate(()=>switchLanguage('zh'));
      await page.setViewportSize({width:1440,height:1000});
      await page.screenshot({path:path.join(screenshots,'tracking-desktop.png')});
      await page.setViewportSize({width:390,height:844});
      await page.screenshot({path:path.join(screenshots,'tracking-mobile.png')});
      await page.evaluate(()=>openJobDetail(JOBS[0]));
      await page.locator('#application-followUpOn').scrollIntoViewIfNeeded();
      await page.screenshot({path:path.join(screenshots,'tracking-detail-mobile.png')});
    }
    assert.deepEqual(errors,[]);
    console.log('PASS: legacy edit, dates/history, real download, restore in fresh browser, conflict preservation, invalid import, reload persistence, 3 languages, mobile/desktop, no page errors');
  } finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exit(1)});
