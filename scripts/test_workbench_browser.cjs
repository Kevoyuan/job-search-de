// Run with PLAYWRIGHT_MODULE pointing to an installed playwright module if needed.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const {pathToFileURL} = require('node:url');
const {resolve} = require('node:path');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const file = resolve(process.argv[2]);
const html = fs.readFileSync(file, 'utf8');
for (const match of html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)) new vm.Script(match[1]);
(async () => {
  const browser = await chromium.launch({headless: true});
  try {
    const page = await browser.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    await page.goto(pathToFileURL(file).href);
    const expected = await page.evaluate(() => JOBS.filter(j => hasScore(j) && j.score >= 75).length);
    assert.equal(Number(await page.locator('#highFitCount').textContent()), expected);
    for (const [lang, label] of [['zh', '未评分'], ['en', 'Unrated'], ['de', 'Unbewertet']]) {
      await page.evaluate(lang => {
        if (!JOBS.some(j => j.id === 'test-unrated')) {
          JOBS.push({id: 'test-unrated', title: 'Unrated fixture', score: null});
          JOBS.push({id: 'test-zero', title: 'Zero fixture', score: 0});
        }
        switchLanguage(lang); renderTable(); renderKanban(); filterJobs();
      }, lang);
      assert.equal(await page.locator('[data-id="test-unrated"] .score-badge').first().textContent(), label);
      assert.equal(await page.locator('[data-id="test-zero"] .score-badge').first().textContent(), '0');
      await page.evaluate(() => openJobDetailById('test-unrated'));
      assert.ok((await page.locator('#jobDetailScoreBadge').textContent()).endsWith(label));
      await page.evaluate(() => closeJobDetail());
      for (const order of ['asc', 'desc']) {
        await page.evaluate(order => {currentSort = {field: 'score', order}; renderTable();}, order);
        assert.equal(await page.locator('#jobsTableBody tr').last().getAttribute('data-id'), 'test-unrated');
      }
      await page.selectOption('#scoreFilter', '75');
      assert.equal(await page.locator('#jobsTableBody tr:visible').count(), expected);
      await page.selectOption('#scoreFilter', '0');
      await page.evaluate(() => switchView('kanban'));
      assert.ok(await page.locator('#kanbanView').isVisible());
      assert.equal(await page.locator('.kanban-card[data-id="test-unrated"] .score-badge').textContent(), label);
      await page.evaluate(() => switchView('table'));
      await page.evaluate(() => openConfigDrawer());
      assert.ok(await page.locator('#configDrawer').evaluate(el => el.classList.contains('open')));
      await page.evaluate(() => closeConfigDrawer());
      for (const theme of ['notion', 'obsidian', 'bauhaus', 'bento']) {
        await page.evaluate(theme => switchTheme(theme), theme);
        assert.equal(await page.locator('html').getAttribute('data-theme'), theme);
      }
    }
    for (const lang of ['zh', 'en', 'de']) {
      const content = await page.evaluate(lang => {
        switchLanguage(lang);
        const job = {id: 'analysis-fixture', title: 'Analysis fixture', score: 89,
          reason: '<img src=x onerror=alert(1)> Evidence', gap: 'Experience gap',
          jd: 'German C1', salary: 'Not published', reasonEn: 'English evidence'};
        openJobDetail(job);
        return ['Strengths', 'Gaps', 'Requirements', 'Salary'].map(name => document.getElementById('jobDetail' + name).textContent);
      }, lang);
      assert.deepEqual(content, [lang === 'en' ? 'English evidence' : '<img src=x onerror=alert(1)> Evidence', 'Experience gap', 'German C1', 'Not published']);
      assert.equal(await page.locator('#jobDetailStrengths img').count(), 0);
      await page.evaluate(() => closeJobDetail());
    }
    await page.locator('#jobsTableBody .btn-detail-trigger').first().click();
    assert.equal(await page.locator('.job-analysis-row .analysis-panel:visible').count(), 2);
    await page.fill('#searchInput', 'hide-inline-analysis-fixture');
    await page.evaluate(() => filterJobs());
    assert.equal(await page.locator('.job-analysis-row:visible').count(), 0);
    await page.fill('#searchInput', '');
    await page.evaluate(() => filterJobs());
    assert.equal(await page.locator('.job-analysis-row:visible').count(), 1);
    await page.locator('#jobsTableBody .btn-detail-trigger').first().click();
    assert.equal(await page.locator('.job-analysis-row:visible').count(), 0);
    await page.evaluate(() => renderTable());
    const boundary = await page.evaluate(() => {
      const now = new Date(2026, 8, 20, 0, 15);
      return ['2026-09-20', '2026-09-16', '2026-09-15', '2026-09-21', '', '2026-02-30']
        .map(addedOn => isRecentSearch({addedOn}, 5, now));
    });
    assert.deepEqual(boundary, [true, true, false, false, false, false]);
    await page.fill('#recentSearchDays', '3');
    await page.locator('#recentSearchDays').dispatchEvent('change');
    await page.reload();
    assert.equal(await page.inputValue('#recentSearchDays'), '3');
    const recent = await page.evaluate(() => JOBS.filter(job => isRecentSearch(job)).length);
    assert.equal(Number(await page.locator('#recentSearchCount').textContent()), recent);
    assert.equal(await page.locator('#recentSearchBody .recent-card').count(), recent);
    const columns = await page.locator('#recentSearchBody').evaluate(el => getComputedStyle(el).gridTemplateColumns.split(' ').length);
    assert.equal(await page.locator('.recent-card:visible').count(), Math.min(recent, columns * 2));
    if (recent > columns * 2) {
      await page.locator('#recentSearchExpand').click();
      assert.equal(await page.locator('.recent-card:visible').count(), recent);
      await page.locator('#recentSearchExpand').click();
    }
    if (recent) {
      await page.locator('.recent-card').first().click();
      assert.ok(await page.locator('#jobDetailDrawer').evaluate(el => el.classList.contains('open')));
      await page.evaluate(() => closeJobDetail());
    }
    const totalRows = await page.locator('#jobsTableBody tr:visible').count();
    await page.evaluate(() => switchView('kanban'));
    assert.ok(await page.locator('#recentSearchSection').isVisible());
    assert.equal(await page.locator('#recentSearchBody .recent-card').count(), recent);
    await page.evaluate(() => switchView('table'));
    await page.fill('#searchInput', 'no-results-fixture-xxxxxxxx');
    await page.evaluate(() => filterJobs());
    assert.equal(await page.locator('#jobsTableBody tr:visible').count(), 0);
    assert.equal(await page.locator('#recentSearchBody .recent-card').count(), recent);
    assert.ok(await page.locator('#recentSearchDays').isVisible());
    await page.fill('#searchInput', '');
    await page.evaluate(() => filterJobs());
    assert.equal(await page.locator('#jobsTableBody tr:visible').count(), totalRows);
    const empty = await page.evaluate(() => {
      const original = JOBS.map(j => j.addedOn);
      JOBS.forEach(j => j.addedOn = undefined);
      renderRecentSearchResults();
      const empty = !document.getElementById('recentSearchEmpty').hidden;
      JOBS.forEach((j, i) => j.addedOn = original[i]);
      renderRecentSearchResults();
      return empty;
    });
    assert.equal(empty, true);
    await page.evaluate(() => resetRecentSearchDays());
    assert.equal(await page.inputValue('#recentSearchDays'), String(await page.evaluate(() => configuredRecentDays())));
    assert.equal(await page.evaluate(() => localStorage.getItem('job_workbench_recent_search_days')), null);
    await page.setViewportSize({width: 390, height: 844});
    for (const view of ['table', 'kanban']) {
      await page.evaluate(view => switchView(view), view);
      const sizes = await page.evaluate(() => [document.documentElement.scrollWidth, window.innerWidth]);
      assert.ok(sizes[0] <= sizes[1] + 1, `${view} mobile overflow: ${sizes}`);
    }
    assert.deepEqual(errors, []);
    console.log(`PASS: syntax, ${expected} high-fit jobs, scores, filters, sorting, 3 languages, 4 themes, drawers, kanban, recent-day boundaries/persistence/filtering, mobile`);
  } finally { await browser.close(); }
})().catch(error => {console.error(error); process.exitCode = 1;});
