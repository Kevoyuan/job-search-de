// Local configuration editing must never invoke a model or corrupt unrelated source.
const assert = require('node:assert/strict');
const {resolve} = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
(async () => {
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage({reducedMotion: 'reduce'});
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    await page.goto(pathToFileURL(resolve(process.argv[2] || 'job-hunt-workbench.html')).href);
    await page.evaluate(() => {switchLanguage('en'); openConfigDrawer();});
    assert.equal(await page.evaluate(() => currentEditorMode), 'form');
    const requests = [];
    page.on('request', r => requests.push(r.url()));
    const markdown = '# Profile\r\n\r\n## Facts\r\n- Name: Ada\r\n- Languages:\r\n\r\n## Evidence\r\nA paragraph <img src=x onerror=alert(1)>\r\n\r\n```md\r\n## Not a section\r\n- Code: untouched\r\n```\r\n';
    await page.evaluate(text => {configData.profile = text; loadConfigTabContent();}, markdown);
    assert.equal(await page.locator('.config-card').count(), 3);
    assert.equal(await page.locator('#configSections img').count(), 0);
    await page.getByLabel('Name', {exact: true}).fill('Ada Lovelace');
    await page.getByLabel('Languages', {exact: true}).fill('English, Deutsch');
    const edited = markdown.replace('Name: Ada', 'Name: Ada Lovelace').replace('Languages:', 'Languages:English, Deutsch');
    assert.equal(await page.evaluate(() => configData.profile), edited);
    await page.evaluate(() => {switchConfigTab('preferences'); switchConfigTab('profile'); setEditorMode('source');});
    assert.equal(await page.locator('#configTextarea').inputValue(), edited.replace(/\r\n/g, '\n'));
    await page.locator('#configTextarea').fill(edited.replace('Ada Lovelace', 'Grace Hopper'));
    await page.evaluate(() => setEditorMode('form'));
    assert.equal(await page.getByLabel('Name', {exact: true}).inputValue(), 'Grace Hopper');
    await page.evaluate(() => {closeConfigDrawer(); openConfigDrawer();});
    assert.equal(await page.getByLabel('Name', {exact: true}).inputValue(), 'Grace Hopper');
    const ini = '; keep this\r\n[thresholds]\r\ntriage_keep = 65 ; note\r\ndeep_score = 75\r\nhigh_value_fit = 80\r\n[custom]\r\ntriage_keep = 123\r\nunknown = keep\r\n[delivery]\r\nworkbench = true\r\n';
    await page.evaluate(text => {configData.settings = text; switchConfigTab('settings');}, ini);
    const score = page.getByLabel('triage_keep', {exact: true}).first();
    await score.fill('101');
    assert.equal(await score.getAttribute('aria-invalid'), 'true');
    await page.evaluate(() => setEditorMode('source'));
    assert.equal(await page.evaluate(() => currentEditorMode), 'form');
    assert.equal(await page.evaluate(() => configData.settings), ini);
    await score.fill('70');
    await page.getByLabel('workbench', {exact: true}).selectOption('false');
    assert.equal(await page.evaluate(() => configData.settings), ini.replace('65 ; note', '70 ; note').replace('workbench = true', 'workbench = false'));
    assert.equal(await page.locator('meter').count(), 3);
    for (const width of [390, 1440, 1728]) {
      await page.setViewportSize({width, height: 900});
      for (const lang of ['en', 'zh', 'de']) {
        await page.evaluate(lang => switchLanguage(lang), lang);
        for (const tab of ['profile', 'preferences', 'settings']) {
          await page.evaluate(tab => switchConfigTab(tab), tab);
          const overflow = await page.locator('#configDrawer').evaluate(el => el.scrollWidth > el.clientWidth);
          assert.equal(overflow, false, `${width}/${lang}/${tab} overflow`);
        }
      }
    }
    await page.evaluate(() => {configData.profile = ''; switchConfigTab('profile');});
    assert.equal(await page.locator('#configSections button').count(), 1);
    assert.equal(requests.length, 0, 'config UI must perform no network requests');
    assert.deepEqual(errors, []);
    console.log('PASS: zero-request rendering, complete source preservation, CRLF/comments/fences/XSS, edit round trips, validation, boolean controls, drafts, 3 locales × 3 widths × 3 tabs, empty state');
  } finally {await browser.close();}
})().catch(e => {console.error(e); process.exitCode = 1;});
