const assert=require('node:assert/strict');
const {resolve}=require('node:path');
const {pathToFileURL}=require('node:url');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
(async()=>{const browser=await chromium.launch();try{
 const page=await browser.newPage();await page.goto(pathToFileURL(resolve(process.argv[2]||'job-hunt-workbench.html')).href);
 const result=await page.evaluate(()=>{
  const state=()=>({config:document.querySelector('#configDrawer').classList.contains('open'),docs:document.querySelector('#docsDrawer').classList.contains('open'),theme:document.documentElement.dataset.theme,view:currentJobView});
  const before=JSON.stringify(state());const failures=[];
  for(const modifier of ['ctrlKey','metaKey','altKey'])for(const key of ['c','C','t','k','g','1','/','?']){
   const event=new KeyboardEvent('keydown',{key,[modifier]:true,bubbles:true,cancelable:true});document.body.dispatchEvent(event);
   if(event.defaultPrevented||JSON.stringify(state())!==before)failures.push(`${modifier}/${key}`);
  }
  const edit=document.createElement('div');edit.contentEditable='true';document.body.append(edit);edit.dispatchEvent(new KeyboardEvent('keydown',{key:'c',bubbles:true}));const editableProtected=!state().config;edit.remove();
  document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'c',isComposing:true,bubbles:true}));const composingProtected=!state().config;
  document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'c',bubbles:true}));const bareC=state().config;
  const oldSave=saveCurrentConfig;let saves=0;saveCurrentConfig=()=>{saves++;};
  const save=new KeyboardEvent('keydown',{key:'s',ctrlKey:true,bubbles:true,cancelable:true});document.body.dispatchEvent(save);
  const shiftSave=new KeyboardEvent('keydown',{key:'s',ctrlKey:true,shiftKey:true,bubbles:true,cancelable:true});document.body.dispatchEvent(shiftSave);
  closeConfigDrawer();const browserSave=new KeyboardEvent('keydown',{key:'s',ctrlKey:true,bubbles:true,cancelable:true});document.body.dispatchEvent(browserSave);saveCurrentConfig=oldSave;
  return {failures,editableProtected,composingProtected,bareC,saves,savePrevented:save.defaultPrevented,shiftSavePrevented:shiftSave.defaultPrevented,browserSavePrevented:browserSave.defaultPrevented};
 });
 assert.deepEqual(result.failures,[]);assert.ok(result.editableProtected);assert.ok(result.composingProtected);assert.ok(result.bareC);assert.equal(result.saves,1);assert.ok(result.savePrevented);assert.equal(result.shiftSavePrevented,false);assert.equal(result.browserSavePrevented,false);
 await page.locator('body').focus();await page.keyboard.press('Control+c');assert.equal(await page.locator('#configDrawer').evaluate(el=>el.classList.contains('open')),false);
 await page.keyboard.press('Meta+c');assert.equal(await page.locator('#configDrawer').evaluate(el=>el.classList.contains('open')),false);
 console.log('PASS: Ctrl/Meta copy and browser combinations preserved; bare C, editable/IME guards and configuration-only save verified.');
}finally{await browser.close();}})().catch(error=>{console.error(error);process.exit(1);});
