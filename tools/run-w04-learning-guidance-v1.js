/* W04 local user-flow inventory and acceptance. No natural timeout proof. */
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
 need(cfg.mode==="acceptance"&&cfg.task==="ACCAOUI_DEVELOPMENT_SEQUENCE_W04","explicit W04 inventory only");
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
 const result={schema:1,state:cfg.mode==="inventory"?"W04_INVENTORY_RUNNING":"W04_FUNCTIONAL_ACCEPTANCE_RUNNING",startedUtc:utc(),task:cfg.task,manifestSHA256:cfg.manifestSHA256,mode:cfg.mode,snapshots:[],pageErrors:[],externalRequests:[],naturalTimeoutProof:false,fullProductAcceptance:false,physicalDeviceAcceptance:false};
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
  runPureW04(root,result,need);
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
     const data=await page.evaluate(()=>({heading:[...document.querySelectorAll("main h1,main h2")].map(e=>e.textContent.trim()),text:document.querySelector("main")?.innerText.slice(0,5000),mode:typeof currentMode==="undefined"?null:currentMode,questions:typeof allQuestions==="undefined"?null:allQuestions.length,buttons:[...document.querySelectorAll("button,[onclick],input,.menu-item")].map(e=>({tag:e.tagName,id:e.id,classes:e.className,type:e.getAttribute("type"),text:e.innerText?.trim().slice(0,150),onclick:e.getAttribute("onclick"),visible:!!e.getClientRects().length})),viewport:{width:innerWidth,height:innerHeight,documentWidth:document.documentElement.scrollWidth},storageKeys:Object.keys(localStorage).sort()}));
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
    if(cfg.mode==="acceptance")await runFunctionalW04({page,home,snap,profile,result,need});
   }finally{await ctx.close();}
  }
  need(result.cases?.length===32&&result.cases.every(x=>x.status==="PASS")&&result.pureCases?.length===26&&result.pureCases.every(x=>x.status==="PASS"),"all exact new W04 functional cases");
  need(result.externalRequests.length===0,"no external requests");
  exact();result.postGuard=guard("post-guard");need(JSON.stringify(result.preGuard)===JSON.stringify(result.postGuard),"exact unchanged guard snapshots");
  need(result.pageErrors.length===0,"no unhandled browser errors");
  result.state=cfg.mode==="inventory"?"W04_UI_INVENTORY_COMPLETE_ACCEPTANCE_PENDING":"W04_FUNCTIONAL_CASES_COMPLETE_FULL_ACCEPTANCE_PENDING";
 }catch(e){failure=e;result.state=cfg.mode==="inventory"?"W04_UI_INVENTORY_FAILED":"W04_FUNCTIONAL_CASE_FAILURE";result.error=String(e);result.stack=e.stack;}
 finally{
  if(browser)await browser.close();if(server)await new Promise(resolve=>server.close(resolve));
  result.endedUtc=utc();save("events.json",events);save("result.json",result);console.log(JSON.stringify({state:result.state,snapshots:result.snapshots.length,error:result.error||null,fullProductAcceptance:false,output:out}));
 }
 if(failure)throw failure;
}
main().catch(e=>{console.error(e.stack);process.exitCode=1;});

function runPureW04(root,result,need){
 const a=require(path.join(root,"data/learning-guidance-v1.js"));
 result.pureCases=[];
 const check=(id,fn)=>{const row={id,status:"RUNNING"};result.pureCases.push(row);try{fn();row.status="PASS";}catch(e){row.status="FAIL";row.error=String(e);throw e;}};
 const eq=(x,y,m)=>need(JSON.stringify(x)===JSON.stringify(y),m);
 const at=s=>new Date(s+"T12:00:00");
 const memory=initial=>{const data=new Map(Object.entries(initial||{}));return {data,getItem:k=>data.has(k)?data.get(k):null,setItem:(k,v)=>data.set(k,String(v)),removeItem:k=>data.delete(k)};};
 check("calendar-leap-invalid",()=>{need(a.ordinal("2024-02-29")!==null&&a.ordinal("2023-02-29")===null&&a.ordinal("2026-02-30")===null,"real dates only");});
 check("calendar-year-boundary",()=>eq(a.addDays("2026-12-31",1),"2027-01-01","calendar boundary"));
 check("calendar-DST-days",()=>{eq(a.addDays("2026-03-28",2),"2026-03-30","spring days");eq(a.addDays("2026-10-24",2),"2026-10-26","autumn days");});
 check("first-rating-next-day",()=>eq(a.nextReview(null,"known",at("2026-10-27")),{schema:1,stage:1,reviewedDay:"2026-10-27",dueDay:"2026-10-28"},"first self-rating is not mastery"));
 check("early-repeat-cannot-postpone",()=>{const entry={lastStatus:"known",review:{schema:1,stage:2,reviewedDay:"2026-10-25",dueDay:"2026-10-28"}};eq(a.nextReview(entry,"known",at("2026-10-27")),entry.review,"early rating retains scheduled due day");});
 check("due-success-advances",()=>{const entry={lastStatus:"known",review:{schema:1,stage:1,reviewedDay:"2026-10-27",dueDay:"2026-10-28"}};need(a.nextReview(entry,"known",at("2026-10-28")).dueDay==="2026-10-31","due self-rating advances interval");});
 check("unknown-resets-interval",()=>{const r=a.nextReview({lastStatus:"known",review:{schema:1,stage:5,reviewedDay:"2026-09-01",dueDay:"2026-10-01"}},"unknown",at("2026-10-27"));need(r.stage===0&&r.dueDay==="2026-10-28","unknown resets to one day");});
 check("legacy-count-not-spaced-mastery",()=>{const r=a.reviewOf({lastStatus:"known",knownCount:999,updatedAt:"2026-10-25T12:00:00"},at("2026-10-27"));need(r.legacy&&r.stage===0&&r.dueDay==="2026-10-26","old count cannot imply spaced success");});
 check("invalid-legacy-date-still-due",()=>eq(a.dueKeys({x:{lastStatus:"unknown",updatedAt:"bad"}},["x"],at("2026-10-27")),["x"],"damaged legacy date must not suppress review"));
 check("future-legacy-clock-still-due",()=>eq(a.dueKeys({x:{lastStatus:"known",updatedAt:"2099-01-01"}},["x"],at("2026-10-27")),["x"],"future legacy time cannot hide card"));
 check("foreign-and-duplicate-keys",()=>eq(a.dueKeys({x:{lastStatus:"unknown",updatedAt:"2000-01-01"},foreign:{lastStatus:"known",updatedAt:"2000-01-01"}},["x","x","absent"],at("2026-10-27")),["x"],"only real unique bank keys"));
 check("damaged-review-due-conservatively",()=>eq(a.dueKeys({x:{lastStatus:"known",review:{stage:9,dueDay:"2099-01-01"}}},["x"],at("2026-10-27")),["x"],"malformed future schedule cannot hide card"));
 check("default-read-does-not-write",()=>{const s=memory();need(a.readState(s).ok&&s.data.size===0,"default read has no writes");});
 check("corrupt-state-never-overwritten",()=>{const s=memory({[a.KEY]:"{bad",other:"keep"});need(!a.savePreferences(s,a.defaults().preferences).ok&&s.getItem(a.KEY)==="{bad"&&s.getItem("other")==="keep","retain corrupt input");});
 check("storage-read-error-closed",()=>need(!a.readState({getItem(){throw Error("denied");}}).ok,"unavailable storage is reported"));
 check("quota-preserves-state",()=>{const s=memory();a.savePreferences(s,a.defaults().preferences);const old=s.getItem(a.KEY);s.setItem=()=>{throw Error("quota");};need(!a.savePreferences(s,{...a.defaults().preferences,minutes:60}).ok&&s.getItem(a.KEY)===old,"failed write keeps last state");});
 check("unconfirmed-write-rejected",()=>{const s=memory();s.setItem=()=>{};need(!a.savePreferences(s,a.defaults().preferences).ok,"no false saved status");});
 check("objective-and-self-rating-separated",()=>{const s=memory();a.activity(s,"written",3,2,at("2026-10-27"));a.activity(s,"card",5,0,at("2026-10-27"));eq(a.readState(s).state.daily,{day:"2026-10-27",answers:3,correct:2,cardRatings:5},"card ratings never become correct answers");});
 check("preference-save-keeps-fresh-counters",()=>{const s=memory();a.activity(s,"written",2,1,at("2026-10-27"));a.savePreferences(s,{...a.defaults().preferences,minutes:45});need(a.readState(s).state.daily.correct===1&&a.readState(s).state.preferences.minutes===45,"settings merge preserves activity");});
 check("new-day-resets-only-daily-counters",()=>{const s=memory();a.savePreferences(s,{...a.defaults().preferences,minutes:55});a.activity(s,"written",4,3,at("2026-10-27"));a.activity(s,"card",1,0,at("2026-10-28"));const v=a.readState(s).state;need(v.daily.answers===0&&v.daily.cardRatings===1&&v.preferences.minutes===55,"new day retains settings");});
 check("pause-expires-next-calendar-day",()=>{const p={...a.defaults().preferences,pausedUntil:"2026-10-27"};need(a.buildPlan(p,[],at("2026-10-27")).paused&&!a.buildPlan(p,[],at("2026-10-28")).paused,"pause does not delete future plan");});
 check("deadline-selects-first-upcoming",()=>{const p=a.buildPlan(a.defaults().preferences,["bad","2020-01-01","2026-10-30","2026-10-28"],at("2026-10-27"));need(p.deadline==="2026-10-28"&&p.days===1&&p.reviewPriority,"upcoming real dates only");});
 check("every-budget-keeps-study-time",()=>{for(let minutes=10;minutes<=120;minutes++){const p=a.buildPlan({...a.defaults().preferences,minutes},[],at("2026-10-27"));need(p.blocks.filter(b=>b.kind!=="break").reduce((x,b)=>x+b.minutes,0)===minutes&&p.blocks.every(b=>b.minutes>0&&b.minutes<=25),"budget without phantom measured time");}});
 check("invalid-preferences-rejected",()=>{for(const p of [{minutes:9},{minutes:121},{minutes:20.5},{reminderTime:"25:00"},{pausedUntil:"2026-02-30"}])need(!a.validPreferences({...a.defaults().preferences,...p}),"bounded valid preferences");});
 check("in-app-reminder-and-pause",()=>{const p={...a.defaults().preferences,reminders:true,reminderTime:"00:00"};need(a.buildPlan(p,[],at("2026-10-27")).reminder&&!a.buildPlan({...p,pausedUntil:"2026-10-27"},[],at("2026-10-27")).reminder,"only in-app eligible reminder");});
 check("reset-only-own-key",()=>{const s=memory({[a.KEY]:"{bad",answers:"preserve",exam:"preserve"});need(a.reset(s).ok&&s.data.size===2&&s.getItem("answers")==="preserve"&&s.getItem("exam")==="preserve","only new plan key removed");});
 need(result.pureCases.length===26,"all exact pure W04 cases");
}
async function runFunctionalW04({page,home,snap,profile,result,need}){
 result.cases ||= [];
 const check=async(id,fn)=>{const row={id:profile.id+":"+id,startedUtc:utc(),status:"RUNNING"};result.cases.push(row);try{row.evidence=await fn();row.status="PASS";}catch(e){row.status="FAIL";row.error=String(e);try{await snap("failure-"+id);}catch(_){}throw e;}finally{row.endedUtc=utc();}};
 const storage=()=>page.evaluate(()=>Object.fromEntries(Object.keys(localStorage).sort().map(k=>[k,localStorage.getItem(k)])));
 const plan=()=>page.evaluate(()=>ACCAOUI_LEARNING_GUIDANCE_V1.readState(localStorage));
 const settings=async()=>{await page.locator("#guidanceSettingsV1").evaluate(e=>{e.open=true;});};
 await home();await page.locator("#learningGuidanceV1").waitFor({state:"visible"});
 await check("daily-plan-default-without-writes",async()=>{
  need((await page.locator("#guidancePlanStatusV1").innerText()).includes("20 Minuten"),"real default daily plan");
  const s=await storage();need(!Object.hasOwn(s,"accaoui_learning_guidance_v1"),"read-only default");await snap("plan-default");return {minutes:20,noPlanWrite:true};
 });
 await check("settings-save-reload-breaks",async()=>{
  await settings();await page.locator("#guidanceMinutesV1").fill("60");await page.locator("#guidanceSaveV1").click();await home();
  const s=await plan();need(s.ok&&s.state.preferences.minutes===60,"saved preferences survive reload");
  need((await page.locator("#guidancePlanStatusV1").innerText()).includes("10 Minuten Pause"),"actual break budget");await snap("plan-with-breaks");return s.state.preferences;
 });
 await check("invalid-budget-retains-input-and-state",async()=>{
  await settings();const before=await storage();await page.locator("#guidanceMinutesV1").fill("5");await page.locator("#guidanceSaveV1").click();
  need(JSON.stringify(before)===JSON.stringify(await storage())&&(await page.locator("#guidanceMinutesV1").inputValue())==="5"&&(await page.locator("#guidancePlanErrorV1").innerText()).length>0,"invalid preferences are not saved");await home();return {preserved:true};
 });
 await check("pause-resume-without-progress-reset",async()=>{
  const before=await storage();await page.locator("#guidancePauseV1").click();need(await page.locator("#guidanceBlocksV1 li").count()===0,"pause hides plan blocks");
  await home();need((await plan()).state.preferences.pausedUntil!==null,"pause persists");
  await page.locator("#guidancePauseV1").click();need((await plan()).state.preferences.pausedUntil===null&&(await page.locator("#guidanceBlocksV1 li").count())>0,"plan resumes");
  const after=await storage();for(const k of Object.keys(before))if(k!=="accaoui_learning_guidance_v1")need(before[k]===after[k],"pause does not change progress");return {pausedAndResumed:true};
 });
 await check("in-app-reminder-only",async()=>{
  await settings();await page.locator("#guidanceReminderEnabledV1").check();await page.locator("#guidanceReminderTimeV1").fill("00:00");await page.locator("#guidanceSaveV1").click();
  need((await page.locator("#guidanceReminderV1").innerText()).includes("In-App-Erinnerung"),"visible eligible in-app reminder");return {reminder:(await plan()).state.preferences.reminderTime,externalMessages:false};
 });
 await check("overdue-cards-and-future-card-separated",async()=>{
  const seeded=await page.evaluate(()=>{
   const a=ACCAOUI_LEARNING_GUIDANCE_V1,keys=allQuestions.slice(0,2).map(getFlashcardProgressKey),today=a.day();
   const isolatedSessionKeys=[STORAGE_KEYS.activeSession,STORAGE_KEYS.activeLearningSession,ACTIVE_FLASHCARD_SESSION_KEY_V261C];
   isolatedSessionKeys.forEach(key=>localStorage.removeItem(key));
   if(isolatedSessionKeys.some(key=>localStorage.getItem(key)!==null))throw Error("synthetic empty-session fixture not established");
   const values={[keys[0]]:{lastStatus:"known",knownCount:90,unknownCount:0,updatedAt:"2000-01-01T12:00:00Z"},[keys[1]]:{lastStatus:"known",knownCount:5,updatedAt:new Date().toISOString(),review:{schema:1,stage:5,reviewedDay:today,dueDay:a.addDays(today,30)}}};
   localStorage.setItem(FLASHCARD_PROGRESS_KEY,JSON.stringify(values));return {keys,isolatedSessionKeys};
  });
  await home();const due=await page.evaluate(()=>getDueFlashcardQuestionsV1().map(getFlashcardProgressKey));
  need(due.length===1&&due[0]===seeded.keys[0],"actual due queue excludes future card");need((await page.locator("#guidancePlanStatusV1").innerText()).includes("1 bewertete Karte"),"due count visible");await snap("due-review");return {seeded,due};
 });
 await check("native-due-launch-and-existing-session-priority",async()=>{
  await page.locator("#guidanceBlocksV1 button").first().click();await page.locator("#showFlashcardAnswerBtn").waitFor({state:"visible"});
  const data=await page.evaluate(()=>({count:flashcardQuestions.length,id:flashcardQuestions[0].id}));
  need(data.count===1,"native due action uses existing card flow");await home();
  need((await page.evaluate(()=>getNextLearningStepV2735B().actionHandler))==="resumeActiveFlashcardSession()","existing interrupted session stays first");return data;
 });
 await check("native-card-rating-schedule-and-daily-separation",async()=>{
  await page.locator("#guidanceBlocksV1 button").first().click();await page.locator("#showFlashcardAnswerBtn").click();await page.locator('button[onclick="markFlashcardKnown()"]').click();await home();
  const data=await page.evaluate(()=>{const a=ACCAOUI_LEARNING_GUIDANCE_V1,s=a.readState(localStorage).state,key=getFlashcardProgressKey(allQuestions[0]);return {state:s,entry:JSON.parse(localStorage.getItem(FLASHCARD_PROGRESS_KEY))[key],today:a.day()};});
  need(data.entry.review.schema===1&&data.entry.review.stage===1&&data.entry.review.dueDay>data.today,"real rating saves next review");
  need(data.state.daily.cardRatings===1&&data.state.daily.answers===0&&data.state.daily.correct===0,"self-rating is not objective correct answer");await snap("rating-separated");return data;
 });
 await check("native-checked-answer-daily-progress",async()=>{
  await page.locator("#openQuestionsCard").click();await page.locator("#questionArea .answer-btn").first().waitFor({state:"visible"});
  const q=await page.evaluate(()=>({id:currentQuestions[currentQuestionIndex].id,correct:[...currentQuestions[currentQuestionIndex].correct]}));
  for(const index of q.correct){const button=page.locator('#questionArea .answer-btn[data-index="'+index+'"]');await button.focus();await page.keyboard.press("Enter");}
  const state=await plan();need(state.state.daily.answers===1&&state.state.daily.correct===1&&state.state.daily.cardRatings===1,"real graded answer counted separately");await home();await snap("daily-evidence");return {question:q.id,daily:state.state.daily};
 });
 await check("native-manual-written-result-excludes-open-answers",async()=>{
  await home();const before=(await plan()).state.daily;
  await page.locator("#examCard").click();await page.locator("[onclick*=\"startExamMode\"][onclick*=\"'full'\"]").click();
  const attempt=await page.evaluate(()=>JSON.parse(localStorage.getItem("accaoui_active_session")));
  need(attempt.questions.length===82&&attempt.secondsLeft>7180&&attempt.attemptStatus==="active","real native exam with original duration");
  const index=attempt.questions.findIndex(q=>Number(q.points)===1);need(index>=0,"real one-point question");
  await page.locator("#examNavToggle").click();await page.locator("#examNav .exam-nav-btn").nth(index).click();
  for(const answer of attempt.questions[index].correct)await page.locator('#examQuestionArea .answer-btn[data-index="'+answer+'"]').click();
  await page.locator("#finishExamNowBtn").click();need(await page.locator("#examWarningBox").isVisible(),"real open-answer confirmation");
  await page.locator('#examWarningBox button[onclick="finishExamMode()"]').focus();await page.keyboard.press("Enter");
  await page.locator(".result-wrapper .result-hero").waitFor({state:"visible"});
  const history=await page.evaluate(()=>JSON.parse(localStorage.getItem("accaoui_exam_history")));
  const row=history.find(x=>x.attemptId===attempt.attemptId);need(history.length===1&&row.total===82&&row.correct===1&&row.wrong===0&&row.unanswered===81&&row.points.reached===1&&row.points.max===120,"one actual result, one answered and81open");
  const daily=(await plan()).state.daily;need(daily.answers===before.answers+1&&daily.correct===before.correct+1&&daily.cardRatings===before.cardRatings,"only answered exam question adds objective daily evidence");
  await home();need(JSON.stringify((await plan()).state.daily)===JSON.stringify(daily),"reload does not count result again");
  await snap("manual-written-daily-separation");return {attemptId:attempt.attemptId,historyCount:history.length,correct:row.correct,wrong:row.wrong,unanswered:row.unanswered,dailyBefore:before,dailyAfter:daily,completion:"MANUAL_FUNCTIONAL_NO_CLOCK_PATCH",naturalTimeoutProof:false};
 });
 await check("dates-drive-replan-without-extra-minutes",async()=>{
  const date=await page.evaluate(()=>ACCAOUI_LEARNING_GUIDANCE_V1.addDays(ACCAOUI_LEARNING_GUIDANCE_V1.day(),1));
  await page.locator("#examDateWrittenV1Input").fill(date);await page.locator("#examDateWrittenV1Save").click();await page.locator("#guidanceReplanV1").click();
  const text=await page.locator("#guidancePlanStatusV1").innerText();
  need(text.includes("in 1 Tag")&&text.includes("bekannte Inhalte")&&text.includes("60 Minuten"),"actual saved date adjusts bounded guidance");await snap("deadline-plan");return {date,text};
 });
 await check("corrupt-plan-preserved-and-own-key-recovery",async()=>{
  const before=await storage();await page.evaluate(()=>localStorage.setItem(ACCAOUI_LEARNING_GUIDANCE_V1.KEY,"{synthetic-invalid-plan"));await home();
  need((await page.locator("#guidancePlanErrorV1").innerText()).includes("nicht überschrieben"),"damaged plan reported");
  await settings();await page.locator("#guidanceResetV1").click();
  const after=await storage();need(!Object.hasOwn(after,"accaoui_learning_guidance_v1"),"own plan key reset");
  for(const k of Object.keys(before))if(k!=="accaoui_learning_guidance_v1")need(after[k]===before[k],"all old stores survive plan reset");await snap("safe-plan-recovery");return {otherStoresPreserved:true};
 });
 await check("quota-error-preserves-preferences-and-draft",async()=>{
  await settings();const before=await storage();
  await page.evaluate(()=>{const original=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k===ACCAOUI_LEARNING_GUIDANCE_V1.KEY)throw new DOMException("synthetic W04 quota","QuotaExceededError");return original.call(this,k,v);};});
  await page.locator("#guidanceMinutesV1").fill("45");await page.locator("#guidanceSaveV1").click();
  need(JSON.stringify(await storage())===JSON.stringify(before)&&(await page.locator("#guidanceMinutesV1").inputValue())==="45"&&(await page.locator("#guidancePlanErrorV1").innerText()).includes("nicht sicher"),"quota failure keeps prior state and draft");await home();return {preserved:true};
 });
 await check("second-tab-conflict-requires-explicit-resave",async()=>{
  await settings();await page.locator("#guidanceMinutesV1").fill("55");
  const other=await page.context().newPage();other.on("pageerror",e=>result.pageErrors.push({profile:profile.id+":second-tab",error:String(e)}));try{
   await other.goto(new URL(page.url()).origin,{waitUntil:"load"});await other.waitForFunction(()=>window.ACCAOUI_LEARNING_GUIDANCE_V1);
   await other.evaluate(()=>{const a=ACCAOUI_LEARNING_GUIDANCE_V1,s=a.readState(localStorage).state;return a.savePreferences(localStorage,{...s.preferences,minutes:35});});
   await page.bringToFront();await page.waitForFunction(()=>document.visibilityState==="visible");
   await page.locator("#guidanceSaveV1").scrollIntoViewIfNeeded();
   await page.locator("#guidanceSaveV1").click();need((await plan()).state.preferences.minutes===35&&(await page.locator("#guidanceMinutesV1").inputValue())==="55","fresh foreign setting is not silently overwritten");
   need((await page.locator("#guidancePlanErrorV1").innerText()).includes("inzwischen"),"conflict visibly explained");await page.locator("#guidanceSaveV1").click();
   need((await plan()).state.preferences.minutes===55,"explicit repeated save applies retained draft");return {sameBrowserTwoTabs:true,actualDeviceSyncClaim:false};
  }finally{await other.close();}
 });
 await check("keyboard-focus-and-viewport",async()=>{
  await home();await settings();await page.locator("#guidanceMinutesV1").focus();let focus;
  for(let n=0;n<7;n++){await page.keyboard.press("Tab");focus=await page.evaluate(()=>({id:document.activeElement.id,tag:document.activeElement.tagName}));if(focus.id==="guidanceSaveV1")break;}
  const size=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));
  need(focus.id==="guidanceSaveV1"&&focus.tag==="BUTTON"&&size.scroll<=size.width+1,"native focus order and viewport width");await snap("keyboard-mobile-layout");return {focus,size,physicalDevice:false};
 });
 await check("active-recall-opens-existing-card-flow",async()=>{
  await home();await page.locator("#guidanceBlocksV1 button").nth(1).click();
  need(await page.locator('button[onclick^="startFlashcardSession(allQuestions"]').count()===1,"recall reuses existing card selector, no second bank");return {existingFlashcardsReused:true};
 });
 need(result.cases.filter(x=>x.id.startsWith(profile.id+":")).length===16,"exact sixteen W04 browser cases per profile");
}
