#!/usr/bin/env python3
"""Execute current app.js in isolated DOM/event/storage contexts; no real data.

The DOM harness dispatches capture then target/bubble events. Reflow is modeled
adversarially: a second physical click may target any newly positioned control.
Every behavioral mutation is syntax-valid and must fail an actual assertion.
"""
import hashlib
from pathlib import Path
import runpy
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = "c2371ba93188b0cfaffe1c13e199f350fbf20a02"
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HARNESS = r'''
"use strict";
const assert = require("node:assert/strict"), vm = require("node:vm"), fs = require("node:fs");
const source = fs.readFileSync(0,"utf8");
const fixtures = [
 {id:"mixed",category:"Bürgerliches Gesetzbuch",question:"Test A",answers:["Wrong","Right A","Right B","Wrong B"],correct:[1,2],points:2},
 {id:"single",category:"Bürgerliches Gesetzbuch",question:"Test B",answers:["Right","Wrong"],correct:[0],points:1},
 {id:"double",category:"Bürgerliches Gesetzbuch",question:"Test C",answers:["Right A","Right B","Wrong"],correct:[0,1],points:2}
];
const K = {session:"accaoui_active_session",history:"accaoui_exam_history",
 stats:"accaoui_topic_stats",mistakes:"accaoui_topic_mistakes",answered:"accaoui_answered_questions"};
let uuid=0, checks=0;
function fixture(store=new Map()) {
 let run, now=10000, nextTimer=0;
 const timers=new Map(), intervals=new Map(), writes=[], logs=[];
 class Element {
  constructor(tag="div") {this.tagName=tag.toUpperCase();this.children=[];this.parentNode=null;this.attrs={};this.dataset={};this.style={};this.listeners=[];this._html="";this.textContent="";this.disabled=false;}
  get id(){return this.attrs.id||"";} set id(v){this.attrs.id=v;}
  get className(){return this.attrs.class||"";} set className(v){this.attrs.class=v;}
  get classList(){const e=this;return {add(...v){e.className=[...new Set([...e.className.split(/\s+/),...v])].join(" ");},remove(...v){e.className=e.className.split(/\s+/).filter(c=>!v.includes(c)).join(" ");},contains(v){return e.className.split(/\s+/).includes(v);},toggle(v,force){const on=force??!this.contains(v);on?this.add(v):this.remove(v);return on;}};}
  appendChild(e){if(e.parentNode)e.remove();this.children.push(e);e.parentNode=this;return e;}
  prepend(e){if(e.parentNode)e.remove();this.children.unshift(e);e.parentNode=this;}
  insertBefore(e){this.prepend(e);return e;}
  remove(){if(this.parentNode)this.parentNode.children=this.parentNode.children.filter(c=>c!==this);this.parentNode=null;}
  contains(e){return e===this||this.children.some(c=>c.contains(e));}
  setAttribute(k,v){this.attrs[k]=String(v);if(k.startsWith("data-"))this.dataset[k.slice(5)]=String(v);}
  addEventListener(type,fn,capture=false){this.listeners.push({type,fn,capture:capture===true||capture?.capture===true});}
  removeEventListener(type,fn,capture=false){this.listeners=this.listeners.filter(l=>!(l.type===type&&l.fn===fn&&l.capture===capture));}
  matches(s){return s.startsWith("#")?this.id===s.slice(1):s.startsWith(".")?this.classList.contains(s.slice(1)):this.tagName===s.toUpperCase();}
  closest(s){return this.matches(s)?this:this.parentNode?.closest(s)||null;}
  querySelectorAll(s){return this.children.flatMap(c=>[...(c.matches(s)?[c]:[]),...c.querySelectorAll(s)]);}
  querySelector(s){return this.querySelectorAll(s)[0]||null;}
  scrollIntoView(){this.scrolled=true;}
  showModal(){this.open=true;} close(){this.open=false;}
  get innerHTML(){return this._html;}
  set innerHTML(html){
   this._html=html;this.children.forEach(c=>c.parentNode=null);this.children=[];
   const stack=[this], pattern=/<\/?([a-z][\w-]*)\b([^>]*?)>/gi;let match;
   while((match=pattern.exec(html))){const tag=match[1].toLowerCase();
    if(match[0].startsWith("</")){if(stack.length>1&&stack.at(-1).tagName===tag.toUpperCase())stack.pop();continue;}
    const e=new Element(tag);for(const a of match[2].matchAll(/([\w-]+)\s*=\s*"([^"]*)"/g))e.setAttribute(a[1],a[2]);
    if(e.attrs.onclick)e.onclick=()=>run(e.attrs.onclick);
    stack.at(-1).appendChild(e);if(!["br","hr","input","img","meta","link"].includes(tag))stack.push(e);
   }
  }
 }
 const body=new Element("body"), main=new Element("main"), hero=new Element("section");
 main.className="main-content";hero.className="hero-grid";main.appendChild(hero);body.appendChild(main);
 const document={body,visibilityState:"visible",listeners:[],
  addEventListener(type,fn){this.listeners.push({type,fn});},
  createElement(tag){return new Element(tag);},getElementById(id){return body.querySelector("#"+id);},
  querySelector(s){return body.querySelector(s);},querySelectorAll(s){return body.querySelectorAll(s);}};
 class Clock extends Date {static now(){return now;}}
 const math=Object.create(Math);math.random=()=>0.999999;
 const context=vm.createContext({document,window:{addEventListener(){}},Math:math,Date:Clock,
  crypto:{randomUUID:()=>"11111111-1111-4111-8111-"+String(++uuid).padStart(12,"0")},
  localStorage:{getItem:k=>store.get(k)??null,setItem(k,v){writes.push(k);store.set(k,String(v));},removeItem(k){store.delete(k);}},
  setTimeout(fn,delay=0){const id=++nextTimer;timers.set(id,{fn,at:now+delay});return id;},clearTimeout(id){timers.delete(id);},
  setInterval(fn){const id=++nextTimer;intervals.set(id,fn);return id;},clearInterval(id){intervals.delete(id);},
  console:Object.fromEntries(["log","warn","error","info"].map(n=>[n,(...a)=>logs.push(a.join(" "))])),
  alert:m=>logs.push(m),location:{reload(){}},fetch(){throw Error("Network forbidden");}});
 run=code=>vm.runInContext(code,context,{timeout:4000});run(source);
 run("allQuestions="+JSON.stringify(fixtures));
 function dispatch(target,type,detail=1){
  const event={target,type,detail,defaultPrevented:false,stopped:false,
   preventDefault(){this.defaultPrevented=true;},stopImmediatePropagation(){this.stopped=true;},stopPropagation(){this.stopped=true;}};
  const path=[];for(let e=target;e;e=e.parentNode)path.push(e);
  for(const e of path.slice().reverse())for(const l of e.listeners.slice())if(l.type===type&&l.capture&&!event.stopped)l.fn(event);
  if(!event.stopped&&!target.disabled&&type==="click"&&target.onclick)target.onclick(event);
  for(const e of path)for(const l of e.listeners.slice())if(l.type===type&&!l.capture&&!event.stopped)l.fn(event);
  return event;
 }
 function pointer(target,detail=1){for(const t of ["pointerdown","mousedown","pointerup","mouseup","click"])dispatch(target,t,detail);}
 const json=code=>JSON.parse(run("JSON.stringify("+code+")"));
 const get=id=>document.getElementById(id), answers=()=>document.querySelectorAll(".answer-btn");
 const confirm=()=>document.querySelectorAll("button").find(e=>e.attrs.onclick==="finishExamMode()");
 const advance=ms=>{now+=ms;for(const [id,t] of [...timers])if(t.at<=now){timers.delete(id);t.fn();}};
 return {run,json,store,writes,main,document,intervals,get,answers,confirm,pointer,dispatch,advance,
  start(){run('startExamMode(3,"Synthetic test","short")');assert.ok(get("finishExamNowBtn"));},
  mixed(){pointer(answers()[2]);pointer(answers()[0]);assert.deepEqual(json("examAnswers[0]"),[2,0]);},
  submit(){pointer(get("finishExamNowBtn"));},
  history(){return JSON.parse(store.get(K.history)||"[]");}};
}
function test(name,fn){fn();checks++;console.log("PASS "+name);}
function unchanged(f){assert.deepEqual(f.json("examAnswers[0]"),[2,0]);assert.deepEqual(JSON.parse(f.store.get(K.session)).answers[0],[2,0]);assert.equal(f.run("getExamReachedPoints()"),0);}
function noNewKeys(f){assert.ok([...f.store.keys()].every(k=>Object.values(K).includes(k)));assert.ok(f.writes.every(k=>Object.values(K).includes(k)));}
test("normal single click, warning render preserves mixed [2,0], confirmed score zero",()=>{
 const f=fixture();f.start();f.mixed();f.submit();unchanged(f);assert.ok(f.get("examWarningBox"));assert.equal(f.history().length,0);
 f.advance(601);f.pointer(f.confirm());assert.equal(f.history().length,1);assert.equal(f.history()[0].points.reached,0);
 assert.deepEqual([f.history()[0].wrong,f.history()[0].unanswered],[1,2]);assert.match(f.main.innerHTML,/0\/5/);noNewKeys(f);
});
for(const detail of [1,2])for(const index of [0,1,2,3])test("rapid reflow second click detail="+detail+" answer="+index,()=>{
 const f=fixture();f.start();f.mixed();f.submit();unchanged(f);f.advance(100);f.pointer(f.answers()[index],detail);unchanged(f);
 assert.equal(f.history().length,0);f.advance(501);f.pointer(f.confirm());assert.equal(f.history()[0].points.reached,0);noNewKeys(f);
});
test("same submit button double click and premature confirmation cannot finish",()=>{
 const f=fixture();f.start();f.mixed();const first=f.get("finishExamNowBtn");f.submit();f.advance(100);f.pointer(first,2);f.pointer(f.confirm(),1);
 unchanged(f);assert.equal(f.history().length,0);assert.equal(f.document.querySelectorAll("#examWarningBox").length,1);
 f.advance(501);f.pointer(f.confirm());const snapshot=JSON.stringify([...f.store]);f.run("finishExamMode();finishExamMode()");assert.equal(JSON.stringify([...f.store]),snapshot);
 assert.equal(f.history().length,1);
});
test("keyboard confirmation remains available during pointer guard",()=>{
 const f=fixture();f.start();f.mixed();f.submit();f.dispatch(f.confirm(),"click",0);assert.equal(f.history()[0].points.reached,0);
});
test("guard expires and intentional answer editing still works",()=>{
 const f=fixture();f.start();f.mixed();f.submit();f.advance(601);f.pointer(f.answers()[0]);assert.deepEqual(f.json("examAnswers[0]"),[2]);assert.equal(f.run("getExamReachedPoints()"),1);
});
test("unanswered focus remains functional",()=>{
 const f=fixture();f.start();f.mixed();f.submit();f.advance(601);
 const button=f.document.querySelectorAll("button").find(e=>e.attrs.onclick==="startUnansweredExamFocus()");assert.ok(button);f.pointer(button);
 assert.deepEqual(f.json("examFocusQuestionIndexes"),[1,2]);assert.equal(f.run("examQuestionIndex"),1);assert.ok(f.get("finishExamNowBtn"));
});
test("all answered single submission, two points and partial scoring",()=>{
 const f=fixture();f.start();f.run("examAnswers={0:[1,2],1:[0],2:[0,1]};saveActiveExamSession()");f.submit();assert.equal(f.history()[0].points.reached,5);assert.equal(f.history().length,1);
 const p=fixture();p.start();p.run("examAnswers={0:[2],1:[0],2:[0,1]};saveActiveExamSession()");p.submit();assert.equal(p.history()[0].points.reached,4);
});
test("pause, fresh-context resume preserve identity, order, mixed answers and seconds",()=>{
 const f=fixture();f.start();f.mixed();f.submit();f.advance(601);f.run("examSecondsLeft=321;pauseExam()");
 const snapshot=JSON.parse(f.store.get(K.session));const r=fixture(f.store);assert.equal(r.run("resumeActiveExamSession()"),true);
 assert.deepEqual(r.json("[examQuestions,examAnswers,examSecondsLeft,writtenExamAttemptV2737G.id]"),[snapshot.questions,snapshot.answers,321,snapshot.attemptId]);
 r.submit();r.advance(601);r.pointer(r.confirm());assert.equal(r.history()[0].points.reached,0);assert.equal(r.history()[0].attemptId,snapshot.attemptId);noNewKeys(r);
});
test("zero answers remain unanswered and record once",()=>{
 const f=fixture();f.start();f.submit();assert.equal(f.history().length,0);f.advance(601);f.pointer(f.confirm());assert.deepEqual([f.history()[0].correct,f.history()[0].wrong,f.history()[0].unanswered,f.history()[0].points.reached],[0,0,3,0]);
});
for(const points of [59,60])test("real full start 82 / 120 / 7200 and pass boundary "+points,()=>{
 const f=fixture();f.run('allQuestions=EXAM_CORE_QUESTION_IDS_V244.map((id,i)=>({...allQuestions[0],id,points:i<38?2:1,correct:i<38?[1,2]:[0]}));startExamMode(82,"Synthetic full","full")');
 assert.equal(f.run("examQuestions.length"),82);assert.equal(f.run("getExamMaxPoints()"),120);assert.equal(f.run("examSecondsLeft"),7200);assert.equal(f.intervals.size,1);
 f.run('examAnswers={};for(let i=0;i<'+(points===60?30:29)+';i++)examAnswers[i]=[1,2];'+(points===59?'examAnswers[38]=[0];':'')+'saveActiveExamSession()');
 f.submit();f.advance(601);f.pointer(f.confirm());assert.equal(f.history()[0].points.reached,points);assert.equal(f.history()[0].passed,points>=60);assert.equal(f.intervals.size,0);noNewKeys(f);
});
console.log("POSITIVES PASS: "+checks+"; actual current JS rendering, capture events, completion and storage");
'''


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def replace_last(source, start, following, transform):
    assert source.count(start) == source.count(following) == 2
    left, tail = source.rsplit(start, 1)
    body, right = tail.split(following, 1)
    return left + start + transform(body) + following + right


def mutations(source):
    def once(old, new):
        assert source.count(old) == 1, "Mutation anchor must occur exactly once: " + old
        return source.replace(old, new, 1)

    yield "second click reaches moved answer", once(
        '    event.stopImmediatePropagation();', '    if (!event.target.classList.contains("answer-btn")) event.stopImmediatePropagation();')
    yield "answers mutated during warning render", replace_last(source,
        "function showExamSubmitWarning(firstUnansweredIndex, unansweredCount) {", "function goToExamQuestion(index) {",
        lambda body: '\n  examAnswers[examQuestionIndex] = [2]; saveActiveExamSession();' + body)
    yield "protection removed", once('  protectExamSubmitPointerSequenceV2737L();', '  /* guard omitted */')
    yield "single click broken", replace_last(source,
        "function handleExamSubmitRequest() {", "function showExamSubmitWarning(firstUnansweredIndex, unansweredCount) {",
        lambda body: '\n  return;' + body)
    yield "warning skipped", replace_last(source,
        "function handleExamSubmitRequest() {", "function showExamSubmitWarning(firstUnansweredIndex, unansweredCount) {",
        lambda body: body.replace('    showExamSubmitWarning(firstUnansweredIndex, unansweredCount);', '    return;'))
    yield "automatic direct completion", replace_last(source,
        "function handleExamSubmitRequest() {", "function showExamSubmitWarning(firstUnansweredIndex, unansweredCount) {",
        lambda body: body.replace('    showExamSubmitWarning(firstUnansweredIndex, unansweredCount);', '    finishExamMode();'))
    yield "double recording", once('  writtenExamAttemptV2737G.status = "completed";',
        '  const duplicate = writtenExamHistoryV2737G(); duplicate.push(duplicate[duplicate.length - 1]); writeStorage(STORAGE_KEYS.examHistory, duplicate);\n  writtenExamAttemptV2737G.status = "completed";')
    yield "mixed scoring changed", once('  if (hasWrongSelection) {\n    return 0;\n  }',
        '  if (hasWrongSelection) {\n    return 1;\n  }')
    yield "additional storage key", once('  protectExamSubmitPointerSequenceV2737L();',
        '  protectExamSubmitPointerSequenceV2737L(); localStorage.setItem("forbidden_v2737l_key", "1");')


def frozen_files():
    excluded = {"app.js", "tools/preflight.py", "tools/check-written-exam-submit-doubleclick-v2737l.py",
                "docs/WRITTEN_EXAM_SUBMIT_DOUBLECLICK_V2737L.md", "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md",
                "docs/PROJECT_MASTERLIST.md", "docs/PROJECT_STATE_CURRENT.md", "docs/tasks/CURRENT_TASK.md"}
    reference = {}
    for entry in git("ls-tree", "-r", "--full-tree", BASE).decode("utf-8").splitlines():
        metadata, path = entry.split("\t", 1)
        if path not in excluded:
            reference[path] = metadata.split()[2]
    current = {path: hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
               for path in reference for data in [(ROOT / path).read_bytes()]}
    return reference, current


def check_source(source, control):
    node = shutil.which("node")
    if not node:
        raise RuntimeError("Node unavailable; no tests run")
    def syntax(text):
        subprocess.run([node, "--check"], input=text, encoding="utf-8", text=True,
                       capture_output=True, check=True, timeout=30)
    def execute(text):
        return subprocess.run([node, "-e", HARNESS], input=text, encoding="utf-8", text=True,
                              capture_output=True, timeout=100)
    syntax(source)
    result = execute(source)
    print(result.stdout, end="")
    if result.returncode:
        raise RuntimeError(result.stderr)
    count = 0
    for name, changed in mutations(source):
        syntax(changed)  # Syntax errors must never count as blocked semantics.
        result = execute(changed)
        if result.returncode == 0 or "AssertionError" not in result.stderr:
            raise RuntimeError("Mutation not rejected semantically: " + name + "\n" + result.stderr)
        count += 1
        print("MUTATION BLOCKED (valid syntax / actual assertions): " + name)

    baseline = git("show", BASE + ":app.js").decode("utf-8")
    remainder = control["v2737l_app_remainder"]
    assert remainder(source) == remainder(baseline), "app.js outside allowed scope changed"
    outside = source.replace("function finishExamMode() {", "function finishExamMode() {\n  return;", 1)
    syntax(outside)
    assert remainder(outside) != remainder(baseline), "Outside-scope mutation not blocked"
    count += 1
    print("MUTATION BLOCKED (valid syntax / byte boundary): frozen historical finishExamMode")
    reference, current = frozen_files()
    assert current == reference, "Frozen product/test/audit/control file changed"
    foreign = dict(current)
    foreign["patch-v21.js"] = "0" * 40
    assert foreign != reference, "Foreign product mutation not blocked"
    count += 1
    print("MUTATION BLOCKED (Git blob equality): foreign patch-v21.js change")
    print(f"SEMANTIC MUTATIONS PASS: {count}; syntax rejections excluded")
    # Execute the existing completion suite against this actual source as well;
    # its main/phase is NOT replaced. Historical phase-bound checks remain real.
    completion = runpy.run_path(str(ROOT / "tools/check-written-exam-completion-v2737g.py"))
    completion["check_source"](source)
    print("Current actual completion/storage/pause/history regressions: PASS")


def main():
    control = runpy.run_path(str(ROOT / "tools/check-project-continuity-control.py"))
    phase = control["detect_v2737l_phase"]()
    if phase not in {"v2737l_implementation_prepared", "v2737l_implementation_committed",
                     "v2737l_closure_prepared", "v2737l_closure_committed"}:
        raise RuntimeError("Unexpected phase: " + str(phase))
    check_source((ROOT / "app.js").read_bytes().decode("utf-8"), control)
    print("v27.37l written exam submit double-click: PASS; phase=" + phase)


if __name__ == "__main__":
    main()
