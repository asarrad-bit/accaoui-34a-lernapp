/* W02 local user-flow inventory and acceptance. No natural timeout proof. */
"use strict";
const fs=require("fs"),path=require("path"),http=require("http"),crypto=require("crypto");
const {spawnSync}=require("child_process");
const sha=b=>crypto.createHash("sha256").update(b).digest("hex");
const need=(v,m)=>{if(!v)throw Error(m);};
const utc=()=>new Date().toISOString();
async function main(){
 const cfg=JSON.parse(fs.readFileSync(path.resolve(process.argv[2]),"utf8"));
 const root=path.resolve(cfg.root),out=path.resolve(cfg.output),origin="http://127.0.0.1:8766";
 need(root.toLowerCase()==="c:\\xampp\\htdocs\\accaoui\\v4-dashboard","exact existing checkout");
 need(out.toLowerCase().startsWith(path.resolve(cfg.evidenceDirectory).toLowerCase()+path.sep),"private child output");
 need(["inventory","acceptance"].includes(cfg.mode)&&cfg.task==="ACCAOUI_DEVELOPMENT_SEQUENCE_W02","explicit W02 inventory only");
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
 const result={schema:1,state:cfg.mode==="inventory"?"W02_INVENTORY_RUNNING":"W02_FUNCTIONAL_ACCEPTANCE_RUNNING",startedUtc:utc(),task:cfg.task,manifestSHA256:cfg.manifestSHA256,mode:cfg.mode,snapshots:[],pageErrors:[],externalRequests:[],naturalTimeoutProof:false,fullProductAcceptance:false,physicalDeviceAcceptance:false};
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
  server=http.createServer((req,res)=>{
   try{
    const u=new URL(req.url,origin);const rel=decodeURIComponent(u.pathname)==="/"?"index.html":decodeURIComponent(u.pathname).slice(1);
    if(req.method!=="GET"||!Object.hasOwn(cfg.servedFiles,rel)){events.push({kind:"unserved-local-request",path:rel});res.writeHead(404);res.end();return;}
    const b=fs.readFileSync(path.join(root,rel));need(sha(b)===cfg.servedFiles[rel].sha256,"asset changed "+rel);
    const mime=rel.endsWith(".js")?"application/javascript":rel.endsWith(".css")?"text/css":rel.endsWith(".json")?"application/json":"text/html";
    res.writeHead(200,{"Content-Type":mime+"; charset=utf-8","Cache-Control":"no-store"});res.end(b);
   }catch(e){events.push({kind:"server-error",error:String(e)});res.writeHead(500);res.end();}
  });
  await new Promise((resolve,reject)=>{server.once("error",reject);server.listen({host:"127.0.0.1",port:8766,exclusive:true},resolve);});
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
    const home=async()=>{await page.goto(origin,{waitUntil:"load"});await page.waitForFunction(()=>typeof allQuestions!=="undefined"&&allQuestions.length>0&&document.querySelector("#examDateWrittenV1Form")&&document.querySelector("#mobileBottomNavV227"));};
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
    if(cfg.mode==="acceptance")await runFunctionalW02({page,home,snap,profile,result,need});
   }finally{await ctx.close();}
  }
  exact();result.postGuard=guard("post-guard");need(JSON.stringify(result.preGuard)===JSON.stringify(result.postGuard),"exact unchanged guard snapshots");
  need(result.pageErrors.length===0,"no unhandled browser errors");
  result.state=cfg.mode==="inventory"?"W02_UI_INVENTORY_COMPLETE_ACCEPTANCE_PENDING":"W02_FUNCTIONAL_CASES_COMPLETE_FULL_ACCEPTANCE_PENDING";
 }catch(e){failure=e;result.state=cfg.mode==="inventory"?"W02_UI_INVENTORY_FAILED":"W02_FUNCTIONAL_CASE_FAILURE";result.error=String(e);result.stack=e.stack;}
 finally{
  if(browser)await browser.close();if(server)await new Promise(resolve=>server.close(resolve));
  result.endedUtc=utc();save("events.json",events);save("result.json",result);console.log(JSON.stringify({state:result.state,snapshots:result.snapshots.length,error:result.error||null,fullProductAcceptance:false,output:out}));
 }
 if(failure)throw failure;
}
main().catch(e=>{console.error(e.stack);process.exitCode=1;});

async function runFunctionalW02({page,home,snap,profile,result,need}){
 result.cases ||= [];
 const check=async(id,fn)=>{
  const row={id:profile.id+":"+id,startedUtc:new Date().toISOString(),status:"RUNNING"};result.cases.push(row);
  try{row.evidence=await fn();row.status="PASS";}catch(e){row.status="FAIL";row.error=String(e);try{await snap("failure-"+id);}catch(captureError){row.captureError=String(captureError);}throw e;}finally{row.endedUtc=new Date().toISOString();}
 };
 const storage=()=>page.evaluate(()=>Object.fromEntries(Object.keys(localStorage).sort().map(k=>[k,localStorage.getItem(k)])));
 const mobileMenu=async target=>{
  if(profile.isMobile){
   if(["oral","stats"].includes(target)){await page.locator('[data-mobile-target="more"]').click();await page.locator('#mobileMoreSheetV227 button[onclick="navigateMobileV227(\''+target+'\')"]').click();}
   else await page.locator('[data-mobile-target="'+target+'"]').click();
  }else if(target==="flashcards")await page.locator("#flashcardsMenu").click();
  else if(target==="stats")await page.locator("#statsMenu").click();
  else if(target==="oral")await page.locator(".menu-item").filter({hasText:"Mündliche Prüfung"}).click();
 };
 await home();
 await check("dates-save-independent-and-reload",async()=>{
  await page.locator("#examDateWrittenV1Input").fill("2030-01-15");await page.locator("#examDateWrittenV1Save").click();
  await page.locator("#examDateOralV1Input").fill("2030-02-16");await page.locator("#examDateOralV1Save").click();
  await home();const s=await storage();
  need(s.accaoui_exam_date_written_v1==="2030-01-15"&&s.accaoui_exam_date_oral_v1==="2030-02-16","two independent dates persisted");
  return {written:s.accaoui_exam_date_written_v1,oral:s.accaoui_exam_date_oral_v1};
 });
 await check("date-delete-preserves-other-date",async()=>{
  await page.locator("#examDateWrittenV1Delete").click();await home();const s=await storage();
  need(s.accaoui_exam_date_written_v1===undefined&&s.accaoui_exam_date_oral_v1==="2030-02-16","delete only requested date");return {written:s.accaoui_exam_date_written_v1||null,oral:s.accaoui_exam_date_oral_v1};
 });
 await check("date-quota-error-preserves-storage",async()=>{
  const before=await storage();
  await page.evaluate(()=>{Storage.prototype.setItem=function(){throw new DOMException("synthetic W02 quota fault","QuotaExceededError");};});
  await page.locator("#examDateWrittenV1Input").fill("2030-03-17");await page.locator("#examDateWrittenV1Save").click();
  const after=await storage(),error=await page.locator("#examDateWrittenV1Error").innerText();
  need(JSON.stringify(before)===JSON.stringify(after)&&error.trim().length>0,"quota fault preserves prior storage and reports error");await home();return {storageUnchanged:true,error};
 });
 await check("learning-keyboard-answer-score-and-autosave",async()=>{
  await page.locator("#openQuestionsCard").click();await page.locator("#questionArea .answer-btn").first().waitFor({state:"visible"});
  const q=await page.evaluate(()=>({id:currentQuestions[currentQuestionIndex].id,correct:[...currentQuestions[currentQuestionIndex].correct],total:currentQuestions.length}));
  for(const i of q.correct){const b=page.locator('#questionArea .answer-btn[data-index="'+i+'"]');await b.focus();await page.keyboard.press("Enter");}
  const actual=await page.evaluate(()=>({awaiting:learningQuestionAwaitingNext,correct:correctAnswersCount,wrong:wrongAnswersCount,saved:JSON.parse(localStorage.getItem("accaoui_active_learning_session"))}));
  need(actual.awaiting&&actual.correct===1&&actual.wrong===0&&actual.saved,"keyboard grading and persisted review");
  await snap("learning-keyboard-reviewed");return {questionId:q.id,total:q.total,correct:actual.correct,wrong:actual.wrong};
 });
 await check("learning-pause-reload-resume-review",async()=>{
  const before=await page.evaluate(()=>({id:currentQuestions[currentQuestionIndex].id,selected:[...selectedAnswers],right:correctAnswersCount,wrong:wrongAnswersCount}));
  await page.locator('button[onclick="pauseLearningSession()"]').click();await home();
  await page.locator('button[onclick="resumeActiveLearningSession()"]:visible').first().click();
  const after=await page.evaluate(()=>({id:currentQuestions[currentQuestionIndex].id,selected:[...selectedAnswers],right:correctAnswersCount,wrong:wrongAnswersCount,awaiting:learningQuestionAwaitingNext}));
  need(after.id===before.id&&after.right===before.right&&after.wrong===before.wrong&&after.awaiting,"resume preserves question, counts and answer review");return {before,after};
 });
 await home();
 await check("category-route-preserves-written-learning-mode",async()=>{
  await page.locator("#allQuestionsCard").click();await page.locator('.category-card[onclick^="openCategory"]').first().click();
  const x=await page.evaluate(()=>({mode:currentMode,total:currentQuestions.length,categories:[...new Set(currentQuestions.map(q=>q.category))]}));
  need(x.mode==="category"&&x.total>0&&x.categories.length===1,"actual category route");return x;
 });
 await home();
 await check("flashcard-reveal-and-rating",async()=>{
  await mobileMenu("flashcards");await page.locator('button[onclick^="startFlashcardSession(allQuestions"]').click();
  await page.locator("#showFlashcardAnswerBtn").click();
  need(await page.locator("#flashcardRating").isVisible(),"card rating visible after reveal");
  await page.locator('button[onclick="markFlashcardUnknown()"]').click();
  const x=await page.evaluate(()=>({mode:currentMode,index:flashcardIndex,progress:JSON.parse(localStorage.getItem("accaoui_flashcard_progress")),session:JSON.parse(localStorage.getItem("accaoui_active_flashcard_session"))}));
  need(x.mode==="flashcards"&&x.index===1&&x.progress&&x.session,"unknown card persisted and next card displayed");await snap("flashcard-rated");return {mode:x.mode,index:x.index,progressKeys:Object.keys(x.progress)};
 });
 await check("flashcard-pause-reload-resume",async()=>{
  const index=await page.evaluate(()=>flashcardIndex);await page.locator('button[onclick="pauseFlashcardSession()"]').click();await home();
  await page.locator('button[onclick="resumeActiveFlashcardSession()"]:visible').first().click();
  const resumed=await page.evaluate(()=>flashcardIndex);need(resumed===index,"same flashcard index after reload");return {index,resumed};
 });
 await home();
 await check("oral-practice-reveal-and-separate-rating",async()=>{
  const before=await storage();await mobileMenu("oral");await page.locator(".oral-topic-card").first().click();
  const count=await page.evaluate(()=>oralExamQuestionsV220.length);need(count===2,"first actual oral topic has two practice questions");
  for(let i=0;i<count;i++){
   await page.locator('.oral-room-controls-v226 button[onclick="showOralExamAnswerV220()"]:visible').click();await page.locator(".oral-room-qa-bubble-v225.is-answer-visible .oral-room-answer-view-v225").waitFor({state:"visible"});
   await page.locator('.oral-room-controls-v226 button[onclick="rateOralExamQuestionV220(\''+(i===0?"practice":"known")+'\')"]:visible').click();
  }
  const after=await storage();need(after.accaoui_flashcard_progress===before.accaoui_flashcard_progress&&after.accaoui_active_learning_session===before.accaoui_active_learning_session,"oral rating does not overwrite card or written learning state");
  await snap("oral-practice-finished");return {questions:count,newOrChangedKeys:Object.keys(after).filter(k=>after[k]!==before[k])};
 });
 await check("oral-mistake-reveal-collapse-resolve-last",async()=>{
  await page.locator('button[onclick*="showOralMistakeTraining"]:visible').first().click();
  const cards=page.locator("[data-oral-mistake-key-v2340]");need(await cards.count()===1,"one oral mistake from practice rating");
  await page.locator('[data-oral-action-v2340="reveal"]').click();
  need(await page.locator('[data-oral-action-v2340="resolve"]').isVisible(),"oral error revealed");
  await page.locator('[data-oral-action-v2340="collapse"]').click();
  need(await page.locator('[data-oral-action-v2340="reveal"]').isVisible(),"still practice collapses without removal");
  await page.locator('[data-oral-action-v2340="reveal"]').click();await page.locator('[data-oral-action-v2340="resolve"]').click();
  need(await cards.count()===0&&(await page.locator("main").innerText()).includes("Keine offenen mündlichen Fehler"),"last oral error clears and real empty state renders");
  await snap("oral-mistake-empty");return {remainingCards:0};
 });
 await home();
 await check("oral-sheet-A-manual-all-known-blocks",async()=>{
  await mobileMenu("oral");await page.locator('button[onclick="showOralExamModeSelectV2314()"]:visible').click();
  await page.locator('button[onclick="startOralSimulation15V2314()"]:visible').click();
  need(await page.evaluate(()=>oralExamQuestionsV220.length)===15,"actual sheet A contains fifteen questions");
  for(let i=0;i<15;i++){
   await page.waitForFunction(i=>oralExamIndexV220===i,i);
   await page.locator('.oral-room-controls-v226 button[onclick="showOralExamAnswerV220()"]:visible').click();
   await page.locator(".oral-room-qa-bubble-v225.is-answer-visible .oral-room-answer-view-v225").waitFor({state:"visible"});
   await page.locator('.oral-room-controls-v226 button[onclick="rateOralExamQuestionV220(\'known\')"]:visible').click();
  }
  const blocks=await page.evaluate(()=>getOralBlockResultStatsV2321());
  need(blocks.length===3&&blocks.every(b=>b.total===5&&b.known===5&&b.practice===0&&b.open===0),"fifteen manual ratings, three independent five-question blocks");
  await snap("oral-sheet-A-manual-complete");return {blocks,completion:"MANUAL_FUNCTIONAL_NO_TIMER_PATCH"};
 });

 await home();
 let activeAttempt=null,terminalHistory=null;
 await check("written-full-manual-flow-start-no-clock-patch",async()=>{
  await page.locator("#examCard").click();await page.locator('[onclick*="startExamMode"][onclick*="\'full\'"]').click();
  activeAttempt=await page.evaluate(()=>JSON.parse(localStorage.getItem("accaoui_active_session")));
  need(activeAttempt.questions.length===82&&activeAttempt.secondsLeft>7180&&activeAttempt.attemptStatus==="active","ordinary W02 full exam manual user-flow starts with original duration and identity");
  const used=new Set(),pick=f=>{const i=activeAttempt.questions.findIndex((q,i)=>!used.has(i)&&f(q));need(i>=0,"actual grading type exists");used.add(i);return i;};
  const one=pick(q=>Number(q.points)===1),two=pick(q=>Number(q.points)===2&&q.correct.length>=2),partial=pick(q=>Number(q.points)===2&&q.correct.length>=2),wrong=pick(q=>q.answers.some((_,i)=>!q.correct.includes(i)));
  const plan=[{index:one,answers:activeAttempt.questions[one].correct,points:1},{index:two,answers:activeAttempt.questions[two].correct,points:2},{index:partial,answers:[activeAttempt.questions[partial].correct[0]],points:1},{index:wrong,answers:[activeAttempt.questions[wrong].answers.findIndex((_,i)=>!activeAttempt.questions[wrong].correct.includes(i))],points:0}];
  await page.locator("#examNavToggle").click();
  for(const c of plan){await page.locator("#examNav .exam-nav-btn").nth(c.index).click();for(const a of c.answers)await page.locator('#examQuestionArea .answer-btn[data-index="'+a+'"]').click();}
  const stored=await page.evaluate(()=>JSON.parse(localStorage.getItem("accaoui_active_session")));
  need(plan.every(c=>JSON.stringify([...(stored.answers[c.index]||[])].sort())===JSON.stringify([...c.answers].sort())),"four UI answer patterns autosaved");
  result.writtenUserFlowStarts=(result.writtenUserFlowStarts||0)+1;
  return {attemptId:activeAttempt.attemptId,total:82,answerPatterns:plan,originalSeconds:activeAttempt.secondsLeft,manualFinishPlanned:true,naturalProof:false};
 });
 await check("written-pause-reload-resume-identity-and-answers",async()=>{
  const saved=await page.evaluate(()=>JSON.parse(localStorage.getItem("accaoui_active_session")));await page.locator('button[onclick="pauseExam()"]').click();await home();
  await page.locator('button[onclick="resumeActiveExamSession()"]:visible').first().click();
  const after=await page.evaluate(()=>JSON.parse(localStorage.getItem("accaoui_active_session")));
  need(after.attemptId===saved.attemptId&&JSON.stringify(after.answers)===JSON.stringify(saved.answers)&&after.secondsLeft<=saved.secondsLeft&&after.secondsLeft>saved.secondsLeft-10,"written identity, answers and natural elapsed seconds on resume");
  return {sameIdentity:true,answerCount:Object.keys(after.answers).length,secondsLeft:after.secondsLeft};
 });
 await check("written-unanswered-warning-preserves-answers",async()=>{
  const before=await page.evaluate(()=>JSON.stringify(examAnswers));await page.locator("#finishExamNowBtn").click();
  need(await page.locator("#examWarningBox").isVisible(),"real unanswered warning rendered");
  const after=await page.evaluate(()=>JSON.stringify(examAnswers));need(before===after,"warning does not mutate answers");return {answersUnchanged:true,warning:await page.locator("#examWarningBox").innerText()};
 });
 await check("written-manual-confirmation-grades-once",async()=>{
  await page.locator('#examWarningBox button[onclick="finishExamMode()"]').focus();await page.keyboard.press("Enter");
  await page.locator(".result-wrapper .result-hero").waitFor({state:"visible"});
  terminalHistory=await page.evaluate(()=>JSON.parse(localStorage.getItem("accaoui_exam_history")));
  const row=terminalHistory.find(x=>x.attemptId===activeAttempt.attemptId);
  need(terminalHistory.length===1&&row.total===82&&row.points.max===120&&row.points.reached===4&&row.correct===2&&row.wrong===2&&row.unanswered===78,"independent mixed full/partial/wrong/open score and one history");
  await snap("written-manual-result");return {attemptId:row.attemptId,points:row.points,correct:row.correct,wrong:row.wrong,unanswered:row.unanswered,completion:"MANUAL_FUNCTIONAL_NOT_NATURAL_TIMEOUT"};
 });
 await check("written-mistake-training-and-real-partial-result",async()=>{
  const before=await storage();await page.locator('button[onclick="startMistakeTraining()"]:visible').click();
  const x=await page.evaluate(()=>({mode:currentMode,total:currentQuestions.length,correct:[...currentQuestions[currentQuestionIndex].correct]}));
  need(x.mode==="last-exam-mistakes"&&x.total===80,"written wrong/partial/open questions reach distinct eighty-question training");
  for(const a of x.correct)await page.locator('#questionArea .answer-btn[data-index="'+a+'"]').click();
  await page.locator('button[onclick="showLearningPartialResultV2311()"]:visible').click();
  const values=await page.locator(".learning-partial-grid-v2311 strong").allTextContents();
  need(JSON.stringify(values.map(x=>x.trim()))===JSON.stringify(["1/80","1","0","79"]),"actual partial-result DOM shows one correct and seventy-nine open");
  const after=await storage();need(after.accaoui_exam_history===before.accaoui_exam_history&&after.accaoui_oral_exam_mistakes_v2324===before.accaoui_oral_exam_mistakes_v2324,"written training does not append history or modify oral mistakes");
  await snap("written-mistake-partial-result");return {mode:x.mode,trainingQuestions:x.total,values,oralStoreUnchanged:true,writtenHistoryUnchanged:true};
 });

 await check("written-reload-history-no-false-resume",async()=>{
  await home();const after=await page.evaluate(()=>({history:JSON.parse(localStorage.getItem("accaoui_exam_history")),resume:[...document.querySelectorAll('button[onclick="resumeActiveExamSession()"]')].some(e=>e.getClientRects().length)}));
  need(JSON.stringify(after.history)===JSON.stringify(terminalHistory)&&!after.resume,"one terminal history preserved and no active resume");return {historyCount:after.history.length,resume:false};
 });
 await check("statistics-actual-ui-after-synthetic-result",async()=>{
  await mobileMenu("stats");const text=await page.locator("main").innerText();
  need(text.includes("Prüfungsentwicklung")&&text.includes("Prüfungsverlauf"),"actual statistics route after synthetic written completion");await snap("statistics-after-result");return {historyCount:terminalHistory.length};
 });
 await home();
 await check("corrupt-written-storage-rejected-without-deletion",async()=>{
  await page.evaluate(()=>localStorage.setItem("accaoui_active_session","{synthetic-invalid-json"));
  await home();await page.locator("#examCard").click();await page.locator('[onclick*="startExamMode"][onclick*="\'full\'"]').click();
  const s=await storage();need(s.accaoui_active_session==="{synthetic-invalid-json"&&JSON.stringify(JSON.parse(s.accaoui_exam_history))===JSON.stringify(terminalHistory)&&!(await page.locator("#examQuestionArea").count()),"invalid active storage is retained, history unchanged, no successful new exam");
  return {injected:"synthetic-invalid-json",preserved:true,noNewAttempt:true};
 });
 await check("layout-width-and-native-button-focus",async()=>{
  await home();const x=await page.evaluate(()=>({width:innerWidth,documentWidth:document.documentElement.scrollWidth}));
  need(x.documentWidth<=x.width+1,"dashboard has no horizontal viewport overflow");
  await page.locator("#examDateWrittenV1Input").focus();
  let focus;
  for(let i=0;i<8;i++){await page.keyboard.press("Tab");focus=await page.evaluate(()=>({tag:document.activeElement.tagName,id:document.activeElement.id}));if(focus.id==="examDateWrittenV1Save")break;}
  need(focus.tag==="BUTTON"&&focus.id==="examDateWrittenV1Save","native keyboard tab reaches date submit");return {viewport:x,focus,physicalDevice:false};
 });
}
