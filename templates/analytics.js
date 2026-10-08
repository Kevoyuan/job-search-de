// Pure aggregation functions are shared by rendering and regression tests.
const UNKNOWN_FACET = '__unknown__';
const ANALYTICS_COPY = {
  en: {
    jobs:'Jobs', analysis:'Analysis', title:'Collected job analysis', scope:'Only your collected jobs. Charts follow the list filters.',
    cities:'Locations', industry:'Industries', role:'Job categories', technologies:'Technologies', workModel:'Work models',
    unknown:'Unknown', total:'jobs in this selection', demo:'Fictional demonstration vacancies.',
    coverage:'Data coverage', missing:'unknown', empty:'No jobs match these filters.', reset:'Reset all filters', showJobs:'View matching jobs', showAll:'Show all', showLess:'Show top 10',
    analyzed:'Analyzed', undated:'Date not recorded', required:'Required', preferred:'Preferred', mentioned:'Mentioned',
    multi:'A job may appear in several locations or technologies. Shares use all selected jobs and may total more than 100%.',
    locationRole:'Location × job category', roleTech:'Job category × technology', rows:'Rows', columns:'Columns', choose:'Choose rows and columns',
    multiSelect:'Use Ctrl / Cmd to select multiple items.', add:'Add a filter', remove:'Remove', records:'Matching jobs',
    remote:'Remote', hybrid:'Hybrid', onsite:'On-site', selected:'Selected filters', matrixHint:'Select a count to filter the matching jobs.', raw:'Stored evidence', techNote:'Levels: required / preferred / mentioned. Missing tags do not mean no technical requirements.'
  },
  zh: {
    jobs:'岗位', analysis:'分析', title:'已收录岗位分析', scope:'仅代表已收录岗位样本，图表跟随列表筛选。',
    cities:'地点分布', industry:'行业分布', role:'具体岗位', technologies:'技术需求', workModel:'工作方式',
    unknown:'未知', total:'个筛选内岗位', demo:'虚构岗位演示数据。',
    coverage:'资料覆盖', missing:'未知', empty:'没有符合筛选条件的岗位。', reset:'重置所有筛选', showJobs:'查看对应岗位', showAll:'展开全部', showLess:'显示前十项',
    analyzed:'分析时间', undated:'时间未记录', required:'必需', preferred:'加分项', mentioned:'仅提及',
    multi:'一个岗位可归入多个地点或技术。占比以筛选内全部岗位为分母，合计可能超过 100%。',
    locationRole:'地点 × 岗位类别', roleTech:'岗位类别 × 技术', rows:'行', columns:'列', choose:'选择行列',
    multiSelect:'按住 Ctrl / Cmd 可多选。', add:'添加筛选', remove:'移除', records:'对应岗位',
    remote:'远程', hybrid:'混合', onsite:'现场办公', selected:'已选筛选', matrixHint:'点击数量筛选对应岗位。', raw:'已保存依据', techNote:'要求等级：必需 / 加分项 / 仅提及。缺少标签不代表岗位没有技术要求。'
  },
  de: {
    jobs:'Stellen', analysis:'Analyse', title:'Analyse erfasster Stellen', scope:'Nur erfasste Stellen. Die Diagramme folgen den Listenfiltern.',
    cities:'Standorte', industry:'Branchen', role:'Berufskategorien', technologies:'Technologien', workModel:'Arbeitsmodelle',
    unknown:'Unbekannt', total:'Stellen in dieser Auswahl', demo:'Fiktive Beispielstellen.',
    coverage:'Datenabdeckung', missing:'unbekannt', empty:'Keine Stellen für diese Filter.', reset:'Alle Filter zurücksetzen', showJobs:'Passende Stellen anzeigen', showAll:'Alle anzeigen', showLess:'Top 10 anzeigen',
    analyzed:'Analysiert', undated:'Datum fehlt', required:'Erforderlich', preferred:'Wünschenswert', mentioned:'Erwähnt',
    multi:'Eine Stelle kann mehrere Standorte oder Technologien haben. Anteile beziehen sich auf alle ausgewählten Stellen und können zusammen über 100 % liegen.',
    locationRole:'Standort × Berufskategorie', roleTech:'Berufskategorie × Technologie', rows:'Zeilen', columns:'Spalten', choose:'Zeilen und Spalten wählen',
    multiSelect:'Mit Strg / Cmd mehrere Einträge wählen.', add:'Filter hinzufügen', remove:'Entfernen', records:'Passende Stellen',
    remote:'Remote', hybrid:'Hybrid', onsite:'Vor Ort', selected:'Aktive Filter', matrixHint:'Eine Zahl wählen, um passende Stellen zu filtern.', raw:'Gespeicherte Belege', techNote:'Stufen: erforderlich / wünschenswert / erwähnt. Fehlende Tags bedeuten nicht, dass keine Kenntnisse erforderlich sind.'
  }
};
const ROLE_CATEGORY_LABELS={
 zh:{'AI Engineering':'AI 应用与开发','Machine Learning':'机器学习工程','Forward Deployed Engineering':'前线部署工程','AI Solutions Engineering':'AI 解决方案工程','AI Consulting':'AI 技术咨询','Platform / DevOps':'平台工程 / DevOps','Backend':'后端工程','Frontend':'前端工程','Robotics':'机器人与机器人学习','Data Science':'数据科学','AI Architecture':'AI 架构','Simulation / Graphics':'仿真与图形工程','Full Stack':'全栈工程','Data Engineering':'数据工程','Product Engineering':'产品工程','AI Transformation / Enablement':'AI 转型与赋能','Software Engineering':'软件工程','MLOps / LLMOps':'机器学习与大模型运维','Data Management / Governance':'数据管理与治理','Embedded Engineering':'嵌入式工程','Research / R&D':'研究与研发','Application Engineering':'应用工程','Data Consulting':'数据与分析咨询','Solution Architecture':'解决方案架构','SRE / Cloud':'可靠性与云工程'},
 de:{'AI Engineering':'KI-Anwendungen und Entwicklung','Machine Learning':'Machine-Learning-Engineering','Forward Deployed Engineering':'Forward Deployed Engineering','AI Solutions Engineering':'KI-Lösungsengineering','AI Consulting':'KI-Beratung','Platform / DevOps':'Plattformengineering / DevOps','Backend':'Backend-Engineering','Frontend':'Frontend-Engineering','Robotics':'Robotik und Roboterlernen','Data Science':'Data Science','AI Architecture':'KI-Architektur','Simulation / Graphics':'Simulation und Grafik','Full Stack':'Full-Stack-Engineering','Data Engineering':'Data Engineering','Product Engineering':'Produktengineering','AI Transformation / Enablement':'KI-Transformation und Enablement','Software Engineering':'Softwareengineering','MLOps / LLMOps':'MLOps / LLMOps','Data Management / Governance':'Datenmanagement und Governance','Embedded Engineering':'Embedded-Engineering','Research / R&D':'Forschung und Entwicklung','Application Engineering':'Anwendungsengineering','Data Consulting':'Daten- und Analytics-Beratung','Solution Architecture':'Lösungsarchitektur','SRE / Cloud':'SRE / Cloud'}
};
const ANALYTICS_DETAIL_COPY={
 zh:{roleMissing:'岗位类别待确认',technologyGroups:'技术分类',technologyStatus:'技术资料情况',specific:'已识别具体技术',direction_only:'仅识别技术方向',language_only:'仅记录语言要求',no_description:'未保存岗位描述',unidentified:'有描述，暂未识别技术',locationMissing:'未记录地点',technologyMissing:'未识别技术标签',multiple:'多地',recorded:'已记录地点',languages:'编程语言',frameworks:'框架与库',cloud:'云与基础设施',data:'数据库与数据平台',ai_tools:'AI 工具与推理框架',engineering:'工程工具与协议',methods:'技术方向与方法',other:'其他明确技术',locationNote:'远程、多地是地点说明，具体城市仍单独统计。远程包含明确写明可远程的岗位；安排以原文为准。',technologyNote:'按已保存资料匹配技术词表。具体工具与技术方向分开标记；仅记录语言要求或未识别标签，不代表没有技术要求。'},
 en:{roleMissing:'Job category not yet identified',technologyGroups:'Technology categories',technologyStatus:'Technology information',specific:'Specific technologies identified',direction_only:'Technical directions only',language_only:'Language requirements only',no_description:'No saved job description',unidentified:'Description saved; no recognized technology',locationMissing:'Location not recorded',technologyMissing:'No recognized technology tags',multiple:'Multiple locations',recorded:'Recorded location',languages:'Programming languages',frameworks:'Frameworks and libraries',cloud:'Cloud and infrastructure',data:'Databases and data platforms',ai_tools:'AI tools and inference frameworks',engineering:'Engineering tools and protocols',methods:'Technical directions and methods',other:'Other named technologies',locationNote:'Remote and multiple locations are location qualifiers; named cities are counted separately. Remote includes explicitly offered remote options; see the original arrangement.',technologyNote:'Tags are matched against stored job text. Named tools and technical directions are distinguished. Language-only records or unrecognized tags do not imply no technical requirements.'},
 de:{roleMissing:'Berufskategorie noch nicht zugeordnet',technologyGroups:'Technologiekategorien',technologyStatus:'Technologieangaben',specific:'Konkrete Technologien erkannt',direction_only:'Nur technische Themen erkannt',language_only:'Nur Sprachanforderungen erfasst',no_description:'Keine Stellenbeschreibung gespeichert',unidentified:'Beschreibung vorhanden; keine Technologie erkannt',locationMissing:'Standort nicht erfasst',technologyMissing:'Keine Technologie-Tags erkannt',multiple:'Mehrere Standorte',recorded:'Erfasster Standort',languages:'Programmiersprachen',frameworks:'Frameworks und Bibliotheken',cloud:'Cloud und Infrastruktur',data:'Datenbanken und Datenplattformen',ai_tools:'KI-Werkzeuge und Inferenz-Frameworks',engineering:'Entwicklungswerkzeuge und Protokolle',methods:'Technische Themen und Methoden',other:'Weitere benannte Technologien',locationNote:'Remote und mehrere Standorte sind Standortmerkmale; konkrete Städte werden separat gezählt. Remote umfasst ausdrücklich angebotene Optionen; maßgeblich ist der Originaltext.',technologyNote:'Tags werden aus gespeicherten Texten erkannt. Konkrete Werkzeuge und technische Themen werden getrennt markiert. Reine Sprachanforderungen oder fehlende Tags bedeuten nicht, dass keine technischen Anforderungen bestehen.'}
};
for(const lang of Object.keys(ANALYTICS_COPY))Object.assign(ANALYTICS_COPY[lang],ANALYTICS_DETAIL_COPY[lang]);
function isMissingFacet(value){return value===UNKNOWN_FACET||value.startsWith('__tech_');}
const TRACK_COPY={
 zh:{track:'岗位方向分布',today:'今日新增',latest:'最近一批',all:'全部已收录',range:'统计范围',todayTitle:'今日新增岗位方向分布（Track Breakdown）',latestTitle:'最近一批岗位方向分布（Track Breakdown）',allTitle:'已收录岗位方向分布（Track Breakdown）',unit:'席',note:'每个岗位只计入一个主要方向。点击条形查看对应岗位。',empty:'此范围暂无符合条件的新增岗位，可切换最近一批或全部已收录。',other:'其他 / 待核对',matrixNote:'仅交叉统计已识别的类别和技术，资料缺口请查看技术资料情况。'},
 en:{track:'Track breakdown',today:'Added today',latest:'Latest batch',all:'All collected',range:'Scope',todayTitle:'Today’s new jobs — Track breakdown',latestTitle:'Latest batch — Track breakdown',allTitle:'Collected jobs — Track breakdown',unit:'jobs',note:'Each job belongs to one primary track. Select a bar to view matching jobs.',empty:'No jobs in this scope. Select the latest batch or all collected jobs.',other:'Other / Needs review',matrixNote:'Only identified categories and technologies are crossed; see technology information for missing data.'},
 de:{track:'Verteilung nach Richtung',today:'Heute neu',latest:'Letzte Sammlung',all:'Alle erfassten',range:'Zeitraum',todayTitle:'Heute neue Stellen — Track Breakdown',latestTitle:'Letzte Sammlung — Track Breakdown',allTitle:'Erfasste Stellen — Track Breakdown',unit:'Stellen',note:'Jede Stelle zählt zu einer Hauptrichtung. Balken wählen, um Stellen anzuzeigen.',empty:'Keine Stellen in diesem Zeitraum. Letzte Sammlung oder alle Stellen wählen.',other:'Weitere / zu prüfen',matrixNote:'Nur erkannte Kategorien und Technologien werden gekreuzt; fehlende Angaben stehen bei Technologieangaben.'}
};
for(const lang of Object.keys(ANALYTICS_COPY))ANALYTICS_COPY[lang].track=TRACK_COPY[lang].track;
let analyticsTimeScope='all',analyticsOpened=false,analyticsBatchDate='';
function tc(){return TRACK_COPY[currentLang]||TRACK_COPY.en;}
function latestCollectedDate(){return JOBS.filter(j=>isRecentSearch(j,36500)).map(j=>j.addedOn).sort().at(-1)||'';}
function inAnalyticsTimeScope(job){return analyticsTimeScope==='today'?isRecentSearch(job,1):analyticsTimeScope==='latest'?!!(analyticsBatchDate||latestCollectedDate())&&job.addedOn===(analyticsBatchDate||latestCollectedDate()):true;}
function renderTrackBreakdown(jobs){
 const c=tc(),counts=countFacet(jobs,'track'),main=counts.filter(([name])=>name!==UNKNOWN_FACET&&name!=='Other / Needs review');
 const other=counts.filter(([name])=>name===UNKNOWN_FACET||name==='Other / Needs review').reduce((n,[,v])=>n+v,0);
 const max=Math.max(1,...main.map(([,n])=>n));
 const title=analyticsTimeScope==='today'?c.todayTitle:analyticsTimeScope==='latest'?c.latestTitle:c.allTitle;
 return `<section class="analytics-panel track-panel"><div class="lf-card-head"><h2>${title}</h2><span class="analytics-meta">${jobs.length} ${c.unit}${analyticsTimeScope==='latest'?' · '+latestCollectedDate():''}</span></div>${jobs.length?`<div class="track-rows">${main.map(([value,n])=>`<button class="track-row" data-action="facet" ${facetAttrs('track',value)} aria-pressed="${(analyticsFilters.track||[]).includes(value)}"><span class="track-name">${escapeHtml(value)}</span><span class="track-meter" aria-hidden="true"><span style="width:${n/max*100}%"></span></span><span class="track-count">${n} ${c.unit}</span></button>`).join('')}</div>${other?`<div class="track-other">${analyticsButton(c.other+' · '+other+' '+c.unit,'facet',facetAttrs('track','Other / Needs review'))}</div>`:''}<p class="analytics-meta">${c.note}</p>`:`<p class="analytics-note" role="status">${c.empty}</p>`}</section>`;
}
let analyticsSection = 'jobs';
let analyticsTab = 'distribution';
let analyticsDistribution = 'track';
let analyticsCross = 'locationRole';
const ANALYTICS_TABS = {zh:['岗位分布','交叉分析'],en:['Distributions','Cross analysis'],de:['Verteilungen','Kreuzanalyse']};
let analyticsFilters = {};
let analyticsExpanded = new Set();
let analyticsMatrixSelection = {};
let analyticsVisibleJobs = [];
const analyticsDisclosureState={};
const FACET_KEYS = ['track','cities','industry','role','technologies','technologyGroups','technologyStatus','workModel'];
function ac() { return ANALYTICS_COPY[currentLang] || ANALYTICS_COPY.en; }
function facetValues(job, key) {
  const a = job.analytics || {};
  const value = key === 'technologies' ? (a.technologies || []).map(t => t.name) : key==='cities' ? (a.locationTags||a.cities) : a[key];
  const values = [...new Set((Array.isArray(value) ? value : [value]).filter(v => typeof v === 'string' && v))];
  return values.length ? values : key==='track'?['Other / Needs review']:key==='technologies'&&a.technologyStatus ? ['__tech_'+a.technologyStatus+'__'] : [UNKNOWN_FACET];
}
function facetLabel(key,value){
 const c=ac();
 if(value===UNKNOWN_FACET)return key==='cities'?c.locationMissing:key==='technologies'?c.technologyMissing:key==='role'?c.roleMissing:c.unknown;
 if(value==='__location_remote__')return c.remote;
 if(value==='__location_multiple__')return c.multiple;
 if(value.startsWith('__location_recorded__:'))return c.recorded+' · '+value.slice('__location_recorded__:'.length);
 if(value.startsWith('__tech_'))return c[value.slice(7,-2)]||c.technologyMissing;
 if(key==='role'){const labels=ROLE_CATEGORY_LABELS[currentLang];return labels&&Object.hasOwn(labels,value)?labels[value]:value;}
 return ['workModel','technologyGroups','technologyStatus'].includes(key)?c[value]||value:value;
}

function matchesAnalytics(job) {
  if(!inAnalyticsTimeScope(job))return false;
  return Object.entries(analyticsFilters).every(([key, values]) => !values.length || facetValues(job,key).some(v => values.includes(v)));
}
function countFacet(jobs, key) {
  const counts = new Map();
  jobs.forEach(job => facetValues(job,key).forEach(value => counts.set(value,(counts.get(value)||0)+1)));
  return [...counts].sort((a,b) => b[1]-a[1] || a[0].localeCompare(b[0]));
}
function matrixCount(jobs, rowKey, row, colKey, col) {
  return jobs.filter(j=>facetValues(j,rowKey).includes(row) && facetValues(j,colKey).includes(col)).length;
}
function num(value) { return value === null ? '—' : new Intl.NumberFormat(currentLang,{maximumFractionDigits:1}).format(value); }
function analyticsButton(label, action, attrs='') {
  return `<button class="btn" data-action="${action}" ${attrs}>${escapeHtml(label)}</button>`;
}
function facetAttrs(key, value) { return `data-key="${key}" data-value="${escapeAttr(value)}"`; }
function switchAnalytics(section) {
  if(section==='analysis'&&!analyticsOpened){analyticsOpened=true;analyticsBatchDate=latestCollectedDate();analyticsTimeScope=JOBS.some(j=>isRecentSearch(j,1))?'today':latestCollectedDate()?'latest':'all';}
  analyticsSection = section;
  document.getElementById('analyticsView').hidden = section !== 'analysis';
  document.getElementById('jobsViewButton').setAttribute('aria-pressed',String(section==='jobs'));
  document.getElementById('analyticsViewButton').setAttribute('aria-pressed',String(section==='analysis'));
  document.getElementById('jobsViewButton').classList.toggle('btn-primary',section==='jobs');
  document.getElementById('analyticsViewButton').classList.toggle('btn-primary',section==='analysis');
  document.getElementById('jobViewControls').hidden = section === 'analysis';
  document.getElementById('tableView').style.display = section === 'jobs' && currentJobView === 'table' ? 'block' : 'none';
  document.getElementById('kanbanView').style.display = section === 'jobs' && currentJobView === 'kanban' ? 'grid' : 'none';
  filterJobs();
}
function renderAnalyticsFilters() {
  const c=ac(), host=document.getElementById('analyticsFilters');
  document.getElementById('jobsViewButton').textContent=c.jobs;
  document.getElementById('analyticsViewButton').textContent=c.analysis;
  document.getElementById('analyticsDemoNotice').textContent=DEMO_MODE?c.demo:'';
  document.getElementById('analyticsDemoNotice').hidden=!DEMO_MODE;
  const items=Object.entries(analyticsFilters).flatMap(([key,vs])=>vs.map(v=>analyticsButton(`${c.remove}: ${c[key]} · ${facetLabel(key,v)} ×`,'remove',facetAttrs(key,v))));
  if(analyticsTimeScope!=='all')items.unshift(analyticsButton(tc().range+': '+tc()[analyticsTimeScope]+' ×','time-reset'));
  host.hidden=!items.length;
  host.innerHTML=items.length ? `<span>${c.selected}</span>${items.join('')}${analyticsButton(c.reset,'reset')}` : '';
}
// Adapted from Lieflat Charts F5 Tick Rows (basics-gallery.html, C1) and
// L4 Arc Matrix (lupi-gallery.html, 3). PolyForm Noncommercial 1.0.0:
// https://polyformproject.org/licenses/noncommercial/1.0.0/
const LIEFLAT_COPY = {
  zh:{scroll:'横向滚动查看全部列',leading:'出现最多',tie:'并列最多',tags:'已标注标签',unit:'每条刻度 = 1 个岗位',area:'气泡面积 = 岗位数',replay:'重播',data:'查看完整数值',source:'已收录岗位 · 当前筛选',unknown:'未记录的资料',labels:'标签',count:'岗位数',share:'占比',page:'标签分页',peak:'最多的组合',noKnown:'暂无已标注标签',selection:'选择标签可筛选岗位',matrixLimit:'每次最多显示 8 行、8 列',showFirst:'返回前八项'},
  en:{scroll:'Scroll horizontally to compare all columns',leading:'appears most often',tie:'tied for most',tags:'recorded tags',unit:'One tick = one job',area:'Bubble area = jobs',replay:'Replay',data:'View exact values',source:'Collected jobs · current filters',unknown:'Missing information',labels:'Tag',count:'Jobs',share:'Share',page:'Tag page',peak:'Largest combination',noKnown:'No recorded tags',selection:'Select a tag to filter jobs',matrixLimit:'Show up to 8 rows and 8 columns',showFirst:'Return to top 8'},
  de:{scroll:'Horizontal scrollen, um alle Spalten zu vergleichen',leading:'am häufigsten',tie:'gleich häufig',tags:'erfasste Tags',unit:'Ein Strich = eine Stelle',area:'Blasenfläche = Stellen',replay:'Wiederholen',data:'Genaue Werte anzeigen',source:'Erfasste Stellen · aktuelle Filter',unknown:'Fehlende Angaben',labels:'Tag',count:'Stellen',share:'Anteil',page:'Tag-Seite',peak:'Größte Kombination',noKnown:'Keine erfassten Tags',selection:'Tag wählen, um Stellen zu filtern',matrixLimit:'Bis zu 8 Zeilen und 8 Spalten anzeigen',showFirst:'Zurück zu Top 8'}
};
let lieflatChartDisposers=[];
let analyticsDistributionPage=0;
function lc(){return LIEFLAT_COPY[currentLang]||LIEFLAT_COPY.en;}
function chartWidth(){return Math.max(180,Math.min(1120,document.getElementById('analyticsView').clientWidth-(innerWidth<760?32:48)));}
// Wrap full labels at their actual text width; never rotate or discard category names.
const analyticsLabelCanvas=document.createElement('canvas');
function chartLabelLines(value,width){
  const ctx=analyticsLabelCanvas.getContext('2d');ctx.font='600 12px Inter, system-ui';
  const lines=[];let rest=value;
  while(rest){
    let end=1;while(end<rest.length&&ctx.measureText(rest.slice(0,end+1)).width<=width)end++;
    if(end<rest.length){const space=rest.lastIndexOf(' ',end);if(space>0)end=space;}
    lines.push(rest.slice(0,end).trim());rest=rest.slice(end).trimStart();
  }
  return lines.length?lines:[''];
}
function distributionGeometry(jobs,key){
  const width=chartWidth(),x0=width<600?Math.min(140,width*.34):200;
  const {shown}=distributionData(jobs,key);
  const labels=shown.map(([v])=>chartLabelLines(facetLabel(key,v),x0-22));
  const rowHeight=Math.max(48,...labels.map(lines=>lines.length*15+18));
  return {width,x0,labels,rowHeight,height:shown.length*rowHeight+12};
}
function matrixGeometry(rows,cols,rowKey,colKey){
  const left=180,columnWidth=Math.max(128,Math.min(160,(chartWidth()-left-16)/Math.max(1,cols.length)));
  const rowLabels=rows.map(v=>chartLabelLines(facetLabel(rowKey,v),left-36));
  const colLabels=cols.map(v=>chartLabelLines(facetLabel(colKey,v),columnWidth-12));
  const rowHeight=Math.max(56,...rowLabels.map(lines=>lines.length*15+20));
  const top=Math.max(76,...colLabels.map(lines=>lines.length*15+38));
  return {width:left+cols.length*columnWidth+16,height:top+Math.max(0,rows.length-1)*rowHeight+28,left,columnWidth,rowHeight,top,rowLabels,colLabels};
}
function chartWrappedLabel(parent,attrs,lines){
  const label=MONO.el(parent,'text',attrs);
  lines.forEach((line,i)=>{const span=MONO.el(label,'tspan',{x:attrs.x,dy:i?15:0});span.textContent=line;});
  return label;
}
function shortChartLabel(value,limit){return value.length>limit?value.slice(0,limit-1)+'…':value;}
function chartSource(template){return `<div class="lf-src">${escapeHtml(lc().source)}</div>`;}
function distributionData(jobs,key){
  const counts=countFacet(jobs,key),known=counts.filter(([v])=>!isMissingFacet(v));
  const missingEntries=counts.filter(([v])=>isMissingFacet(v));
  const missing=missingEntries.reduce((n,[,v])=>n+v,0);
  const expanded=analyticsExpanded.has(key),pages=Math.ceil(known.length/8);
  const page=expanded?Math.min(analyticsDistributionPage,Math.max(0,pages-1)):0;
  return {known,missing,missingEntries,pages,page,shown:known.slice(page*8,page*8+8)};
}
function renderDistribution(jobs,key){
  const c=ac(),l=lc(),{known,missing,missingEntries,pages,page,shown}=distributionData(jobs,key);
  const leader=known[0], tied=leader&&known.filter(([,n])=>n===leader[1]).length>1;
  const title=leader?`${facetLabel(key,leader[0])} · ${num(leader[1])}`:l.noKnown;
  const table=known.map(([v,n])=>`<tr><th scope="row">${escapeHtml(facetLabel(key,v))}</th><td class="analytics-numeric">${n}</td><td class="analytics-numeric">${num(jobs.length?n/jobs.length*100:0)}%</td>${key==='technologies'?`<td>${escapeHtml(c[(jobs.flatMap(j=>j.analytics?.technologies||[]).find(t=>t.name===v)||{}).category]||c.other)}</td>`+['required','preferred','mentioned'].map(level=>`<td class="analytics-numeric">${jobs.filter(j=>(j.analytics?.technologies||[]).some(t=>t.name===v&&t.requirement===level)).length}</td>`).join(''):''}</tr>`).join('');
  return `<section class="analytics-panel lf-card" data-template="F5"><div class="lf-card-head"><div><h2>${escapeHtml(title)}</h2><div class="lf-sub">${l.unit} · ${c.coverage}: ${jobs.length-missing}/${jobs.length}</div></div>${shown.length?analyticsButton(l.replay,'replay','data-chart="lf-distribution"'):''}</div>${shown.length?`<svg class="lf-svg" id="lf-distribution" viewBox="0 0 ${distributionGeometry(jobs,key).width} ${distributionGeometry(jobs,key).height}" role="group" aria-label="${escapeAttr(c[key]+'. '+l.unit)}"></svg><p class="analytics-meta">${l.selection}</p>`:`<p>${l.noKnown}</p>`}${known.length>8?analyticsButton(analyticsExpanded.has(key)?l.showFirst:c.showAll,'expand',`data-key="${key}"`):''}${analyticsExpanded.has(key)&&pages>1?`<label class="analytics-toolbar">${l.page}<select data-dist-page>${Array.from({length:pages},(_,i)=>`<option value="${i}" ${i===page?'selected':''}>${i*8+1}–${Math.min(known.length,(i+1)*8)} / ${known.length}</option>`).join('')}</select></label>`:''}<div class="lf-missing"><span>${l.unknown}</span>${missingEntries.length?missingEntries.map(([value,n])=>analyticsButton(`${facetLabel(key,value)} · ${n} / ${jobs.length}`,'facet',`${facetAttrs(key,value)} aria-pressed="${(analyticsFilters[key]||[]).includes(value)}"`)).join(''):`<span>0 / ${jobs.length}</span>`}<span>${c.multi}</span></div><details class="lf-values" data-disclosure="distribution-values"><summary>${l.data}</summary><div class="analytics-scroll" tabindex="0" role="region" aria-label="${c[key]}"><table><thead><tr><th>${l.labels}</th><th class="analytics-numeric">${l.count}</th><th class="analytics-numeric">${l.share}</th>${key==='technologies'?`<th>${c.technologyGroups}</th>`+['required','preferred','mentioned'].map(level=>`<th class="analytics-numeric">${c[level]}</th>`).join(''):''}</tr></thead><tbody>${table}${missingEntries.map(([value,n])=>`<tr><th scope="row">${escapeHtml(facetLabel(key,value))}</th><td class="analytics-numeric">${n}</td><td class="analytics-numeric">${num(jobs.length?n/jobs.length*100:0)}%</td>${key==='technologies'?'<td colspan="4">—</td>':''}</tr>`).join('')}</tbody></table></div></details>${key==='technologies'?`<p class="analytics-meta">${c.techNote} ${c.technologyNote}</p>`:''}${key==='cities'?`<p class="analytics-meta">${c.locationNote}</p>`:''}${key==='technologies'?`<div class="lf-missing"><span>${c.technologyStatus}</span>${countFacet(jobs,'technologyStatus').map(([value,n])=>analyticsButton(`${facetLabel('technologyStatus',value)} · ${n}`,'facet',`${facetAttrs('technologyStatus',value)} aria-pressed="${(analyticsFilters.technologyStatus||[]).includes(value)}"`)).join('')}</div>`:''}${chartSource('F5 · TICK ROWS')}</section>`;
}
function matrixData(jobs,id,rowKey,colKey){
  const allRows=countFacet(JOBS,rowKey).map(x=>x[0]).filter(v=>id!=='roleTech'||v!==UNKNOWN_FACET),allCols=countFacet(JOBS,colKey).map(x=>x[0]).filter(v=>id!=='roleTech'||!isMissingFacet(v));
  const selection=analyticsMatrixSelection[id]||{rows:allRows.slice(0,6),columns:allCols.slice(0,6)};
  const rows=selection.rows.slice(0,8),cols=selection.columns.slice(0,8);
  const cells=rows.flatMap((row,i)=>cols.map((col,j)=>({row,col,i,j,n:matrixCount(jobs,rowKey,row,colKey,col)})));
  return {allRows,allCols,rows,cols,cells,max:Math.max(0,...cells.map(c=>c.n))};
}
function renderMatrix(jobs,id,rowKey,colKey){
  const c=ac(),l=lc(),{allRows,allCols,rows,cols,cells,max}=matrixData(jobs,id,rowKey,colKey);
  const peak=cells.find(cell=>cell.n===max),title=max?`${facetLabel(rowKey,peak.row)} × ${facetLabel(colKey,peak.col)} · ${max}`:c.empty;
  const options=(all,selected,key)=>all.map(v=>`<option value="${escapeAttr(v)}" ${selected.includes(v)?'selected':''}>${escapeHtml(facetLabel(key,v))}</option>`).join('');
  return `<section class="analytics-panel lf-card" data-template="L4"><div class="lf-card-head"><div><h2>${escapeHtml(title)}</h2><div class="lf-sub">${c[id]} · ${l.area} · ${l.peak}${id==='roleTech'?'<br>'+tc().matrixNote:''}</div></div>${rows.length&&cols.length?analyticsButton(l.replay,'replay','data-chart="lf-matrix"'):''}</div><div class="lf-matrix-controls"><details data-disclosure="matrix-options"><summary>${c.choose}</summary><p class="analytics-meta">${c.multiSelect} ${l.matrixLimit}</p><div class="analytics-toolbar"><label>${c.rows}<select multiple size="4" data-matrix="${id}" data-side="rows" aria-label="${c[id]}: ${c.rows}">${options(allRows,rows,rowKey)}</select></label><label>${c.columns}<select multiple size="4" data-matrix="${id}" data-side="columns" aria-label="${c[id]}: ${c.columns}">${options(allCols,cols,colKey)}</select></label></div></details><p class="analytics-meta">${c.matrixHint}</p></div><p class="analytics-meta lf-scroll-note" data-matrix-scroll hidden>${l.scroll}</p><div class="analytics-scroll" tabindex="0" role="region" aria-label="${c[id]}"><svg class="lf-svg lf-matrix-svg" id="lf-matrix" viewBox="0 0 ${matrixGeometry(rows,cols,rowKey,colKey).width} ${matrixGeometry(rows,cols,rowKey,colKey).height}" role="group" aria-label="${escapeAttr(c[id]+'. '+l.area)}"></svg></div><details class="lf-values" data-disclosure="matrix-values"><summary>${l.data}</summary><div class="analytics-scroll" tabindex="0" role="region" aria-label="${c[id]}"><table><thead><tr><th>${c[rowKey]}</th>${cols.map(col=>`<th scope="col">${escapeHtml(facetLabel(colKey,col))}</th>`).join('')}</tr></thead><tbody>${rows.map(r=>`<tr><th scope="row">${escapeHtml(facetLabel(rowKey,r))}</th>${cols.map(col=>`<td class="analytics-numeric">${matrixCount(jobs,rowKey,r,colKey,col)}</td>`).join('')}</tr>`).join('')}</tbody></table></div></details>${chartSource('L4 · ARC MATRIX')}</section>`;
}
function restoreChartFocus(focus){
  if(!focus||!['facet','matrix'].includes(focus.action))return;
  const target=[...document.querySelectorAll('#analyticsView [data-action]')].find(el=>Object.entries(focus).every(([k,v])=>el.dataset[k]===v));
  target?.focus({preventScroll:true});
}
function mountLieflatCharts(jobs,focus){
  lieflatChartDisposers.forEach(dispose=>dispose());lieflatChartDisposers=[];
  if(document.getElementById('lf-distribution'))lieflatChartDisposers.push(MONO.obsReveal('lf-distribution',s=>{
    // F5/C1: a horizontal countable queue, fifth-unit dots and endpoint value.
    const {shown}=distributionData(jobs,analyticsDistribution),{width,height,x0:X0,labels,rowHeight}=distributionGeometry(jobs,analyticsDistribution);
    s.setAttribute('viewBox',`0 0 ${width} ${height}`);s.style.width=width+'px';
    const max=Math.max(1,...shown.map(([,n])=>n)),PX=Math.min(8,Math.max(1,width-X0-80)/max);
    shown.forEach(([value,v],i)=>{
      const name=facetLabel(analyticsDistribution,value),y=rowHeight/2+i*rowHeight;
      const row=MONO.el(s,'g',{class:'analytics-bar',role:'button',tabindex:0,'data-action':'facet','data-key':analyticsDistribution,'data-value':value,'data-count':v,'data-unit':1,'aria-label':`${name}: ${v} / ${jobs.length}, ${num(jobs.length?v/jobs.length*100:0)}%`,'aria-pressed':String((analyticsFilters[analyticsDistribution]||[]).includes(value))});
      MONO.el(row,'rect',{class:'lf-hit',x:0,y:y-20,width,height:rowHeight-4,rx:6});
      const label=chartWrappedLabel(row,{x:X0-14,y:y+4-(labels[i].length-1)*7.5,'font-size':12,'font-weight':600,fill:MONO.L[2],'text-anchor':'end',class:'lf-label'},labels[i]);MONO.tip(label,name);
      MONO.el(row,'line',{x1:X0,y1:y+9,x2:X0+max*PX,y2:y+9,stroke:MONO.GRID,'stroke-width':.6,class:'fade',style:`animation-delay:${i*.1}s`});
      for(let k=0;k<v;k++){
        const x=X0+k*PX+PX/2,h=9+MONO.rnd(k+1,i+2)*6;
        MONO.el(row,'line',{class:'lf-tick fade',x1:x,y1:y+9,x2:x,y2:y+9-h,stroke:MONO.INK,'stroke-width':Math.min(.9,PX*.65),style:`animation-delay:${i*.1+k*.012}s`});
        if(k%5===4)MONO.el(row,'circle',{cx:x,cy:y+13,r:.8,fill:MONO.L[5],class:'fade',style:`animation-delay:${i*.1+k*.012}s`});
      }
      const labelValue=MONO.txt(row,{x:X0+v*PX+9,y:y+4,'font-size':13,'font-weight':800,fill:MONO.INK,class:'fade',style:`animation-delay:${.4+i*.1}s`},v);MONO.tip(labelValue,`${name}: ${v} / ${jobs.length}`);
      MONO.txt(row,{x:width-2,y:y+4,'font-size':12,'font-weight':500,fill:MONO.L[2],'text-anchor':'end'},num(jobs.length?v/jobs.length*100:0)+'%');
    });restoreChartFocus(focus);
  }));
  if(document.getElementById('lf-matrix'))lieflatChartDisposers.push(MONO.obsReveal('lf-matrix',s=>{
    // L4/3: bowed row horizons; circle area is proportional to cell count.
    const id=analyticsCross,rowKey=id==='locationRole'?'cities':'role',colKey=id==='locationRole'?'role':'technologies';
    const {rows,cols,cells,max}=matrixData(jobs,id,rowKey,colKey);
    const {width,height,left,columnWidth,rowHeight,top:headerHeight,rowLabels,colLabels}=matrixGeometry(rows,cols,rowKey,colKey);
    s.setAttribute('viewBox',`0 0 ${width} ${height}`);s.style.width=width+'px';
    const scrollNote=s.closest('section').querySelector('[data-matrix-scroll]');if(scrollNote)scrollNote.hidden=s.parentElement.clientWidth>=width;
    const rowY=i=>headerHeight+i*rowHeight,colX=j=>left+columnWidth/2+j*columnWidth,dy=j=>cols.length<2?0:-10*Math.sin(Math.PI*j/(cols.length-1));
    const radiusScale=max?15/Math.sqrt(max):0,top=[...cells].filter(c=>c.n>0).sort((a,b)=>b.n-a.n).slice(0,4);
    rows.forEach((row,i)=>{
      const d='M'+cols.map((_,j)=>`${colX(j)} ${rowY(i)+dy(j)}`).join(' L ');
      if(cols.length)MONO.el(s,'path',{d,fill:'none',stroke:MONO.GRID,'stroke-width':1,pathLength:1,class:'draw',style:`animation-delay:${i*.08}s`});
      const label=chartWrappedLabel(s,{x:left-24,y:rowY(i)+4-(rowLabels[i].length-1)*7.5,'font-size':12,'font-weight':600,fill:MONO.L[2],'text-anchor':'end'},rowLabels[i]);MONO.tip(label,facetLabel(rowKey,row));
      cols.forEach((col,j)=>{
        const x=colX(j),y=rowY(i)+dy(j),vv=cells.find(c=>c.i===i&&c.j===j).n;
        if(!vv){MONO.el(s,'circle',{cx:x,cy:y,r:.9,fill:MONO.L[5],class:'pop'});return;}
        const name=`${facetLabel(rowKey,row)} / ${facetLabel(colKey,col)}: ${vv}`;
        const group=MONO.el(s,'g',{class:'analytics-cell',role:'button',tabindex:0,'data-action':'matrix','data-key':rowKey,'data-value':row,'data-col-key':colKey,'data-col-value':col,'data-count':vv,'aria-label':name});
        MONO.el(group,'rect',{class:'lf-hit',x:x-24,y:y-24,width:48,height:48,rx:8});
        const r=Math.sqrt(vv)*radiusScale;
        const dot=MONO.el(group,'circle',{class:'lf-bubble pop',cx:x,cy:y,r,fill:vv>=max*.66?MONO.INK:vv>=max*.33?MONO.L[2]:MONO.L[4],style:`animation-delay:${.2+i*.08+j*.02}s`});MONO.tip(dot,name);
        if(top.some(c=>c.i===i&&c.j===j))MONO.txt(group,{x,y:y-r-5,'font-size':12,'font-weight':800,fill:MONO.INK,'text-anchor':'middle',class:'fade',style:'animation-delay:.6s'},vv);
      });
    });
    cols.forEach((col,j)=>{
      const x=colX(j),label=chartWrappedLabel(s,{x,y:16,'font-size':12,'font-weight':600,fill:MONO.L[2],'text-anchor':'middle',class:'lf-column-label'},colLabels[j]);MONO.tip(label,facetLabel(colKey,col));
    });restoreChartFocus(focus);
  }));
}

function renderAnalytics(jobs=analyticsVisibleJobs) {
  const focused=document.activeElement;
  const focusData=focused?.dataset ? {...focused.dataset} : {};
  analyticsVisibleJobs=jobs;
  renderAnalyticsFilters();
  if(analyticsSection!=='analysis') return;
  const c=ac(), host=document.getElementById('analyticsView');
  const tabLabels=ANALYTICS_TABS[currentLang]||ANALYTICS_TABS.en;
  // Keep focus stable when a selected bar or chip redraws the charts.
  const focusKey=Object.keys(focusData).length ? focusData : null;
  host.querySelectorAll('details[data-disclosure]').forEach(el=>analyticsDisclosureState[el.dataset.disclosure]=el.open);
  host.innerHTML=`<div class="analytics-header"><div><h1>${c.title}</h1><p>${c.scope}</p></div><div class="analytics-total"><span class="analytics-count">${jobs.length}</span><span>${c.total}</span></div><div class="analytics-header-actions">${analyticsButton(c.showJobs,'jobs')}${analyticsButton(c.reset,'reset')}</div></div><div class="analytics-controls"><label class="analytics-time-select">${tc().range}<select data-time-scope>${['today','latest','all'].map(value=>`<option value="${value}" ${analyticsTimeScope===value?'selected':''}>${tc()[value]}</option>`).join('')}</select></label><div class="analytics-switch" role="group" aria-label="${c.analysis}">${['distribution','cross'].map((tab,i)=>analyticsButton(tabLabels[i],'tab',`data-key="${tab}" aria-pressed="${analyticsTab===tab}"`)).join('')}</div><label class="analytics-view-select"><span>${analyticsTab==='distribution'?tabLabels[0]:tabLabels[1]}</span>${analyticsTab==='distribution'?`<select data-distribution>${FACET_KEYS.map(k=>`<option value="${k}" ${analyticsDistribution===k?'selected':''}>${c[k]}</option>`).join('')}</select>`:`<select data-cross><option value="locationRole" ${analyticsCross==='locationRole'?'selected':''}>${c.locationRole}</option><option value="roleTech" ${analyticsCross==='roleTech'?'selected':''}>${c.roleTech}</option></select>`}</label><details class="analytics-add-filters" data-disclosure="filters"><summary>${c.add}</summary><div class="analytics-toolbar">${FACET_KEYS.map(key=>`<label>${c[key]}<select data-facet-select="${key}"><option value="">${c.add}</option>${countFacet(JOBS,key).map(([v])=>`<option value="${escapeAttr(v)}">${escapeHtml(facetLabel(key,v))}</option>`).join('')}</select></label>`).join('')}</div></details></div>${!jobs.length?`<p class="analytics-note" role="status">${c.empty}</p>`:''}${analyticsTab==='distribution'?(analyticsDistribution==='track'?renderTrackBreakdown(jobs):renderDistribution(jobs,analyticsDistribution)):renderMatrix(jobs,analyticsCross,analyticsCross==='locationRole'?'cities':'role',analyticsCross==='locationRole'?'role':'technologies')}<section class="analytics-records"><details data-disclosure="records"><summary>${c.records} · ${jobs.length}</summary>${jobs.slice(0,analyticsExpanded.has('records')?jobs.length:10).map(j=>`<div class="analytics-record">${analyticsButton(`${j.company||'—'} · ${j.title||'—'}`,'detail',`data-id="${escapeAttr(j.id)}"`)}<span>${escapeHtml(j.location||c.unknown)}</span></div>`).join('')}${jobs.length>10?analyticsButton(analyticsExpanded.has('records')?c.showLess:c.showAll,'expand','data-key="records"'):''}</details></section>`;
  mountLieflatCharts(jobs,focusKey);
  host.querySelectorAll('details[data-disclosure]').forEach(el=>el.open=!!analyticsDisclosureState[el.dataset.disclosure]);
  if(focusKey){const el=[...document.querySelectorAll('#analyticsView button,#analyticsView select,#analyticsFilters button')].find(el=>Object.entries(focusKey).every(([k,v])=>el.dataset[k]===v));(el||document.getElementById('analyticsViewButton')).focus({preventScroll:true});}
}
function addAnalyticsFacet(key,value) {
  if(!FACET_KEYS.includes(key)) return;
  analyticsFilters[key]=[...new Set([...(analyticsFilters[key]||[]),value])];
}
function handleAnalyticsClick(event) {
  const button=event.target.closest('[data-action]');if(!button)return;
  const {action,key,value}=button.dataset;
  if(action==='time-reset'){analyticsTimeScope='all';filterJobs();return;}
  if(action==='replay'){document.getElementById(button.dataset.chart)?.dispatchEvent(new Event('click'));return;}
  if(action==='tab'){analyticsTab=key;renderAnalytics();return;}
  if(action==='jobs'){switchAnalytics('jobs');return;}
  if(action==='reset'){resetAllFilters();return;}
  if(action==='detail'){openJobDetailById(button.dataset.id);return;}
  if(action==='expand'){analyticsExpanded.has(key)?analyticsExpanded.delete(key):analyticsExpanded.add(key);}
  if(action==='remove') analyticsFilters[key]=(analyticsFilters[key]||[]).filter(v=>v!==value);
  if(action==='facet') {
    if((analyticsFilters[key]||[]).includes(value)) analyticsFilters[key]=analyticsFilters[key].filter(v=>v!==value);
    else addAnalyticsFacet(key,value);
  }
  if(action==='matrix'){analyticsFilters[key]=[value];analyticsFilters[button.dataset.colKey]=[button.dataset.colValue];}
  filterJobs();
}
function initAnalytics() {
  document.getElementById('analyticsView').addEventListener('click',handleAnalyticsClick);
  document.getElementById('analyticsView').addEventListener('keydown',event=>{if(['Enter',' '].includes(event.key)&&event.target.matches('svg [role="button"]')){event.preventDefault();handleAnalyticsClick(event);}});
  document.getElementById('analyticsFilters').addEventListener('click',handleAnalyticsClick);
  let lastChartWidth=0, resizeFrame=0;
  const chartResize=new ResizeObserver(entries=>{
    const width=Math.round(entries[0].contentRect.width);
    if(!width||width===lastChartWidth)return;
    lastChartWidth=width;cancelAnimationFrame(resizeFrame);
    resizeFrame=requestAnimationFrame(()=>{if(analyticsSection==='analysis')mountLieflatCharts(analyticsVisibleJobs);});
  });
  chartResize.observe(document.getElementById('analyticsView'));
  document.getElementById('analyticsView').addEventListener('change',e=>{
    if(e.target.matches('[data-time-scope]')){analyticsTimeScope=e.target.value;analyticsBatchDate=latestCollectedDate();filterJobs();return;}
    if(e.target.matches('[data-dist-page]')){analyticsDistributionPage=Number(e.target.value);renderAnalytics();return;}
    if(e.target.matches('[data-distribution]')){analyticsDistributionPage=0;analyticsDistribution=e.target.value;renderAnalytics();return;}
    if(e.target.matches('[data-cross]')){analyticsCross=e.target.value;renderAnalytics();return;}
    const key=e.target.dataset.facetSelect;
    if(key&&e.target.value){addAnalyticsFacet(key,e.target.value);filterJobs();}
    const id=e.target.dataset.matrix;
    if(id){
      const host=e.target.closest('details');
      analyticsMatrixSelection[id]={};
      host.querySelectorAll('select').forEach(s=>{const selected=[...s.selectedOptions].slice(0,8);[...s.options].forEach(o=>o.selected=selected.includes(o));analyticsMatrixSelection[id][s.dataset.side]=selected.map(o=>o.value);});
      // Preserve the open selector and keyboard focus; redraw only the matrix table.
      const panel=host.closest('section'), wrapper=document.createElement('div');
      wrapper.innerHTML=renderMatrix(analyticsVisibleJobs,id,id==='locationRole'?'cities':'role',id==='locationRole'?'role':'technologies');
      panel.querySelector('.lf-card-head').replaceWith(wrapper.querySelector('.lf-card-head'));
      panel.querySelectorAll('.analytics-scroll').forEach((scroll,i)=>scroll.replaceWith(wrapper.querySelectorAll('.analytics-scroll')[i]));
      mountLieflatCharts(analyticsVisibleJobs);
    }
  });
}

function analyticsJobEvidence(job) {
  const c=ac(), a=job.analytics||{};
  return `<details><summary>${c.raw}</summary><p>${c.analyzed}: ${escapeHtml(a.analyzedAt||c.undated)}</p>${['cities','industry','role'].map(k=>`<p><strong>${c[k]}</strong>: ${escapeHtml(facetValues(job,k).map(v=>facetLabel(k,v)).join(', '))}<br>${escapeHtml(a.evidence?.[k]||c.unknown)}</p>`).join('')}<h3>${c.technologies}</h3><p>${c.technologyStatus}: ${escapeHtml(c[a.technologyStatus]||c.technologyMissing)}</p>${(a.technologies||[]).map(t=>`<p><strong>${escapeHtml(t.name)}</strong> · ${c[t.category]||c.other} · ${c[t.requirement]||c.mentioned}<br>${escapeHtml(t.evidence)}</p>`).join('')||`<p>${c.unknown}</p>`}</details>`;
}
