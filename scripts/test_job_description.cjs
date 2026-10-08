const assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const {resolve}=require('node:path');const {pathToFileURL}=require('node:url');
(async()=>{const browser=await chromium.launch();try{const page=await browser.newPage();await page.goto(pathToFileURL(resolve(process.argv[2]||'job-hunt-workbench.html')).href);const requests=[];page.on('request',r=>requests.push(r.url()));
const cases=[['<strong>About</strong><p>Retail &amp; D2C</p><ul><li>Inventory</li><li>Reporting</li></ul>','About\nRetail & D2C\n\n• Inventory\n\n• Reporting'],['&lt;p&gt;Required &amp;amp; preferred&lt;/p&gt;','Required & preferred'],['English C1\nPython < 4 and salary > 50000','English C1\nPython < 4 and salary > 50000'],['<script>window.injected=1</script><style>hidden</style><img src="https://example.invalid/image" onerror="window.injected=1"><p>Safe</p>','Safe']];
for(const [input,expected]of cases)assert.equal(await page.evaluate(x=>readableJobDescription(x),input),expected);
assert.equal(await page.evaluate(()=>window.injected),undefined);assert.deepEqual(requests,[]);console.log('PASS: readable paragraphs/lists/entities, plain text, inert markup with no requests or script execution');}finally{await browser.close()}})().catch(e=>{console.error(e);process.exit(1)});
