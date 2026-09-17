#!/usr/bin/env python3
"""v27.37g: actual written-exam lifecycle, storage and semantic mutation tests.

Node VM contexts use synthetic questions, memory-only storage and a small DOM.
No browser profile, repository temporary file, network or real learning data.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
from pathlib import Path
import runpy
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]

HARNESS = r'''
"use strict";
const assert = require("node:assert/strict");
const vm = require("node:vm");
const fs = require("node:fs");
const source = fs.readFileSync(0,"utf8");
const K = {session:"accaoui_active_session", history:"accaoui_exam_history",
  stats:"accaoui_topic_stats", mistakes:"accaoui_topic_mistakes", answered:"accaoui_answered_questions"};
const fixtures = [
  {id:"one",category:"Bürgerliches Gesetzbuch",question:"Test A",answers:["Ja","Nein"],correct:[0],points:1},
  {id:"two",category:"Bürgerliches Gesetzbuch",question:"Test B",answers:["A","B","C"],correct:[0,1],points:2},
  {id:"three",category:"Bürgerliches Gesetzbuch",question:"Test C",answers:["Ja","Nein"],correct:[0],points:1}
];
let nextUuid = 1;
function fixture(store = new Map()) {
  const stats = {effects:{}, notices:[], logs:[], writes:[], views:0, training:null};
  const options = {readFail:null, writeFail:null, readHook:null, writeHook:null};
  const elements = new Map(), timeouts = new Map(), intervals = new Map(), queued = [];
  const events = {window:{},document:{}};
  let timerId = 0;
  class Element {
    constructor(tag) {this.tag=tag;this.children=[];this.innerHTML="";this.textContent="";this.listeners={};this.classList={add(){},remove(){}};}
    appendChild(child){this.children.push(child);child.parentNode=this;if(child.id)elements.set(child.id,child);return child;}
    insertBefore(child){return this.appendChild(child);}
    setAttribute(name,value){this[name]=value;}
    addEventListener(name,callback){this.listeners[name]=callback;}
    remove(){elements.delete(this.id);if(this.parentNode)this.parentNode.children=this.parentNode.children.filter(c=>c!==this);}
    showModal(){this.open=true;}
    close(){this.open=false;}
  }
  const main = new Element("main"), body = new Element("body"), hero = new Element("section");
  main.appendChild(hero);
  const document = {body,visibilityState:"visible",
    addEventListener(name,callback){(events.document[name] ||= []).push(callback);},
    getElementById(id){return elements.get(id)||null;},
    querySelector(selector){return selector === ".main-content" ? main : selector === ".hero-grid" ? hero : null;},
    querySelectorAll(){return [];},createElement(tag){return new Element(tag);}};
  const storage = {
    getItem(key){
      if(options.readFail===key)throw Error("PRIVATE_STORAGE_ERROR");
      const raw=store.get(key)??null;
      if(options.readHook){const hook=options.readHook;if(hook.key===key){options.readHook=null;hook.run();}}
      return raw;
    },
    setItem(key,value){
      if(options.writeFail===key)throw Error("PRIVATE_STORAGE_ERROR");
      stats.writes.push(key);store.set(key,value);
      if(options.writeHook){const hook=options.writeHook;options.writeHook=null;hook();}
    },removeItem(){throw Error("Unexpected storage deletion");}
  };
  const win={addEventListener(name,callback){(events.window[name] ||= []).push(callback);}};
  const math=Object.create(Math);math.random=()=>0.5;
  const context=vm.createContext({window:win,document,localStorage:storage,Math:math,
    crypto:{randomUUID(){return "11111111-1111-4111-8111-"+String(nextUuid++).padStart(12,"0");}},
    console:Object.fromEntries(["log","warn","error","info"].map(n=>[n,(...a)=>stats.logs.push(a.join(" "))])),
    alert(message){stats.notices.push(message);},location:{reload(){}},
    setTimeout(fn){const id=++timerId;timeouts.set(id,fn);queued.push(fn);return id;},clearTimeout(id){timeouts.delete(id);},
    setInterval(fn){const id=++timerId;intervals.set(id,fn);return id;},clearInterval(id){intervals.delete(id);},
    fetch(){throw Error("Network forbidden in fixture");},
    __notice(message){stats.notices.push(message);},__view(){stats.views++;},
    __effect(name){stats.effects[name]=(stats.effects[name]||0)+1;},
    __training(questions){stats.training=JSON.parse(JSON.stringify(questions));}
  });
  const run=code=>vm.runInContext(code,context,{timeout:4000});
  run(source);
  run(`
    allQuestions=${JSON.stringify(fixtures)};
    showSmallNotice=message=>__notice(message);
    showExamView=()=>__view(); renderExamQuestion=()=>{};
    updateDashboardNumbers=()=>{}; showAutoSaveIndicator=()=>{};
    startLearningSession=questions=>__training(questions);
    for(const name of ["saveTopicResult","markQuestionAsAnswered","saveTopicMistake","removeTopicMistake"]){
      const original=globalThis[name];globalThis[name]=function(...args){__effect(name);return original(...args);};
    }
    registerActiveSessionAutoSaveListeners();
  `);
  const json=expression=>JSON.parse(run("JSON.stringify("+expression+")"));
  const stored=key=>store.has(key)?JSON.parse(store.get(key)):null;
  const start=()=>run('startExamMode(3,"Testprüfung","short")');
  const answer=expression=>run('examAnswers='+expression+'; saveActiveExamSession()');
  const finish=()=>run('finishExamMode()');
  const leave=()=>{
    for(const name of ["pagehide","beforeunload"])for(const callback of events.window[name]||[])callback();
    document.visibilityState="hidden";for(const callback of events.document.visibilitychange||[])callback();
    document.visibilityState="visible";for(const callback of events.document.visibilitychange||[])callback();
    for(const callback of queued.slice())callback();
  };
  return {run,json,store,stored,start,answer,finish,leave,stats,options,main,elements,intervals,queued,
    decide(label){const dialog=elements.get("writtenExamLegacyDialogV2737G");assert.ok(dialog,"legacy dialog missing");
      const button=dialog.children.flatMap(child=>child.children).find(c=>c.textContent===label);assert.ok(button);button.listeners.click();}};
}
let checks=0;
function test(name,body){body();checks++;console.log("PASS "+name);}
function snapshot(f){return JSON.stringify([...f.store]);}
function closed(f){
  assert.equal(f.run("getActiveSession()"),null);
  assert.equal(f.run("resumeActiveExamSession()"),false);
  assert.equal(f.run("hasActiveExamSession()"),false);
  assert.equal(f.json("getDashboardSessionCandidatesV2735B()").filter(c=>c.type==="exam").length,0);
  f.run("renderDashboardResumeExamCard()");assert.equal(f.elements.has("examResumeCard"),false);
}
test("partial answers, score, topic analysis, review and unanswered error training",()=>{
  const f=fixture();f.start();f.answer('{0:[0],1:[0]}');f.finish();
  const result=f.stored(K.history)[0];
  assert.deepEqual([result.total,result.correct,result.wrong,result.unanswered],[3,1,1,1]);
  assert.deepEqual(result.points,{reached:2,max:4,pass:2,passPercent:50});assert.equal(result.passed,true);
  assert.deepEqual(result.topicBreakdown["Bürgerliches Gesetzbuch"],{total:3,correct:1,wrong:1,unanswered:1,percent:33});
  assert.match(f.main.innerHTML,/Bestanden/);assert.match(f.main.innerHTML,/2\/4/);
  assert.deepEqual(f.json("lastExamMistakes.map(q=>q.id)"),["two","three"]);
  f.run("startMistakeTraining()");assert.deepEqual(f.stats.training.map(q=>q.id),["two","three"]);
  assert.equal(f.stats.effects.saveTopicResult,2);assert.equal(f.stats.effects.markQuestionAsAnswered,2);
  assert.equal(f.stats.effects.saveTopicMistake,2);assert.equal(f.stats.effects.removeTopicMistake,1);
  assert.equal(f.stored(K.stats)["Bürgerliches Gesetzbuch"].answered,2);
  assert.deepEqual(f.stored(K.mistakes)["Bürgerliches Gesetzbuch"].map(q=>q.id),["two","three"]);
});
for(const [name,answers,expected] of [
  ["empty","{}",[0,0,3,0,false]],
  ["all correct","{0:[0],1:[0,1],2:[0]}",[3,0,0,4,true]],
  ["all wrong","{0:[1],1:[2],2:[1]}",[0,3,0,0,false]],
  ["below pass boundary","{0:[0]}",[1,0,2,1,false]]]){
  test(name,()=>{const f=fixture();f.start();f.answer(answers);f.finish();const r=f.stored(K.history)[0];
    assert.deepEqual([r.correct,r.wrong,r.unanswered,r.points.reached,r.passed],expected);});
}
test("full 82-question route retains 120-minute exam and scoring",()=>{
  const f=fixture();f.run('allQuestions=EXAM_CORE_QUESTION_IDS_V244.map(id=>({...allQuestions[0],id}));startExamMode(82,"Vollsimulation","full")');
  assert.equal(f.json("examQuestions.length"),82);assert.equal(f.json("examSecondsLeft"),7200);assert.equal(f.intervals.size,1);
  f.answer('{0:[0]}');f.finish();assert.equal(f.stored(K.history)[0].total,82);assert.equal(f.intervals.size,0);
});
test("terminal persistence, repeat completion, stale autosave and reload/dashboard",()=>{
  const f=fixture();f.start();f.answer('{0:[0]}');f.run("scheduleExamSessionTimerSave()");f.finish();
  const id=f.stored(K.session).attemptId;assert.equal(f.stored(K.session).attemptStatus,"completed");
  assert.equal(f.stored(K.history)[0].attemptId,id);
  const before=snapshot(f),effects=JSON.stringify(f.stats.effects);
  f.finish();f.finish();f.leave();assert.equal(snapshot(f),before);assert.equal(JSON.stringify(f.stats.effects),effects);
  // Even a stale caller's exam mode cannot turn a terminal attempt back into active storage.
  f.run('currentMode="exam";saveActiveExamSession()');assert.equal(snapshot(f),before);
  closed(f);assert.equal(snapshot(f),before);
  const reload=fixture(f.store);closed(reload);reload.finish();reload.leave();assert.equal(snapshot(reload),before);
});
test("synchronous reentrant completion before training writes",()=>{
  const f=fixture();f.start();f.answer('{0:[0],1:[0,1]}');
  f.options.readHook={key:K.stats,run:()=>f.finish()};f.finish();
  assert.equal(f.stats.effects.saveTopicResult,2);assert.equal(f.stored(K.history).length,1);
  assert.equal(f.json("writtenExamAttemptV2737G.status"),"completed");
});
test("timer expiry followed by click counts once",()=>{
  const f=fixture();f.start();f.run('examSecondsLeft=1;startExamTimer()');
  [...f.intervals.values()][0]();f.finish();f.leave();assert.equal(f.stored(K.history).length,1);closed(f);
});
test("new identical attempts get different ids and both count",()=>{
  const f=fixture();f.start();f.answer('{0:[0]}');const id=f.stored(K.session).attemptId;f.finish();
  f.start();assert.notEqual(f.stored(K.session).attemptId,id);assert.equal(f.stored(K.session).attemptStatus,"active");
  f.answer('{0:[0]}');f.finish();const h=f.stored(K.history);assert.equal(h.length,2);assert.notEqual(h[0].attemptId,h[1].attemptId);
  assert.equal(h[0].percent,h[1].percent);assert.equal(f.stored(K.stats)["Bürgerliches Gesetzbuch"].answered,2);
});
test("pause, autosave and fresh-context resume preserve identity and learning state",()=>{
  const f=fixture();f.start();f.run('examQuestionIndex=1;examSecondsLeft=321;examFocusQuestionIndexes=[1,2];examFocusQuestionPosition=1');
  f.answer('{0:[0],1:[0]}');f.run("pauseExam()");f.leave();const session=f.stored(K.session);
  const r=fixture(f.store);assert.equal(r.run("resumeActiveExamSession()"),true);
  assert.deepEqual(r.json("[examQuestions,examQuestionIndex,examAnswers,examSecondsLeft,examFocusQuestionIndexes,examFocusQuestionPosition]"),
    [session.questions,1,session.answers,321,[1,2],1]);
  r.run("saveActiveExamSession()");assert.equal(r.stored(K.session).attemptId,session.attemptId);
});
test("fresh persisted history is authoritative, old duplicates and foreign storage survive",()=>{
  const f=fixture();f.start();const id=f.stored(K.session).attemptId;
  const old=[{date:"old",percent:50},{date:"old",percent:50}];
  f.store.set(K.history,JSON.stringify(old));f.store.set("accaoui_active_learning_session",JSON.stringify({note:"retained"}));
  f.store.set("unrelated", "untouched");f.finish();assert.deepEqual(f.stored(K.history).slice(0,2),old);
  const before=snapshot(f);f.run('saveExamResult({attemptId:'+JSON.stringify(id)+'})');assert.equal(snapshot(f),before);
  assert.equal(f.store.get("unrelated"),"untouched");assert.deepEqual(f.stored("accaoui_active_learning_session"),{note:"retained"});
});
test("history with exact attempt id blocks active snapshot without deletion or training",()=>{
  const f=fixture();f.start();f.store.set(K.history,JSON.stringify([{attemptId:f.stored(K.session).attemptId,percent:25}]));
  const before=snapshot(f);closed(f);f.finish();assert.equal(snapshot(f),before);assert.deepEqual(f.stats.effects,{});
});
function legacy(){const f=fixture();f.start();f.answer('{0:[0],1:[0,1],2:[0]}');const s=f.stored(K.session);
  delete s.attemptId;delete s.attemptStatus;delete s.attemptVersion;s.currentIndex=2;s.secondsLeft=0;
  const store=new Map([[K.session,JSON.stringify(s)],[K.history,JSON.stringify([{percent:100},{percent:100}])]]);
  return {f:fixture(store),s};}
for(const decision of ["Abbrechen","Bereits abgegeben","Noch nicht abgegeben"]){
  test("legacy explicit decision: "+decision,()=>{
    const {f,s}=legacy(),before=snapshot(f),history=f.store.get(K.history);
    const candidate=f.json("getDashboardSessionCandidatesV2735B()")[0];
    assert.equal(f.json("buildDashboardResumeStepV2735B("+JSON.stringify(candidate)+")").title,"Zu prüfende gespeicherte Prüfung");
    f.run("renderDashboardResumeExamCard()");assert.match(f.elements.get("examResumeCard").innerHTML,/Zu prüfende gespeicherte Prüfung/);
    assert.equal(f.run("resumeActiveExamSession()"),false);assert.equal(f.stats.views,0);assert.equal(snapshot(f),before);
    f.decide(decision);assert.equal(f.store.get(K.history),history);
    if(decision==="Abbrechen"){assert.equal(snapshot(f),before);assert.equal(f.stats.views,0);}
    else{const result=f.stored(K.session);for(const [key,value] of Object.entries(s))assert.deepEqual(result[key],value);
      assert.ok(result.attemptId);assert.equal(result.attemptStatus,decision==="Bereits abgegeben"?"completed":"active");
      if(decision==="Bereits abgegeben"){closed(f);assert.equal(f.stats.views,0);}
      else {assert.equal(f.stats.views,1);f.run("saveActiveExamSession()");assert.equal(f.stored(K.session).attemptId,result.attemptId);}}
    assert.deepEqual(f.stats.effects,{});
  });
}
test("legacy dialog refuses changed storage",()=>{
  const {f}=legacy();f.run("resumeActiveExamSession()");f.store.set(K.session,"broken");const before=snapshot(f);
  f.decide("Noch nicht abgegeben");assert.equal(snapshot(f),before);assert.equal(f.stats.views,0);assert.ok(f.stats.notices.length);
});
for(const [name,alter] of [
  ["bad JSON",f=>f.store.set(K.session,"{")],
  ["missing id",f=>{const s=f.stored(K.session);delete s.attemptId;f.store.set(K.session,JSON.stringify(s));}],
  ["bad id",f=>{const s=f.stored(K.session);s.attemptId="bad";f.store.set(K.session,JSON.stringify(s));}],
  ["unknown status",f=>{const s=f.stored(K.session);s.attemptStatus="unknown";f.store.set(K.session,JSON.stringify(s));}],
  ["invalid answers",f=>{const s=f.stored(K.session);s.answers={0:[99]};f.store.set(K.session,JSON.stringify(s));}],
  ["invalid history",f=>f.store.set(K.history,"{}")],
  ["read throw",f=>f.options.readFail=K.session]]){
  test("fail closed without storage loss: "+name,()=>{
    const f=fixture();f.start();alter(f);const before=snapshot(f);assert.equal(f.run("resumeActiveExamSession()"),false);
    f.finish();f.start();assert.equal(snapshot(f),before);assert.deepEqual(f.stats.effects,{});
    assert.ok(f.stats.notices.length);assert.ok(!f.stats.notices.join(" ").includes("PRIVATE_STORAGE_ERROR"));
    assert.ok(!f.main.innerHTML.includes("Prüfungsergebnis"));
  });
}
for(const key of [K.history,K.stats,K.mistakes,K.answered]){
  test("corrupt completion store retained: "+key,()=>{
    const f=fixture();f.start();f.store.set(key,"{");const before=snapshot(f);f.finish();f.finish();
    assert.equal(snapshot(f),before);assert.deepEqual(f.stats.effects,{});assert.ok(f.stats.notices.length);
  });
}
for(const key of [K.session,K.stats,K.mistakes,K.answered,K.history]){
  test("write error is not success or replay: "+key,()=>{
    const f=fixture();f.start();f.answer('{0:[0]}');f.options.writeFail=key;f.finish();const before=snapshot(f);
    const effects=JSON.stringify(f.stats.effects);f.finish();f.leave();assert.equal(snapshot(f),before);
    assert.equal(JSON.stringify(f.stats.effects),effects);assert.ok(f.stats.notices.length);
    assert.ok(!f.main.innerHTML.includes("Prüfungsergebnis"));assert.ok(!f.stats.notices.join(" ").includes("PRIVATE_STORAGE_ERROR"));
    if(key!==K.session)closed(fixture(f.store));
  });
}
test("initial persistence error does not expose a successful new attempt",()=>{
  const f=fixture();f.options.writeFail=K.session;f.start();assert.equal(f.stats.views,0);assert.equal(f.store.size,0);
  assert.ok(f.stats.notices.length);f.finish();assert.equal(f.store.size,0);
});
console.log("BEHAVIOR PASS: "+checks+" scenarios; actual app functions, synthetic storage only");
'''

def mutations(source):
    def once(old, new):
        assert source.count(old) == 1, "Mutation anchor not unique: " + old[:60]
        return source.replace(old, new, 1)
    start = source.index("function saveActiveExamSession() {")
    end = source.index("function scheduleExamSessionTimerSave() {", start)
    yield "terminal autosave protection", source[:start] + '''function saveActiveExamSession() {
  if (currentMode !== "exam" || !writtenExamAttemptV2737G) return false;
  saveActiveSession(writtenExamSnapshotV2737G("active"));
  return true;
}

''' + source[end:]
    yield "synchronous completion guard", once(
        '  if (!writtenExamAttemptV2737G || writtenExamAttemptV2737G.status !== "active" || currentMode !== "exam") return;',
        '  if (!writtenExamAttemptV2737G) return;')
    start = source.index("function saveExamResult(result) {")
    end = source.index("function showStatsPage() {", start)
    yield "unconditional history append", source[:start] + '''function saveExamResult(result) {
  const history = writtenExamHistoryV2737G();
  history.push(result);
  writeStorage(STORAGE_KEYS.examHistory, history);
  examHistory = history;
  return true;
}

''' + source[end:]
    yield "new identity on resume", once(
        'writtenExamAttemptV2737G = {id: session.attemptId, status: "active", createdAt: session.createdAt};',
        'writtenExamAttemptV2737G = {id: writtenExamNewIdV2737G(session, writtenExamHistoryV2737G()), status: "active", createdAt: session.createdAt}; saveActiveSession({...session, attemptId: writtenExamAttemptV2737G.id});')
    yield "identity reused on new exam", once(
        'attemptId = writtenExamNewIdV2737G(previous, history);',
        'attemptId = previous && previous.attemptId || writtenExamNewIdV2737G(previous, history);')
    yield "unconfirmed legacy resume", once(
        '    if (session.attemptId === undefined) {\n      writtenExamLegacyDialogV2737G(session);\n      return false;\n    }',
        '    if (false) return false;')

def check_source(source):
    node = shutil.which("node")
    if not node:
        raise RuntimeError("Node.js unavailable; tests not run")
    def syntax(text):
        subprocess.run([node, "--check"], input=text, encoding="utf-8", text=True,
                       capture_output=True, check=True)
    def execute(text):
        return subprocess.run([node, "-e", HARNESS], input=text, encoding="utf-8",
                              text=True, capture_output=True, timeout=100)
    syntax(source)
    result = execute(source)
    print(result.stdout, end="")
    if result.returncode:
        raise RuntimeError(result.stderr)
    count = 0
    for name, changed in mutations(source):
        syntax(changed)  # A syntax rejection is never a semantic mutation PASS.
        result = execute(changed)
        if result.returncode == 0 or "AssertionError" not in result.stderr:
            raise RuntimeError("Mutation not semantically rejected: " + name + "\n" + result.stderr)
        print("MUTATION BLOCKED (valid syntax): " + name)
        count += 1
    print(f"SEMANTIC MUTATIONS PASS: {count}")

def main():
    control = runpy.run_path(str(ROOT / "tools/check-project-continuity-control.py"))
    phase = control["detect_v2737g_phase"]()
    if phase not in {"v2737g_implementation_prepared", "v2737g_implementation_committed",
                     "v2737g_closure_prepared", "v2737g_closure_committed"}:
        raise RuntimeError("Unexpected v27.37g phase: " + str(phase))
    check_source((ROOT / "app.js").read_text(encoding="utf-8"))
    print("v27.37g written exam completion: PASS; phase=" + phase)

if __name__ == "__main__":
    main()
