/* W01: one real local browser proof. Passive observation; no product/clock patch. */
"use strict";
const fs=require("fs"), path=require("path"), http=require("http"), crypto=require("crypto");
const {performance}=require("perf_hooks"), {spawnSync}=require("child_process");
const ORIGIN="http://127.0.0.1:8765", CORE=["run-context.json","timer-trace.ndjson","browser-events.ndjson","console-events.ndjson","storage-snapshots.ndjson"];
const mono=()=>Number(process.hrtime.bigint())/1e9, utc=()=>new Date().toISOString();
const digest=b=>crypto.createHash("sha256").update(b).digest("hex");
function need(ok,reason){if(!ok)throw new Error(reason);}
function readJSON(p){return JSON.parse(fs.readFileSync(p,"utf8"));}
function score(q,a){const c=new Set(q.correct),s=new Set(a||[]);if(!s.size||[...s].some(i=>!c.has(i)))return 0;if(s.size===c.size)return Number(q.points);return Number(q.points)===2&&c.size>=2?1:0;}
function chooseCases(session){
 const used=new Set(), pick=f=>{const i=session.questions.findIndex((q,i)=>!used.has(i)&&f(q));need(i>=0,"Required real grading case not present");used.add(i);return i;};
 const one=pick(q=>Number(q.points)===1),full=pick(q=>Number(q.points)===2&&q.correct.length>=2),partial=pick(q=>Number(q.points)===2&&q.correct.length>=2),wrong=pick(q=>q.answers.some((_,j)=>!q.correct.includes(j)));
 return [{kind:"full-one",index:one,selected:[...session.questions[one].correct],expected:1},
 {kind:"full-two",index:full,selected:[...session.questions[full].correct],expected:2},
 {kind:"partial-two",index:partial,selected:[session.questions[partial].correct[0]],expected:1},
 {kind:"wrong",index:wrong,selected:[session.questions[wrong].answers.findIndex((_,j)=>!session.questions[wrong].correct.includes(j))],expected:0}];
}
function observerInit(arg){
 const doc=String(performance.timeOrigin);let lastTimer=null,terminal=false;
 const emit=p=>{const fn=window[arg.binding];if(typeof fn!=="function")return;fn({documentId:doc,pagePerformanceMs:performance.now(),...p}).catch(e=>console.error("W01 passive observation transport failed",String(e)));};
 const timer=(value,source)=>{value=String(value||"").trim();if(/^\d{2,3}:\d{2}$/.test(value)&&value!==lastTimer){lastTimer=value;emit({kind:"timer-observed",display:value,source});}};
 const inspectNode=n=>{if(n.nodeType===1){if(n.id==="examTimer")timer(n.textContent,"added-timer");n.querySelectorAll?.("#examTimer").forEach(t=>timer(t.textContent,"added-subtree"));}};
 const inspect=records=>{
  for(const r of records){
   if(r.type==="childList"){if(r.target.nodeType===1&&r.target.id==="examTimer")for(const n of r.addedNodes)timer(n.textContent,"timer-child-mutation");for(const n of r.addedNodes)inspectNode(n);}
   if(r.type==="characterData"&&r.target.parentElement?.id==="examTimer")timer(r.target.textContent,"timer-character-mutation");
  }
  const current=document.getElementById("examTimer");if(current)timer(current.textContent,"live-timer");
  if(!terminal&&document.querySelector(".result-wrapper .result-hero")){terminal=true;emit({kind:"terminal-render",automaticObservation:true,title:document.querySelector(".result-hero h1")?.textContent||""});}
 };
 new MutationObserver(inspect).observe(document,{childList:true,subtree:true,characterData:true});
 document.addEventListener("click",event=>{
  const card=event.target?.closest?.('[onclick*="startExamMode"]');
  if(card&&card.getAttribute("onclick")?.includes("'full'"))emit({kind:"exam-start-ui",target:"full-simulation-card"});
 },true);
 emit({kind:"observer-installed",passive:true,clocksPatched:false});
}
async function main(){
 const configPath=path.resolve(process.argv[2]||"");const cfg=readJSON(configPath);
 const root=path.resolve(cfg.root),out=path.resolve(cfg.evidenceDirectory);
 need(root.toLowerCase()==="c:\\xampp\\htdocs\\accaoui\\v4-dashboard"&&cfg.origin===ORIGIN&&cfg.maximumSeconds===7800&&cfg.minimumNaturalSeconds===7200,"Exact approved root/origin/budgets");
 need(out.toLowerCase().startsWith(path.resolve(cfg.packageEvidenceDirectory).toLowerCase()+path.sep),"Private fresh run child directory");
 need(cfg.task==="ACCAOUI_DEVELOPMENT_SEQUENCE_W01"&&cfg.base&&cfg.runId,"Bound W01 configuration");
 fs.mkdirSync(out,{recursive:true});
 const claim=path.join(cfg.packageEvidenceDirectory,"natural-run-started.json");
 const claimRecord={runId:cfg.runId,task:cfg.task,utc:utc(),monotonic:mono(),runnerStarts:1,examStarts:0,configPath};
 fs.writeFileSync(claim,JSON.stringify(claimRecord,null,2)+"\n",{encoding:"utf8",flag:"wx"});
 const started=mono(), runUTC=utc();let sequence=0, sealed=false, fatal=null,browser=null,context=null,page=null,server=null,checkpointTimer=null,deadlineTimer=null,examStarts=0,terminalSeen=0,zeroSeen=0,terminalSnapshot=null,cases=[],lastCheckpoint=started;
 const fds={};for(const name of CORE.slice(1))fds[name]=fs.openSync(path.join(out,name),"wx");
 const contextRecord={schema:1,runId:cfg.runId,task:cfg.task,base:cfg.base,manifestSHA256:cfg.manifestSHA256,origin:cfg.origin,utc:runUTC,monotonic:started,captureBeforeNavigation:true,captureBeforeExamStart:true,minimumNaturalSeconds:7200,maximumSeconds:7800,flushMaximumSeconds:60,clock:"unmodified host hrtime and renderer performance.now",clockManipulated:false,reconstructed:false,syntheticOnly:true,isolatedContext:true,liveSupabase:false,framework:"existing Playwright 1.62.1",browserExecutable:cfg.browserExecutable};
 fs.writeFileSync(path.join(out,CORE[0]),JSON.stringify(contextRecord,null,2)+"\n",{encoding:"utf8",flag:"wx"});
 const record=(file,payload)=>{if(sealed)return;const row={runId:cfg.runId,sequence:++sequence,utc:utc(),monotonic:mono(),...payload};fs.writeSync(fds[file],JSON.stringify(row)+"\n",null,"utf8");return row;};
 const be=p=>record("browser-events.ndjson",p),te=p=>record("timer-trace.ndjson",p),ce=p=>record("console-events.ndjson",p);
 for(const name of CORE.slice(1))record(name,{kind:"capture-opened",beforeBrowserCreation:true});
 function checkpoint(reason){
  if(sealed)return;for(const fd of Object.values(fds))fs.fsyncSync(fd);
  const files=CORE.map(name=>{const raw=fs.readFileSync(path.join(out,name));return {path:name,bytes:raw.length,sha256:digest(raw)};});
  const now=mono();be({kind:"capture-checkpoint",reason,completePrefixRead:true,gapSeconds:now-lastCheckpoint,files});lastCheckpoint=now;
  fs.fsyncSync(fds["browser-events.ndjson"]);
  fs.writeFileSync(path.join(out,"progress.json"),JSON.stringify({runId:cfg.runId,state:"RUNNING",utc:utc(),monotonic:mono(),elapsedSeconds:mono()-started,examStarts,terminalSeen,zeroSeen,files},null,2)+"\n");
 }
 async function snapshot(phase){
  const raw=await page.evaluate(()=>({pagePerformanceMs:performance.now(),documentId:String(performance.timeOrigin),storage:Object.fromEntries(Object.keys(localStorage).map(k=>[k,localStorage.getItem(k)])),timer:document.getElementById("examTimer")?.textContent||null,resultCount:document.querySelectorAll(".result-wrapper .result-hero").length,resumeOffered:document.getElementById("examResumeCard")!==null,stats:[...document.querySelectorAll(".result-stats-grid .result-stat-card")].map(n=>[n.querySelector("span")?.textContent?.trim(),n.querySelector("strong")?.textContent?.trim()])}));
  need(Object.keys(raw.storage).every(k=>k.startsWith("accaoui_")&&!/token|password|credential|secret|^sb-/i.test(k)),"Only synthetic app storage, no credential keys");
  record("storage-snapshots.ndjson",{kind:"storage-snapshot",phase,...raw});return raw;
 }
 function seal(status,error){
  if(sealed)return null;be({kind:"capture-sealing",status,error:error||null,examStarts,terminalSeen,zeroSeen});
  checkpoint("final-before-cleanup");sealed=true;for(const fd of Object.values(fds))fs.fsyncSync(fd);
  const streams=CORE.map(name=>{const raw=fs.readFileSync(path.join(out,name));const rows=name.endsWith(".ndjson")?raw.toString("utf8").trimEnd().split("\n").map(JSON.parse):[JSON.parse(raw.toString("utf8"))];need(rows.length>0&&rows.every(r=>r.runId===cfg.runId),"Complete core read/run identity "+name);return {path:name,bytes:raw.length,sha256:digest(raw),complete:status==="COMPLETE",utcStart:rows[0].utc,utcEnd:rows[rows.length-1].utc,monotonicStart:rows[0].monotonic,monotonicEnd:rows[rows.length-1].monotonic};});
  const manifest={schema:1,runId:cfg.runId,status,complete:status==="COMPLETE",naturalClock:true,reconstructed:false,error:error||null,streams,utc:utc(),monotonic:mono()};
  fs.writeFileSync(path.join(out,"evidence-manifest.json"),JSON.stringify(manifest,null,2)+"\n");return manifest;
 }
 try{
  const deadline=new Promise((_resolve,reject)=>{deadlineTimer=setTimeout(()=>{fatal=new Error("TIMEOUT: unchanged 7800s complete browser-proof budget reached");reject(fatal);},Math.max(0,(7800-(mono()-started))*1000));});
  await Promise.race([(async()=>{
  checkpoint("prospective-opened");
  checkpointTimer=setInterval(()=>{try{checkpoint("periodic");}catch(e){fatal=e;}},30000);
  server=http.createServer((req,res)=>{
   try{
    const u=new URL(req.url,ORIGIN),rel=decodeURIComponent(u.pathname)==="/"? "index.html":decodeURIComponent(u.pathname).replace(/^\//,"");
    if(["GET","HEAD"].includes(req.method)&&u.pathname==="/favicon.ico"){be({kind:"http-response",path:u.pathname,status:204,testHarnessEmptyFavicon:true});res.writeHead(204);res.end();return;}
    if(!["GET","HEAD"].includes(req.method)||!cfg.servedFiles[rel]){be({kind:"http-response",path:u.pathname,status:404,expectedOptionalMissing:u.pathname==="/data/supabase-config.local.js"});res.writeHead(404);res.end();return;}
    const file=path.resolve(root,rel);need(file.toLowerCase().startsWith(root.toLowerCase()+path.sep),"Static source path contained");
    const raw=fs.readFileSync(file);need(digest(raw)===cfg.servedFiles[rel].sha256,"Unchanged served product source "+rel);
    const type=({".html":"text/html; charset=utf-8",".css":"text/css; charset=utf-8",".js":"text/javascript; charset=utf-8",".json":"application/json; charset=utf-8"})[path.extname(file)]||"application/octet-stream";
    be({kind:"http-response",path:u.pathname,status:200,bytes:raw.length});res.writeHead(200,{"Content-Type":type,"Cache-Control":"no-store"});res.end(req.method==="HEAD"?undefined:raw);
   }catch(e){fatal=e;res.writeHead(500);res.end();}
  });
  await new Promise((resolve,reject)=>{server.once("error",reject);server.listen({host:"127.0.0.1",port:8765,exclusive:true},resolve);});
  be({kind:"server-bound",host:"127.0.0.1",port:8765,origin:ORIGIN,pid:process.pid,address:server.address(),portClaimedExclusively:true});
  const {chromium}=require(cfg.playwrightModule);
  browser=await chromium.launch({executablePath:cfg.browserExecutable,headless:true,chromiumSandbox:true,timeout:30000});
  context=await browser.newContext({viewport:{width:1280,height:900},locale:"de-DE",timezoneId:"Europe/Berlin",ignoreHTTPSErrors:false});
  be({kind:"isolated-browser-created",version:browser.version(),cookiesAtCreation:(await context.cookies()).length,syntheticOnly:true});
  await context.exposeBinding("__ACCAOUI_W01_PASSIVE_EMIT",(_source,payload)=>{
   try{if(payload.kind==="timer-observed"){te(payload);if(payload.display==="00:00")zeroSeen++;}else{be(payload);if(payload.kind==="exam-start-ui")examStarts++;if(payload.kind==="terminal-render")terminalSeen++;}}catch(e){fatal=e;}
  });
  await context.addInitScript(observerInit,{binding:"__ACCAOUI_W01_PASSIVE_EMIT"});
  page=await context.newPage();page.setDefaultTimeout(15000);page.setDefaultNavigationTimeout(30000);
  await page.route("**/*",async route=>{const u=new URL(route.request().url());if(u.origin===ORIGIN)await route.continue();else{be({kind:"forbidden-external-request",origin:u.origin});fatal=new Error("Unexpected external request");await route.abort();}});
  page.on("console",msg=>{const location=msg.location();const expectedOptional404=msg.type()==="error"&&msg.text().includes("404")&&String(location.url||"").startsWith(ORIGIN+"/data/supabase-config.local.js");ce({kind:"console-message",level:msg.type(),text:msg.text(),location,expectedOptional404});if(msg.type()==="error"&&!expectedOptional404)fatal=new Error("Unexpected console error: "+msg.text());});
  page.on("pageerror",err=>{ce({kind:"page-error",text:String(err)});fatal=err;});
  page.on("crash",()=>{be({kind:"browser-page-crash"});fatal=new Error("Browser core lost");});
  browser.on("disconnected",()=>{if(!sealed)fatal=new Error("Browser connection lost");});
  be({kind:"navigation-request",url:ORIGIN+"/index.html",firstBrowserNavigation:true});
  await page.goto(ORIGIN+"/index.html",{waitUntil:"load"});
  await page.waitForFunction(()=>typeof allQuestions!=="undefined"&&Array.isArray(allQuestions)&&allQuestions.length>=82);
  need(!fatal,"Healthy initial browser; "+String(fatal||""));
  const clean=await snapshot("before-exam");need(Object.keys(clean.storage).length>=0&&!clean.storage.accaoui_active_session&&!clean.storage.accaoui_exam_history,"Fresh isolated synthetic attempt");
  await page.locator("#examCard").click();
  const full=page.locator('.hero-card[onclick*="startExamMode"][onclick*="full"]');
  need(await full.count()===1,"One observed full simulation UI card");
  be({kind:"action-full-start-request",userFlow:"click full simulation card"});
  await full.click();
  await page.locator("#examTimer").waitFor();
  const startedSnapshot=await snapshot("exam-start");
  const session=JSON.parse(startedSnapshot.storage.accaoui_active_session);
  need(session.sessionType==="exam"&&session.examType==="full"&&session.questions.length===82&&session.questions.reduce((n,q)=>n+Number(q.points),0)===120,"Actual 82-question 120-point full simulation");
  need(startedSnapshot.timer==="120:00"&&session.secondsLeft===7200,"Actual unmodified 120:00 start");
  need(examStarts===1,"One actual UI exam start");
  cases=chooseCases(session);be({kind:"grading-cases-bound",attemptId:session.attemptId,cases});
  await page.locator("#examNavToggle").click();
  for(const c of cases){await page.locator("#examNav .exam-nav-btn").nth(c.index).click();for(const answer of c.selected)await page.locator("#examQuestionArea .answer-btn[data-index='"+answer+"']").click();be({kind:"answer-case-ui",case:c.kind,index:c.index,selected:c.selected,expectedPoints:c.expected});}
  const answered=await snapshot("synthetic-answers-set"),active=JSON.parse(answered.storage.accaoui_active_session);
  need(cases.every(c=>JSON.stringify([...(active.answers[c.index]||[])].sort())===JSON.stringify([...c.selected].sort())),"UI answers persisted");
  need(cases.reduce((n,c)=>n+score(active.questions[c.index],active.answers[c.index]),0)===4,"Independently expected four points incl true partial and wrong/open cases");
  fs.writeFileSync(claim,JSON.stringify({...claimRecord,examStarts:1,attemptId:session.attemptId},null,2)+"\n");
  let lastStorage=mono();
  while(true){
   if(fatal)throw fatal;
   need(mono()-started<7800,"TIMEOUT: unchanged 7800s maximum reached");
   const state=await page.evaluate(()=>({timer:document.getElementById("examTimer")?.textContent||null,result:document.querySelector(".result-wrapper .result-hero")!==null}));
   if(state.result)break;
   if(mono()-lastStorage>=30){await snapshot("natural-countdown");lastStorage=mono();}
   await new Promise(resolve=>setTimeout(resolve,5000));
  }
  terminalSnapshot=await snapshot("terminal");
  const history=JSON.parse(terminalSnapshot.storage.accaoui_exam_history||"[]"),terminal=JSON.parse(terminalSnapshot.storage.accaoui_active_session||"null");
  need(zeroSeen===1&&terminalSeen===1&&examStarts===1,"Observed one 00:00 and one automatic result");
  need(history.length===1&&history[0].attemptId===session.attemptId&&history[0].total===82&&history[0].points.max===120&&history[0].points.reached===4&&history[0].correct===2&&history[0].wrong===2&&history[0].unanswered===78,"Exactly one correctly graded terminal history record");
  need(terminal?.attemptStatus==="completed"&&terminal.secondsLeft===0,"Terminal session at zero");
  const stats=Object.fromEntries(terminalSnapshot.stats);need(stats.Gesamtfragen==="82"&&stats.Richtig==="2"&&stats.Falsch==="2"&&stats.Unbeantwortet==="78"&&stats.Punkte==="4/120","Real terminal UI counts and points");
  be({kind:"terminal-state-checked",attemptId:session.attemptId,stats,historyRecords:history.length,automatic:true});
  await new Promise(resolve=>setTimeout(resolve,2000));
  be({kind:"post-terminal-reload-request"});await page.reload({waitUntil:"load"});
  await page.waitForFunction(()=>typeof allQuestions!=="undefined"&&allQuestions.length>=82);
  const reloaded=await snapshot("after-reload"),historyAfter=JSON.parse(reloaded.storage.accaoui_exam_history||"[]"),savedAfter=JSON.parse(reloaded.storage.accaoui_active_session||"null");
  need(!reloaded.timer&&!reloaded.resumeOffered&&reloaded.resultCount===0&&historyAfter.length===1&&historyAfter[0].attemptId===session.attemptId&&JSON.stringify(historyAfter)===JSON.stringify(history)&&(!savedAfter||savedAfter.attemptStatus==="completed"),"Reload preserves one result without false resume");
  be({kind:"reload-state-checked",historyRecords:1,resumeOffered:false,timerPresent:false,attemptId:session.attemptId});
  if(fatal)throw fatal;
  need(mono()-started<7800,"Completion within original browser maximum");
  clearInterval(checkpointTimer);checkpointTimer=null;
  seal("COMPLETE");
  const validator=spawnSync(cfg.pythonExecutable,["-X","utf8","-B",path.join(root,"tools/check-written-timeout-browser-proof-v1.py"),"--verify",out],{encoding:"utf8",timeout:60000});
  fs.writeFileSync(path.join(out,"independent-verification.stdout"),validator.stdout||"");fs.writeFileSync(path.join(out,"independent-verification.stderr"),validator.stderr||"");
  need(validator.status===0&&!validator.stderr?.trim(),"Independent complete raw-evidence verification: "+String(validator.stderr||validator.stdout));
  need(!fatal&&mono()-started<7800,"Complete independent verification within unchanged 7800s maximum");
  fs.writeFileSync(path.join(out,"result.json"),JSON.stringify({state:"REAL_NATURAL_BROWSER_PROOF_PASS",runId:cfg.runId,exitCode:0,examStarts,terminalSeen,zeroSeen,seconds:mono()-started,verification:JSON.parse(validator.stdout)},null,2)+"\n");
  console.log(JSON.stringify({state:"REAL_NATURAL_BROWSER_PROOF_PASS",runId:cfg.runId,seconds:mono()-started,evidenceDirectory:out}));
  })(),deadline]);
 }catch(error){
  if(checkpointTimer)clearInterval(checkpointTimer);
  if(!sealed){try{be({kind:"fatal-error",message:String(error)});seal("INCOMPLETE",String(error));}catch(captureError){fs.writeFileSync(path.join(out,"capture-failure.json"),JSON.stringify({error:String(error),captureError:String(captureError),utc:utc(),monotonic:mono()}));}}
  fs.writeFileSync(path.join(out,"result.json"),JSON.stringify({state:"STOPP_NOT_VERIFIED",runId:cfg.runId,exitCode:1,error:String(error),examStarts,terminalSeen,zeroSeen,seconds:mono()-started,noAutomaticRetry:true},null,2)+"\n");
  console.log(JSON.stringify({state:"STOPP_NOT_VERIFIED",error:String(error),runId:cfg.runId,examStarts,evidenceDirectory:out}));process.exitCode=1;
 }finally{
  if(checkpointTimer)clearInterval(checkpointTimer);
  if(deadlineTimer)clearTimeout(deadlineTimer);
  for(const fd of Object.values(fds)){try{fs.closeSync(fd);}catch{}}
  // All core streams are fully read/hashed and sealed before any owned cleanup.
  const cleanup={utc:utc(),monotonic:mono(),coreSealed:sealed,ownBrowserClosed:false,ownServerClosed:false};
  if(browser){await browser.close();cleanup.ownBrowserClosed=true;}
  if(server){await new Promise(resolve=>server.close(resolve));cleanup.ownServerClosed=true;}
  fs.writeFileSync(path.join(out,"cleanup.json"),JSON.stringify(cleanup,null,2)+"\n");
 }
}
module.exports={score,chooseCases,observerInit};
if(require.main===module)main().catch(e=>{console.error(String(e));process.exitCode=1;});
