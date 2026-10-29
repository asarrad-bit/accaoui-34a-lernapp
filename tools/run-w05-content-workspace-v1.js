/* W05 local user-flow inventory and acceptance. No natural timeout proof. */
"use strict";
const fs=require("fs"),path=require("path"),http=require("http"),crypto=require("crypto");
const {spawnSync}=require("child_process");
const sha=b=>crypto.createHash("sha256").update(b).digest("hex");
const need=(v,m)=>{if(!v)throw Error(m);};
const utc=()=>new Date().toISOString();
async function main(){
 const cfg=JSON.parse(fs.readFileSync(path.resolve(process.argv[2]),"utf8"));
 const root=path.resolve(cfg.root),out=path.resolve(cfg.output),origin="http://127.0.0.1:8784";
 need(root.toLowerCase()==="c:\\xampp\\htdocs\\accaoui\\v4-dashboard","exact existing checkout");
 need(out.toLowerCase().startsWith(path.resolve(cfg.evidenceDirectory).toLowerCase()+path.sep),"private child output");
 need(cfg.mode==="acceptance"&&cfg.task==="ACCAOUI_DEVELOPMENT_SEQUENCE_W05","explicit W05 inventory only");
 need(!fs.existsSync(out),"never overwrite or restart an inventory run");
 const manifest=JSON.parse(fs.readFileSync(cfg.manifestPath));
 need(sha(fs.readFileSync(cfg.manifestPath))===cfg.manifestSHA256,"independent manifest pin");
 const exact=()=>{
  for(const [name,pin] of Object.entries(manifest.candidate)){
   const b=fs.readFileSync(path.join(root,name));need(b.length===pin.bytes&&sha(b)===pin.sha256,"candidate "+name);
  }
  for(const [name,pin] of Object.entries(cfg.servedFiles)){
   const b=fs.readFileSync(path.join(root,name));need(b.length===pin.bytes&&sha(b)===pin.sha256,"served source "+name);
  }
  const b=fs.readFileSync(cfg.browserExecutable);need(b.length===cfg.browserPin.bytes&&sha(b)===cfg.browserPin.sha256,"browser pin");
 };
 exact();fs.mkdirSync(out);
 const save=(name,value)=>fs.writeFileSync(path.join(out,name),JSON.stringify(value,null,2)+"\n",{flag:"wx"});
 const events=[];let server,browser,failure;
 const result={schema:1,state:cfg.mode==="inventory"?"W05_INVENTORY_RUNNING":"W05_FUNCTIONAL_ACCEPTANCE_RUNNING",startedUtc:utc(),task:cfg.task,manifestSHA256:cfg.manifestSHA256,mode:cfg.mode,snapshots:[],pageErrors:[],externalRequests:[],naturalTimeoutProof:false,fullProductAcceptance:false,physicalDeviceAcceptance:false};
 const env={...process.env,ACCAOUI_SEQUENCE_MANIFEST_PATH:cfg.manifestPath,ACCAOUI_SEQUENCE_MANIFEST_SHA256:cfg.manifestSHA256,ACCAOUI_W02_RUNTIME_SHA256:cfg.runtimeSHA256};
 const guard=name=>{
  const r=spawnSync(cfg.pythonExecutable,["-X","utf8","-W","error::SyntaxWarning","tools/check-development-queue-v1.py"],{cwd:root,env,windowsHide:true,encoding:null,maxBuffer:8*1024*1024});
  fs.writeFileSync(path.join(out,name+".stdout.txt"),r.stdout||Buffer.alloc(0),{flag:"wx"});
  fs.writeFileSync(path.join(out,name+".stderr.txt"),r.stderr||Buffer.alloc(0),{flag:"wx"});
  need(!r.error&&r.status===0&&r.stderr.length===0,"native exact guard "+name);
  return JSON.parse(r.stdout.toString("utf8"));
 };
 try{
  result.preGuard=guard("pre-guard");
  await runPureW05(root,result,need);
  server=http.createServer((req,res)=>{
   try{
    const u=new URL(req.url,origin);const rel=decodeURIComponent(u.pathname)==="/"?"index.html":decodeURIComponent(u.pathname).slice(1);
    if(req.method!=="GET"||!Object.hasOwn(cfg.servedFiles,rel)){events.push({kind:"unserved-local-request",path:rel});res.writeHead(404);res.end();return;}
    const b=fs.readFileSync(path.join(root,rel));need(sha(b)===cfg.servedFiles[rel].sha256,"asset changed "+rel);
    const mime=rel.endsWith(".js")?"application/javascript":rel.endsWith(".css")?"text/css":rel.endsWith(".json")?"application/json":"text/html";
    res.writeHead(200,{"Content-Type":mime+"; charset=utf-8","Cache-Control":"no-store"});res.end(b);
   }catch(e){events.push({kind:"server-error",error:String(e)});res.writeHead(500);res.end();}
  });
  await new Promise((resolve,reject)=>{server.once("error",reject);server.listen({host:"127.0.0.1",port:8784,exclusive:true},resolve);});
  const {chromium}=require(cfg.playwrightModule);
  browser=await chromium.launch({executablePath:cfg.browserExecutable,headless:true,chromiumSandbox:true,timeout:30000});
  for(const profile of [{id:"desktop",viewport:{width:1440,height:1000},isMobile:false},{id:"mobile-viewport",viewport:{width:390,height:844},isMobile:true}]){
   const ctx=await browser.newContext({viewport:profile.viewport,isMobile:profile.isMobile,locale:"de-DE",timezoneId:"Europe/Berlin",serviceWorkers:"block"});
   try{
    await ctx.route("**/*",route=>{
     if(new URL(route.request().url()).origin===origin)return route.continue();
     result.externalRequests.push(route.request().url());return route.abort();
    });
    const page=await ctx.newPage();page.setDefaultTimeout(10000);
    page.on("pageerror",e=>result.pageErrors.push({profile:profile.id,error:String(e)}));
    page.on("console",m=>{if(m.type()==="error")events.push({kind:"console-error",profile:profile.id,text:m.text()});});
    const home=async()=>{await page.goto(origin,{waitUntil:"load"});await page.waitForFunction(()=>typeof allQuestions!=="undefined"&&allQuestions.length>0&&document.querySelector("#examDateWrittenV1Form")&&document.querySelector("#mobileBottomNavV227")&&document.querySelector("#learningGuidanceV1"));};
    const snap=async id=>{
     const data=await page.evaluate(()=>({heading:[...document.querySelectorAll("main h1,main h2")].map(e=>e.textContent.trim()),text:document.querySelector("main")?.innerText.slice(0,5000),editor:document.querySelector("#contentWorkspaceV1")?.innerText.slice(0,8000),mode:typeof currentMode==="undefined"?null:currentMode,questions:typeof allQuestions==="undefined"?null:allQuestions.length,buttons:[...document.querySelectorAll("button,[onclick],input,.menu-item")].map(e=>({tag:e.tagName,id:e.id,classes:e.className,type:e.getAttribute("type"),text:e.innerText?.trim().slice(0,150),onclick:e.getAttribute("onclick"),visible:!!e.getClientRects().length})),viewport:{width:innerWidth,height:innerHeight,documentWidth:document.documentElement.scrollWidth},storageKeys:Object.keys(localStorage).sort()}));
     const file=profile.id+"-"+id+".png";await page.screenshot({path:path.join(out,file),fullPage:true});
     result.snapshots.push({id:profile.id+":"+id,utc:utc(),screenshot:file,...data});
     save("progress-"+result.snapshots.length+".json",{state:result.state,latest:result.snapshots.at(-1)});
    };
    await home();await snap("dashboard");
    for(const [id,locator] of [["all-questions",()=>page.locator("#allQuestionsCard")],["open-questions",()=>page.locator("#openQuestionsCard")],["flashcards",()=>page.locator("#flashcardsMenu")],["written-start",()=>page.locator("#examCard")],["mistakes",()=>page.locator("#mistakeTrainingCard")],["oral",()=>page.locator(".menu-item").filter({hasText:"Mündliche Prüfung"})],["statistics",()=>page.locator("#statsMenu")]]){
     await home();
     if(profile.isMobile&&["flashcards","oral","statistics"].includes(id)){
      if(id==="flashcards")await page.locator('[data-mobile-target="flashcards"]').click();
      else{
       await page.locator('[data-mobile-target="more"]').click();
       const target=id==="statistics"?"stats":"oral";
       await page.locator("#mobileMoreSheetV227 button").filter({has:page.locator('strong', {hasText:id==="statistics"?"Statistik":"Mündliche Prüfung"})}).click();
      }
     }else await locator().click();
     await snap(id);
    }
    if(cfg.mode==="acceptance")await runFunctionalW05({page,home,snap,profile,result,need,out});
   }finally{await ctx.close();}
  }
  need(result.cases?.length===24&&result.cases.every(x=>x.status==="PASS")&&result.pureCases?.length===20&&result.pureCases.every(x=>x.status==="PASS"),"all exact new W05 functional cases");
  need(result.externalRequests.length===0,"no external requests");
  exact();result.postGuard=guard("post-guard");need(JSON.stringify(result.preGuard)===JSON.stringify(result.postGuard),"exact unchanged guard snapshots");
  need(result.pageErrors.length===0,"no unhandled browser errors");
  result.state=cfg.mode==="inventory"?"W05_UI_INVENTORY_COMPLETE_ACCEPTANCE_PENDING":"W05_FUNCTIONAL_CASES_COMPLETE_FULL_ACCEPTANCE_PENDING";
 }catch(e){failure=e;result.state=cfg.mode==="inventory"?"W05_UI_INVENTORY_FAILED":"W05_FUNCTIONAL_CASE_FAILURE";result.error=String(e);result.stack=e.stack;}
 finally{
  if(browser)await browser.close();if(server)await new Promise(resolve=>server.close(resolve));
  result.endedUtc=utc();save("events.json",events);save("result.json",result);console.log(JSON.stringify({state:result.state,snapshots:result.snapshots.length,error:result.error||null,fullProductAcceptance:false,output:out}));
 }
 if(failure)throw failure;
}
main().catch(e=>{console.error(e.stack);process.exitCode=1;});

async function runPureW05(root,result,need){
 const a=require(path.join(root,"data/content-workspace-v1.js"));result.pureCases=[];
 const at="2026-10-27T10:00:00.000Z",category=a.CATEGORIES[1];
 const denied=async fn=>{let rejected=false;try{await fn();}catch(_){rejected=true;}need(rejected,"operation must reject");};
 const check=async(id,fn)=>{const row={id,status:"RUNNING",startedUtc:utc()};result.pureCases.push(row);try{await fn();row.status="PASS";}catch(e){row.status="FAIL";row.error=String(e);throw e;}finally{row.endedUtc=utc();}};
 function fixture(initial={}){
  const data=new Map(Object.entries(initial)),storage={getItem:k=>data.has(k)?data.get(k):null,setItem:(k,v)=>data.set(k,String(v)),removeItem:k=>data.delete(k)};
  let actor={id:"admin-a",role:"admin",active:true,courseIds:["c1"]};
  const repo=a.createRepository({storage,lock:fn=>fn(),utcNow:()=>at}),service=a.createService({repository:repo,resolveActor:async()=>actor});
  const state=()=>repo.read().state,rev=()=>state().revision;
  const course={id:"c1",title:"Synthetischer Kurs",startDay:"2026-01-01",endDay:"2026-12-31",status:"active",instructorIds:["teacher"]};
  const source={id:"s1",title:"Synthetische Eigenquelle",locator:"synthetic:fixture",usage:"own",ownerReviewed:true};
  const written=(id="e1")=>({id,bank:"written",courseId:"c1",sourceId:"s1",category,question:"Synthetische Frage "+id,points:1,answers:["OptionA","OptionB","OptionC","OptionD"],correct:[0],explanation:"Synthetische Erklärung"});
  const setup=async()=>{await service.saveCourse(course,rev());await service.saveSource(source,rev());};
  return {data,storage,repo,service,state,rev,course,source,written,setup,setActor:x=>actor=x};
 }
 await check("default-read-no-write",async()=>{const f=fixture();need(f.repo.read().ok&&f.data.size===0,"read defaults without mutation");});
 await check("corrupt-state-preserved",async()=>{const f=fixture({[a.KEY]:"{broken",other:"keep"});need(!f.repo.read().ok,"corrupt reported");await denied(()=>f.service.saveCourse(f.course,0));need(f.storage.getItem(a.KEY)==="{broken"&&f.storage.getItem("other")==="keep","preserve all bytes");});
 await check("no-provider-default-deny",async()=>{const f=fixture();const service=a.createService({repository:f.repo});await denied(()=>service.saveCourse(f.course,0));need(f.rev()===0,"no optimistic unverified access");});
 await check("participant-cannot-write",async()=>{const f=fixture();f.setActor({id:"p",role:"participant",active:true,courseIds:["c1"]});await denied(()=>f.service.saveCourse(f.course,0));await denied(()=>f.service.list());need(f.rev()===0,"deny participant editor");});
 await check("inactive-unknown-role-denied",async()=>{need(!a.can({id:"a",role:"admin",active:false,courseIds:[]},"courses",null)&&!a.can({id:"a",role:"owner",active:true,courseIds:[]},"courses",null),"closed role contract");});
 await check("course-calendar-validation",async()=>{const f=fixture();await denied(()=>f.service.saveCourse({...f.course,startDay:"2026-02-30"},0));await denied(()=>f.service.saveCourse({...f.course,endDay:"2025-01-01"},0));need(f.rev()===0,"invalid period atomic");});
 await check("written-format-and-points",async()=>{const f=fixture();await f.setup();const before=f.rev();await denied(()=>f.service.saveEntry({...f.written(),correct:[0,1]},f.rev()));await denied(()=>f.service.saveEntry({...f.written(),answers:["a","a","b","c"]},f.rev()));need(f.rev()===before,"invalid answer logic not persisted");});
 await check("separate-three-bank-payloads",async()=>{const f=fixture();await f.setup();await f.service.saveEntry(f.written(),f.rev());await f.service.saveEntry({id:"oral",bank:"oral",courseId:"c1",sourceId:"s1",category,question:"Synthetische mündliche Frage",modelAnswer:"Muster",followUps:"Nachfrage",criticalMistakes:"Fehler"},f.rev());await f.service.saveEntry({id:"card",bank:"card",courseId:"c1",sourceId:"s1",category,question:"Synthetische Kartenvorderseite",back:"Rückseite"},f.rev());need(new Set(f.state().entries.map(e=>e.bank)).size===3,"three explicit separate banks");});
 await check("normalized-duplicate-rejected",async()=>{const f=fixture();await f.setup();const e=f.written();await f.service.saveEntry(e,f.rev());await denied(()=>f.service.saveEntry({...f.written("e2"),question:"  "+e.question.toUpperCase()+"  "},f.rev()));need(f.state().entries.length===1,"duplicate not inserted");});
 await check("mixed-import-atomic-and-no-preapproval",async()=>{const f=fixture();await f.setup();const before=f.rev();await denied(()=>f.service.importDrafts(JSON.stringify({schema:1,entries:[f.written(),{...f.written("x"),status:"published"}]}),f.rev()));need(f.rev()===before&&f.state().entries.length===0,"entire batch rejected");await f.service.importDrafts(JSON.stringify({schema:1,entries:[f.written()]}),f.rev());need(f.state().entries[0].status==="draft","all imports drafts");});
 await check("cross-course-instructor-denied",async()=>{const f=fixture();await f.setup();f.setActor({id:"other-teacher",role:"instructor",active:true,courseIds:["c1"]});await denied(()=>f.service.saveEntry(f.written(),f.rev()));need((await f.service.list()).courses.length===0,"server actor claim alone does not replace course assignment");});
 await check("instructor-edit-without-admin-release",async()=>{const f=fixture();await f.setup();f.setActor({id:"teacher",role:"instructor",active:true,courseIds:["c1"]});await f.service.saveEntry(f.written(),f.rev());await denied(()=>f.service.transition("e1","approved",{},f.rev()));need((await f.service.list()).entries.length===1,"assigned instructor works but no release");});
 await check("complete-review-and-second-person",async()=>{const f=fixture();await f.setup();await f.service.saveEntry(f.written(),f.rev());await denied(()=>f.service.transition("e1","review",{day:"2026-10-27",checks:{}},f.rev()));await f.service.transition("e1","review",{day:"2026-10-27",checks:Object.fromEntries(a.CHECKS.map(k=>[k,true]))},f.rev());await denied(()=>f.service.transition("e1","approved",{},f.rev()));f.setActor({id:"admin-b",role:"admin",active:true,courseIds:["c1"]});const raw=f.storage.getItem(a.KEY),tampered=JSON.parse(raw);tampered.entries[0].review.checks.facts=false;f.storage.setItem(a.KEY,JSON.stringify(tampered));await denied(()=>f.service.transition("e1","approved",{},f.rev()));f.storage.setItem(a.KEY,raw);await f.service.transition("e1","approved",{},f.rev());await f.service.transition("e1","published",{},f.rev());need((await f.service.published("c1","2026-10-27")).length===1,"only complete review published");});
 await check("unknown-or-analysis-rights-block-release",async()=>{const f=fixture();await f.setup();await f.service.saveSource({...f.source,usage:"analysis"},f.rev());await f.service.saveEntry(f.written(),f.rev());await f.service.transition("e1","review",{day:"2026-10-27",checks:Object.fromEntries(a.CHECKS.map(k=>[k,true]))},f.rev());f.setActor({id:"admin-b",role:"admin",active:true,courseIds:["c1"]});await denied(()=>f.service.transition("e1","approved",{},f.rev()));need(f.state().entries[0].status==="review","analysis source not publishable");});
 await check("source-edit-invalidates-review",async()=>{const f=fixture();await f.setup();await f.service.saveEntry(f.written(),f.rev());await f.service.transition("e1","review",{day:"2026-10-27",checks:Object.fromEntries(a.CHECKS.map(k=>[k,true]))},f.rev());await f.service.saveSource({...f.source,title:"Quelle geändert"},f.rev());need(f.state().entries[0].status==="draft"&&f.state().entries[0].review===null,"all approvals invalidated by source edits");});
 await check("stale-revision-and-entry-version",async()=>{const f=fixture();await f.setup();await f.service.saveEntry(f.written(),f.rev());const old=f.state().entries[0],rev=f.rev();await f.service.saveEntry({...old,question:"Neue Frage"},rev);await denied(()=>f.service.saveEntry({...old,question:"Veraltete Eingabe"},rev));await denied(()=>f.service.saveEntry({...old,question:"Veraltete Eingabe"},f.rev()));need(f.state().entries[0].question==="Neue Frage","no silent old version overwrite");});
 await check("quota-keeps-last-state",async()=>{const f=fixture({other:"keep"});await f.setup();const old=f.storage.getItem(a.KEY);f.storage.setItem=()=>{throw Error("quota");};await denied(()=>f.service.saveEntry(f.written(),f.rev()));need(f.storage.getItem(a.KEY)===old&&f.storage.getItem("other")==="keep","last state and unrelated keys kept");});
 await check("missing-lock-and-unconfirmed-write-denied",async()=>{const f=fixture();const repo=a.createRepository({storage:f.storage});await denied(()=>repo.change(0,{id:"a"},"test","e",()=>{}));f.storage.setItem=()=>{};await denied(()=>f.service.saveCourse(f.course,0));need(f.data.size===0,"no false saved state");});
 await check("participant-course-period-and-draft-isolation",async()=>{const f=fixture();await f.setup();await f.service.saveEntry(f.written(),f.rev());f.setActor({id:"p",role:"participant",active:true,courseIds:["c1"]});need((await f.service.published("c1","2026-10-27")).length===0,"draft invisible");await denied(()=>f.service.published("c1","2027-01-01"));await denied(()=>f.service.published("c2","2026-10-27"));});
 await check("export-is-draft-only-and-no-bank-switch",async()=>{const f=fixture();await f.setup();await f.service.saveEntry(f.written(),f.rev());const old=f.state().entries[0];await denied(()=>f.service.saveEntry({...old,bank:"card",back:"Back"},f.rev()));const exported=JSON.parse(await f.service.exportDrafts("c1"));need(exported.publicationAuthority===false&&exported.entries[0].status==="draft"&&exported.entries[0].review===null&&exported.entries[0].approval===null,"export cannot transfer publication authority");});
 need(result.pureCases.length===20,"exact twenty pure content workflow cases");
}

async function runFunctionalW05({page,home,snap,profile,result,need,out}){
 result.cases||=[];const check=async(id,fn)=>{const row={id:profile.id+":"+id,status:"RUNNING",startedUtc:utc()};result.cases.push(row);try{row.evidence=await fn();row.status="PASS";}catch(e){row.status="FAIL";row.error=String(e);try{await snap("failure-"+id);}catch(_){}throw e;}finally{row.endedUtc=utc();}};
 page.on("dialog",d=>d.accept());
 const get=(p,id)=>p.locator("#content"+id+"V1");
 const idle=async p=>p.waitForFunction(()=>document.querySelector("#contentStatusV1")?.getAttribute("aria-busy")!=="true");
 const action=async(p,id)=>{await get(p,id).click();await idle(p);};
 const data=()=>page.evaluate(()=>ACCAOUI_CONTENT_WORKSPACE_V1.read(localStorage).state);
 const storage=()=>page.evaluate(()=>Object.fromEntries(Object.keys(localStorage).sort().map(k=>[k,localStorage.getItem(k)])));
 const expand=async(p,id)=>{const detail=p.locator("details").filter({has:get(p,id)}).last();if(await detail.getAttribute("open")===null)await detail.locator(":scope > summary").click();};
 const enable=async p=>{await get(p,"AdminOpen").click();await get(p,"Consent").check();await get(p,"Enable").click();await get(p,"WorkspaceBody").waitFor({state:"visible"});};
 const role=async value=>{await get(page,"Role").selectOption(value);};
 const courseSubmit=async p=>{await p.locator("#contentCourseFormV1 button[type=submit]").click();await idle(p);};
 const sourceSubmit=async()=>{await page.locator("#contentSourceFormV1 button[type=submit]").click();await idle(page);};
 const fill=async(bank,id,question)=>{
  await get(page,"New").click();await get(page,"Id").fill(id);await get(page,"Bank").selectOption(bank);await get(page,"EntryCourse").selectOption("c1");await get(page,"Source").selectOption("s1");await get(page,"Category").selectOption("Gewerberecht");await get(page,"Question").fill(question);
  if(bank==="written"){await get(page,"Answers").fill("Option A\nOption B\nOption C\nOption D");await get(page,"Correct").fill("1");await get(page,"Explanation").fill("Synthetische Erklärung für den UI-Test.");}
  if(bank==="oral"){await get(page,"ModelAnswer").fill("Synthetische Musterantwort");await get(page,"FollowUps").fill("Synthetische Nachfrage");await get(page,"Critical").fill("Synthetischer kritischer Fehler");}
  if(bank==="card")await get(page,"Back").fill("Synthetische Rückseite");
 };
 const openEntry=async(p,id)=>p.locator('[data-entry-id="'+id+'"]').click();
 await home();const oldStores=await storage();
 await check("closed-default-consent-and-read-only-empty",async()=>{
  await get(page,"AdminOpen").click();need((await get(page,"Boundary").innerText()).includes("gesperrt"),"real provider remains closed");await get(page,"Enable").click();need(await get(page,"WorkspaceBody").isHidden(),"no implicit local admin enable");
  await get(page,"Consent").check();await get(page,"Enable").click();need(await get(page,"WorkspaceBody").isVisible(),"explicit local synthetic workspace");
  need(JSON.stringify(await storage())===JSON.stringify(oldStores),"empty workspace has no writes");await snap("local-boundary");return {actualAuthAcceptance:false,explicitLocal:true,noInitialWrite:true};
 });
 await check("native-course-period-validation-and-assignment",async()=>{
  await expand(page,"CourseId");await get(page,"CourseId").fill("c1");await get(page,"CourseTitle").fill("Synthetischer Testkurs");await get(page,"CourseStart").fill("2026-10-27");await get(page,"CourseEnd").fill("2026-10-26");await courseSubmit(page);
  need((await data()).revision===0&&(await get(page,"CourseEnd").inputValue())==="2026-10-26","invalid period retains draft");
  await get(page,"CourseStart").fill("2026-01-01");await get(page,"CourseEnd").fill("2099-12-31");await courseSubmit(page);
  need((await data()).courses[0].instructorIds[0]==="demo-teacher","explicit course assignment persisted");return (await data()).courses[0];
 });
 await check("native-source-and-written-answer-validation",async()=>{
  await expand(page,"SourceId");await get(page,"SourceId").fill("s1");await get(page,"SourceTitle").fill("Synthetische Quelle");await get(page,"Locator").fill("synthetic:local-case");await sourceSubmit();
  await fill("written","e1","Synthetische schriftliche Frage");await get(page,"Correct").fill("1,2");const before=(await data()).revision;await action(page,"Save");need((await data()).revision===before&&(await get(page,"Correct").inputValue())==="1,2","invalid answer count cannot save");await get(page,"Correct").fill("1");await action(page,"Save");
  need((await data()).entries[0].status==="draft","native source creates draft only");await snap("written-draft");return {entries:(await data()).entries.length,status:"draft",sourceUsage:"unknown"};
 });
 await check("native-duplicate-preserves-bank",async()=>{
  await fill("written","e2","Synthetische schriftliche Frage");await action(page,"Save");need((await data()).entries.length===1&&(await get(page,"Status").innerText()).includes("Dublette"),"native duplicate rejection");await openEntry(page,"e1");return {exactLocalCount:1};
 });
 await check("native-review-rights-and-independent-release",async()=>{
  for(const key of ["facts","duplicates","rights","wording","answer","explanation","category"])await get(page,"Check-"+key).check();
  await action(page,"Review");need((await data()).entries[0].status==="review","seven native review checks");await action(page,"Approve");need((await data()).entries[0].status==="review","same-person release denied");
  await role("admin-b");await action(page,"Approve");need((await data()).entries[0].status==="review","unknown source rights deny release");
  await get(page,"Usage").selectOption("own");await get(page,"OwnerReviewed").check();await sourceSubmit();need((await data()).entries[0].status==="draft","source changes invalidate review");
  await role("admin-a");await action(page,"Review");need((await data()).entries[0].status==="review","fresh local review");await role("admin-b");await action(page,"Approve");await action(page,"Publish");need((await data()).entries[0].status==="published","independent local release and publication");await snap("local-published");return {status:"published",realPublication:false,sourceOrOwnerApprovalClaim:false};
 });
 await check("native-participant-preview-instructor-edit-invalidates",async()=>{
  await role("participant");need(await get(page,"EditArea").isHidden()&&await get(page,"AdminArea").isHidden(),"participant editor hidden");await expand(page,"PreviewCourse");await get(page,"PreviewCourse").selectOption("c1");await action(page,"Preview");need(await get(page,"PreviewList").locator("li").count()===1,"published only preview");
  await role("instructor");await openEntry(page,"e1");await get(page,"Question").fill("Synthetische schriftliche Frage geändert");await action(page,"Save");need((await data()).entries[0].status==="draft","instructor edit resets publication");await action(page,"Approve");need((await data()).entries[0].status==="draft","instructor cannot approve");
  await role("participant");await action(page,"Preview");need(await get(page,"PreviewList").locator("li").count()===0,"unpublished edit excluded");return {syntheticRoleLogic:true,actualDbAuthAcceptance:false};
 });
 await check("native-oral-and-card-bank-separation",async()=>{
  await role("admin-a");await fill("oral","oral1","Synthetische mündliche Frage");await action(page,"Save");await fill("card","card1","Synthetische Kartenvorderseite");await action(page,"Save");
  const entries=(await data()).entries;need(entries.length===3&&new Set(entries.map(e=>e.bank)).size===3&&!Object.hasOwn(entries[1],"answers")&&!Object.hasOwn(entries[2],"modelAnswer"),"distinct native bank payloads");await snap("three-bank-types");return entries.map(e=>({id:e.id,bank:e.bank,status:e.status}));
 });
 await check("native-file-import-atomic-and-draft-only",async()=>{
  await expand(page,"ImportFile");const e={id:"import1",bank:"card",courseId:"c1",sourceId:"s1",category:"Gewerberecht",question:"Synthetischer Import",back:"Synthetische Rückseite"};const initial=(await data()).revision;
  const upload=async entries=>get(page,"ImportFile").setInputFiles({name:"synthetic.json",mimeType:"application/json",buffer:Buffer.from(JSON.stringify({schema:1,entries}))});
  await upload([e,{...e,id:"import2"}]);await action(page,"Import");need((await data()).revision===initial&&(await data()).entries.length===3,"duplicate batch rolls back entirely");
  await upload([e]);await action(page,"Import");const saved=(await data()).entries.find(x=>x.id==="import1");need(saved.status==="draft"&&saved.review===null,"file imports no publication");return {count:(await data()).entries.length,onlySyntheticFile:true,driveAccess:false};
 });
 await check("native-download-exports-only-drafts",async()=>{
  const downloaded=page.waitForEvent("download");await get(page,"Export").click();const download=await downloaded;const name=profile.id+"-local-drafts.json";await download.saveAs(path.join(out,name));const bytes=fs.readFileSync(path.join(out,name));const exported=JSON.parse(bytes);
  need(exported.entries.length===4&&exported.publicationAuthority===false&&exported.entries.every(e=>e.status==="draft"&&e.review===null),"native local download strips release authority");return {artifact:name,bytes:bytes.length,sha256:sha(bytes),publicationAuthority:false};
 });
 await check("native-quota-keeps-input-and-last-state",async()=>{
  await expand(page,"CourseId");const before=await storage();await page.evaluate(()=>{const original=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k===ACCAOUI_CONTENT_WORKSPACE_V1.KEY)throw new DOMException("synthetic quota","QuotaExceededError");return original.call(this,k,v);};});
  await get(page,"CourseTitle").fill("Nicht gespeicherter Entwurf");await courseSubmit(page);need(JSON.stringify(before)===JSON.stringify(await storage())&&(await get(page,"CourseTitle").inputValue())==="Nicht gespeicherter Entwurf"&&(await get(page,"Status").innerText()).includes("nicht sicher"),"quota keeps last state and visible input");
  await home();await enable(page);return {priorStateAndDraftRetained:true};
 });
 await check("native-two-tab-conflict-and-entry-version",async()=>{
  await openEntry(page,"e1");await get(page,"Question").fill("Ungespeicherte erste Eingabe");const other=await page.context().newPage();other.on("pageerror",e=>result.pageErrors.push({profile:profile.id+":second-tab",error:String(e)}));other.on("console",m=>{if(m.type()==="error")(result.secondTabConsoleErrors||=[]).push({profile:profile.id,text:m.text()});});
  try{
   await other.goto(new URL(page.url()).origin,{waitUntil:"load"});await other.waitForFunction(()=>document.querySelector("#contentAdminOpenV1")&&window.ACCAOUI_CONTENT_WORKSPACE_V1);await enable(other);await openEntry(other,"e1");await get(other,"Question").fill("Gespeicherte zweite Eingabe");await action(other,"Save");
   await page.bringToFront();await page.waitForFunction(()=>document.visibilityState==="visible");await get(page,"Save").scrollIntoViewIfNeeded();await action(page,"Save");need((await data()).entries.find(e=>e.id==="e1").question==="Gespeicherte zweite Eingabe"&&(await get(page,"Question").inputValue())==="Ungespeicherte erste Eingabe","stale revision never overwrites");
   await get(page,"Reload").click();await action(page,"Save");need((await data()).entries.find(e=>e.id==="e1").question==="Gespeicherte zweite Eingabe","stale entry version denied after revision refresh");await openEntry(page,"e1");need((await get(page,"Question").inputValue())==="Gespeicherte zweite Eingabe","explicit reopen sees current content");await snap("conflict-recovery");return {sameBrowserTwoTabs:true,actualDeviceSyncClaim:false};
  }finally{await other.close();}
 });
 await check("native-literal-text-course-archive-and-keyboard",async()=>{
  await openEntry(page,"card1");const literal='Literal <img src="https://invalid.example/x" onerror="window.__w05Xss=1">';await get(page,"Question").fill(literal);await action(page,"Save");need((await get(page,"Entries").innerText()).includes(literal)&&await page.evaluate(()=>window.__w05Xss===undefined),"untrusted content rendered as text");
  await get(page,"Close").focus();for(let n=0;n<8;n++)await page.keyboard.press("Tab");
  const layout=await page.evaluate(()=>{const d=document.querySelector("#contentWorkspaceV1");return {dialogFocus:d.contains(document.activeElement),width:d.clientWidth,scrollWidth:d.scrollWidth,viewport:innerWidth,physicalDevice:false};});
  need(layout.dialogFocus&&layout.scrollWidth<=layout.width+1,"native dialog focus and mobile width");await snap("responsive-editor");
  await expand(page,"CourseId");await get(page,"CourseId").fill("c1");await get(page,"CourseTitle").fill("Synthetischer Testkurs");await get(page,"CourseStart").fill("2026-01-01");await get(page,"CourseEnd").fill("2099-12-31");await get(page,"Instructors").fill("demo-teacher");await get(page,"CourseStatus").selectOption("archived");await courseSubmit(page);
  await role("participant");await expand(page,"PreviewCourse");await get(page,"PreviewCourse").selectOption("c1");await action(page,"Preview");need(await get(page,"PreviewList").locator("li").count()===0&&(await get(page,"Status").innerText()).includes("nicht aktiv"),"archived course denies preview");
  const after=await storage();for(const [k,v]of Object.entries(oldStores))need(after[k]===v,"old participant storage preserved");need(Object.keys(after).every(k=>k==="accaoui_content_workspace_v1"||Object.hasOwn(oldStores,k)),"workspace writes only own key");await get(page,"Close").click();need(await page.locator("#allQuestionsCard").isVisible(),"existing dashboard retained");return {layout,allOldParticipantStoresPreserved:true,actualAuthOrSourceAcceptance:false};
 });
 need(result.cases.filter(x=>x.id.startsWith(profile.id+":")).length===12,"exact twelve W05 local UI cases per viewport");
}
