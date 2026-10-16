#!/usr/bin/env python3
"""Regression against actual app.js and the actual v23.1.1 patch block.

Only synthetic questions, in-memory DOM/storage/timers. No Git/network/writes.
--expect-before reports EXPECTED_DEFECT in actual unchanged code, never PASS.
Default separately identifies its in-memory predecessor fixture and current code.
"""
from pathlib import Path
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
NODE = Path(r"C:\Users\asarr\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe")
OLD_MODES = ["learning", "category", "open-questions", "topic-mistakes", "all-mistakes"]
TARGET = "last-exam-mistakes"
PATCH_START = "if (!window.ACCAOUI_V2311_LEARNING_PARTIAL_RESULT_PATCH) {"
GUARD_ARRAY = re.compile(
    r'function isLearningSessionActiveV2311\(\)\s*\{\s*try\s*\{\s*return\s*'
    r'(?P<array>\[[^\]]*\])\.includes\(String\(currentMode \|\| ""\)\);'
)
HARNESS = r'''
"use strict";
const assert=require("node:assert/strict"), fs=require("node:fs"), vm=require("node:vm");
const input=JSON.parse(fs.readFileSync(0,"utf8"));
const LEARNING_KEY="accaoui_active_learning_session", HISTORY_KEY="accaoui_exam_history";
const sentinel=JSON.stringify([{synthetic:"untouched-history"}]);
const questions=[
  {id:"synthetic-single-two",category:"Bürgerliches Gesetzbuch",
   question:"Synthetic single-answer question",answers:["Right","Wrong","Wrong B"],
   correct:[0],points:2,explanation:"Synthetic explanation A"},
  {id:"synthetic-multiple",category:"Bürgerliches Gesetzbuch",
   question:"Synthetic multiple-answer question",answers:["Right A","Right B","Wrong"],
   correct:[0,1],points:2,explanation:"Synthetic explanation B"},
  {id:"synthetic-open",category:"Bürgerliches Gesetzbuch",
   question:"Synthetic remaining question",answers:["Right","Wrong"],
   correct:[0],points:1,explanation:"Synthetic explanation C"}
];
function fixture(initialStore) {
  let run,now=0,nextTimer=0;
  const timers=new Map(),intervals=new Map();
  const store=new Map(initialStore||[[HISTORY_KEY,sentinel]]),writes=[],logs=[];
  class Element {
    constructor(tag="div") {
      this.tagName=tag.toUpperCase();this.children=[];this.parentNode=null;
      this.attrs={};this.dataset={};this.style={};this._html="";
      this.innerText="";this.textContent="";this.disabled=false;this.listeners=[];
    }
    get id(){return this.attrs.id||"";} set id(v){this.attrs.id=String(v);}
    get className(){return this.attrs.class||"";} set className(v){this.attrs.class=String(v);}
    get classList(){
      const e=this;
      return {
        contains(v){return e.className.split(/\s+/).includes(v);},
        add(...v){e.className=[...new Set([...e.className.split(/\s+/).filter(Boolean),...v])].join(" ");},
        remove(...v){e.className=e.className.split(/\s+/).filter(x=>x&&!v.includes(x)).join(" ");},
        toggle(v,force){
          const enabled=force===undefined?!this.contains(v):force;
          if(enabled)this.add(v);else this.remove(v);return enabled;
        }
      };
    }
    appendChild(c){c.remove();this.children.push(c);c.parentNode=this;return c;}
    insertBefore(c,ref){
      c.remove();const i=this.children.indexOf(ref);
      this.children.splice(i<0?this.children.length:i,0,c);c.parentNode=this;return c;
    }
    prepend(c){return this.insertBefore(c,this.children[0]);}
    insertAdjacentElement(position,c){
      assert.equal(position,"afterend");assert.ok(this.parentNode);
      const p=this.parentNode;return p.insertBefore(c,p.children[p.children.indexOf(this)+1]);
    }
    remove(){
      if(this.parentNode){
        const p=this.parentNode;p.children=p.children.filter(x=>x!==this);this.parentNode=null;
      }
    }
    setAttribute(name,value){
      this.attrs[name]=String(value);
      if(name.startsWith("data-"))this.dataset[name.slice(5)]=String(value);
      if(name==="style"){
        this.style={};
        for(const d of String(value).split(";")){
          const i=d.indexOf(":");if(i<0)continue;
          const k=d.slice(0,i).trim();if(k)this.style[k]=d.slice(i+1).trim();
        }
      }
    }
    addEventListener(type,callback){this.listeners.push({type,callback});}
    removeEventListener(type,callback){
      this.listeners=this.listeners.filter(x=>x.type!==type||x.callback!==callback);
    }
    matches(s){
      if(s.startsWith("#"))return this.id===s.slice(1);
      if(s.startsWith("."))return this.classList.contains(s.slice(1));
      return this.tagName===s.toUpperCase();
    }
    querySelectorAll(s){
      return this.children.flatMap(c=>[...(c.matches(s)?[c]:[]),...c.querySelectorAll(s)]);
    }
    querySelector(s){return this.querySelectorAll(s)[0]||null;}
    contains(e){return e===this||this.children.some(c=>c.contains(e));}
    closest(s){return this.matches(s)?this:this.parentNode?.closest(s)||null;}
    scrollIntoView(){}
    get innerHTML(){return this._html;}
    set innerHTML(html){
      this._html=String(html);this.children.forEach(c=>{c.parentNode=null;});this.children=[];
      const stack=[this],tags=/<\/?([a-z][\w-]*)\b([^>]*?)>/gi;let m;
      while((m=tags.exec(this._html))){
        const tag=m[1].toLowerCase();
        if(m[0].startsWith("</")){
          if(stack.length>1&&stack.at(-1).tagName===tag.toUpperCase())stack.pop();
          continue;
        }
        const e=new Element(tag);
        for(const a of m[2].matchAll(/([\w-]+)\s*=\s*"([^"]*)"/g))e.setAttribute(a[1],a[2]);
        if(e.attrs.onclick)e.onclick=()=>run(e.attrs.onclick);
        stack.at(-1).appendChild(e);
        if(!["br","hr","input","img","meta","link"].includes(tag))stack.push(e);
      }
    }
  }
  const body=new Element("body"),main=new Element("main");
  main.className="main-content";body.appendChild(main);
  const document={
    body,visibilityState:"visible",listeners:[],
    addEventListener(type,callback){this.listeners.push({type,callback});},
    createElement(tag){return new Element(tag);},
    getElementById(id){return body.querySelector("#"+id);},
    querySelector(s){return body.querySelector(s);},
    querySelectorAll(s){return body.querySelectorAll(s);}
  };
  const math=Object.create(Math);
  // Actual app shuffle uses sort(random()-0.5); zero preserves synthetic order.
  math.random=()=>0.5;
  const sandbox={
    document,Math:math,Date,
    crypto:{randomUUID(){return "11111111-1111-4111-8111-111111111111";}},
    localStorage:{
      getItem(k){return store.get(k)??null;},
      setItem(k,v){writes.push({operation:"set",key:k});store.set(k,String(v));},
      removeItem(k){writes.push({operation:"remove",key:k});store.delete(k);}
    },
    getComputedStyle(e){return {display:e.style.display||"block"};},
    addEventListener(){},
    setTimeout(callback,delay=0){
      const id=++nextTimer;timers.set(id,{callback,due:now+Number(delay)});return id;
    },
    clearTimeout(id){timers.delete(id);},
    setInterval(callback){const id=++nextTimer;intervals.set(id,callback);return id;},
    clearInterval(id){intervals.delete(id);},
    console:Object.fromEntries(["log","warn","error","info"].map(name=>[
      name,(...values)=>logs.push({name,values})])),
    alert(message){logs.push({name:"alert",values:[message]});},
    location:{reload(){}},
    fetch(){throw new Error("Network forbidden in synthetic fixture");}
  };
  sandbox.window=sandbox;
  const context=vm.createContext(sandbox);
  run=code=>vm.runInContext(code,context,{timeout:4000});
  run(input.app);run(input.patch);
  run("allQuestions="+JSON.stringify(questions)+";lastExamMistakes="+JSON.stringify(questions));
  const json=expression=>JSON.parse(run("JSON.stringify("+expression+")"));
  function advance(milliseconds){
    now+=milliseconds;let count=0;
    while(true){
      const next=[...timers.entries()].filter(([,t])=>t.due<=now)
        .sort((a,b)=>a[1].due-b[1].due||a[0]-b[0])[0];
      if(!next)break;assert.ok(++count<=100,"unexpected timer recursion");
      timers.delete(next[0]);next[1].callback();
    }
  }
  function click(e){
    assert.ok(e,"missing rendered action");if(e.disabled)return;
    assert.equal(typeof e.onclick,"function");e.onclick();
  }
  const get=id=>document.getElementById(id);
  const answers=()=>document.querySelectorAll(".answer-btn");
  function partialAction(){
    return document.querySelectorAll("button").find(
      e=>e.attrs.onclick==="showLearningPartialResultV2311()");
  }
  function answer(indexes){
    for(const i of indexes)click(answers().find(e=>Number(e.dataset.index)===i));
  }
  function start(mode){
    if(mode==="last-exam-mistakes")run("startMistakeTraining()");
    else run("startLearningSession(allQuestions,'Synthetic learning',"+JSON.stringify(mode)+")");
    advance(250);assert.ok(get("questionArea"));assert.ok(partialAction());
  }
  const state=()=>json("({mode:currentMode,title:currentTrainingTitle,questions:currentQuestions,"
    +"index:currentQuestionIndex,selected:selectedAnswers,correct:correctAnswersCount,"
    +"wrong:wrongAnswersCount,awaitingNext:learningQuestionAwaitingNext,"
    +"lastExamMistakes,examQuestions,examAnswers,examHistory})");
  const storageSnapshot=()=>JSON.stringify([...store]);
  function showPartial(){
    const s=state(),storage=storageSnapshot(),n=writes.length;
    click(partialAction());
    assert.deepEqual(state(),s);assert.equal(storageSnapshot(),storage);
    assert.equal(writes.length,n);assert.equal(store.get(HISTORY_KEY),sentinel);
  }
  return {run,json,store,writes,main,body,document,get,answers,answer,click,start,
          advance,state,storageSnapshot,showPartial,partialAction};
}
function metrics(f,answered,correct,wrong,open,percent){
  const h=f.main.innerHTML;assert.match(h,/learning-partial-result-v2311/);
  for(const [label,value] of [["Bearbeitet",answered+"/3"],["Richtig",correct],
                             ["Falsch",wrong],["Offen",open]])
    assert.match(h,new RegExp("<span>"+label+"</span>\\s*<strong>"+value+"</strong>"));
  assert.match(h,new RegExp('<div class="learning-partial-percent-v2311">\\s*'+percent+'%\\s*</div>'));
}
let checks=0;
function test(name,callback){callback();checks++;console.log("CURRENT CASE "+checks+" PASS: "+name);}
try{
  if(input.mode==="before"){
    const f=fixture();f.start("last-exam-mistakes");f.answer([0]);
    assert.equal(f.run("correctAnswersCount"),1);
    const h=f.main.innerHTML;f.showPartial();
    assert.equal(f.main.innerHTML,h);assert.ok(f.get("questionArea"));
    assert.doesNotMatch(f.main.innerHTML,/learning-partial-result-v2311/);
    assert.equal(f.get("smallNotice"),null);
    console.log("BEFORE EXPECTED_DEFECT: rendered Auswertung action returns without partial result");
    console.log("BEFORE COUNT=1 EXIT=0 RESULT=EXPECTED_DEFECT");
  }else{
    for(const mode of ["learning","category","open-questions","topic-mistakes",
                       "all-mistakes","last-exam-mistakes"]){
      test(mode+": first-answer notice and actual partial result",()=>{
        const f=fixture();f.start(mode);const h=f.main.innerHTML;
        f.showPartial();assert.equal(f.main.innerHTML,h);assert.ok(f.get("questionArea"));
        assert.equal(f.get("smallNotice")?.innerText,"Beantworten Sie zuerst mindestens eine Frage.");
        assert.ok(f.get("smallNotice").classList.contains("show"));
        assert.equal(f.run("correctAnswersCount"),0);assert.equal(f.run("wrongAnswersCount"),0);
        f.answer([0]);f.showPartial();metrics(f,1,1,0,2,100);
      });
    }
    for(const mode of ["dashboard","all-questions","mistake-overview","exam-start","exam",
                       "exam-result","oral-exam","oral-exam-session","flashcards",
                       "flashcards-overview","statistics","unknown","",null,0,
                       "LAST-EXAM-MISTAKES","last-exam-mistakes "]){
      test("blocked mode "+JSON.stringify(mode),()=>{
        const f=fixture();f.start("learning");f.answer([0]);
        f.run("currentMode="+JSON.stringify(mode));
        const h=f.main.innerHTML,c=f.get("learningAbortControlsV2311").innerHTML;
        f.run("window.renderLearningAbortControlsV2311()");
        assert.equal(f.get("learningAbortControlsV2311").innerHTML,c);
        f.showPartial();assert.equal(f.main.innerHTML,h);
        assert.doesNotMatch(f.main.innerHTML,/learning-partial-result-v2311/);
        assert.equal(f.get("smallNotice"),null);
      });
    }
    test("empty actual last-exam-mistakes entry keeps state and storage",()=>{
      const f=fixture();f.run("lastExamMistakes=[]");
      const s=f.state(),h=f.main.innerHTML,storage=f.storageSnapshot(),n=f.writes.length;
      f.run("startMistakeTraining()");
      assert.equal(f.get("smallNotice")?.innerText,"Keine Fehler aus der letzten Prüfung vorhanden.");
      assert.equal(f.main.innerHTML,h);assert.deepEqual(f.state(),s);
      assert.equal(f.storageSnapshot(),storage);assert.equal(f.writes.length,n);
      assert.equal(f.get("questionArea"),null);assert.equal(f.partialAction(),undefined);
    });
    test("mixed answers, existing actions, stored fresh-context resume and normal finish",()=>{
      const f=fixture();f.start("last-exam-mistakes");
      f.answer([0]);f.click(f.get("nextBtn"));f.answer([0,2]);
      assert.equal(f.run("correctAnswersCount"),1);assert.equal(f.run("wrongAnswersCount"),1);
      assert.equal(f.run("currentQuestionIndex"),1);assert.deepEqual(f.json("selectedAnswers"),[0,2]);
      assert.equal(f.run("learningQuestionAwaitingNext"),true);
      f.showPartial();metrics(f,2,1,1,1,50);
      assert.deepEqual(f.document.querySelectorAll("button").map(e=>e.attrs.onclick),
        ["location.reload()","showMistakeOverview()","showAllQuestions()","location.reload()"]);
      const saved=JSON.parse(f.store.get(LEARNING_KEY));
      assert.equal(saved.mode,"last-exam-mistakes");assert.equal(saved.currentIndex,1);
      assert.equal(saved.correctAnswersCount,1);assert.equal(saved.wrongAnswersCount,1);
      assert.equal(saved.awaitingNext,true);assert.deepEqual(saved.selectedAnswers,[0,2]);
      assert.equal(saved.questions.length,3);
      const r=fixture([...f.store]);
      assert.equal(r.run("currentMode"),"dashboard");
      assert.equal(r.run("resumeActiveLearningSession()"),true);r.advance(250);
      assert.equal(r.run("currentMode"),"last-exam-mistakes");
      assert.equal(r.run("currentQuestionIndex"),1);
      assert.equal(r.run("correctAnswersCount"),1);assert.equal(r.run("wrongAnswersCount"),1);
      assert.deepEqual(r.json("selectedAnswers"),[0,2]);
      assert.equal(r.run("learningQuestionAwaitingNext"),true);
      assert.ok(r.answers().every(e=>e.disabled));
      assert.equal(r.get("nextBtn").style.display,"inline-block");
      r.click(r.answers()[0]);
      assert.equal(r.run("correctAnswersCount"),1);assert.equal(r.run("wrongAnswersCount"),1);
      r.click(r.get("nextBtn"));assert.equal(r.run("currentQuestionIndex"),2);
      r.answer([0]);assert.equal(r.run("correctAnswersCount"),2);assert.equal(r.run("wrongAnswersCount"),1);
      r.click(r.get("nextBtn"));
      assert.match(r.main.innerHTML,/Lerneinheit bestanden/);
      assert.match(r.main.innerHTML,/Ergebnis: 67%/);assert.match(r.main.innerHTML,/2 richtig · 1 falsch/);
      assert.equal(r.store.has(LEARNING_KEY),false);
      assert.equal(r.get("questionArea"),null);assert.equal(r.partialAction(),undefined);
      assert.equal(r.store.get(HISTORY_KEY),sentinel);
    });
    test("existing written points unchanged by partial display",()=>{
      const f=fixture();f.start("last-exam-mistakes");f.answer([0]);
      const e="[getExamQuestionReachedPoints(currentQuestions[0],[]),"
        +"getExamQuestionReachedPoints(currentQuestions[0],[0]),"
        +"getExamQuestionReachedPoints(currentQuestions[1],[0]),"
        +"getExamQuestionReachedPoints(currentQuestions[1],[0,1]),"
        +"getExamQuestionReachedPoints(currentQuestions[1],[0,2])]";
      assert.deepEqual(f.json(e),[0,2,1,2,0]);f.showPartial();metrics(f,1,1,0,2,100);
      assert.deepEqual(f.json(e),[0,2,1,2,0]);
    });
    assert.equal(checks,26);console.log("CURRENT COUNT="+checks+" EXIT=0 RESULT=PASS");
  }
}catch(error){
  console.error(error?.stack||String(error));
  console.log((input.mode==="before"?"BEFORE":"CURRENT")+" COUNT="+checks+" EXIT=1 RESULT=FAIL");
  process.exitCode=1;
}
'''

def extract_block(source):
    if source.count(PATCH_START) != 1:
        raise RuntimeError("Actual v23.1.1 patch block is not unique")
    start = source.index(PATCH_START)
    end = source.index("\n/* =====================================================", start)
    if "v23.1.2" not in source[end:end + 180]:
        raise RuntimeError("Unexpected actual patch boundary")
    return source[start:end].strip() + "\n"

def execute(app, block, mode, label):
    print(label, flush=True)
    result = subprocess.run(
        [str(NODE), "-e", HARNESS],
        input=json.dumps({"app":app, "patch":block, "mode":mode}, ensure_ascii=False),
        text=True, encoding="utf-8", capture_output=True, timeout=60, check=False)
    print(result.stdout, end="", flush=True)
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr, flush=True)
    print(f"NODE MODE={mode} EXIT={result.returncode}", flush=True)
    if result.returncode != 0:
        raise RuntimeError("Actual behavioral assertions failed: " + mode)

def main():
    if sys.argv[1:] not in ([], ["--expect-before"]):
        raise RuntimeError("Usage: check-last-exam-mistakes-partial-result.py [--expect-before]")
    if not NODE.is_file():
        raise RuntimeError("Required bundled Node runtime unavailable")
    for path in ("app.js", "patch-v21.js"):
        result = subprocess.run([str(NODE), "--check", str(ROOT / path)],
                                capture_output=True, text=True, encoding="utf-8", check=False)
        print(f"SYNTAX {path} NODE_EXIT={result.returncode}", flush=True)
        if result.returncode or result.stderr:
            raise RuntimeError("Actual source syntax check failed: " + path + "\n" + result.stderr)
    app = (ROOT / "app.js").read_text(encoding="utf-8")
    block = extract_block((ROOT / "patch-v21.js").read_text(encoding="utf-8"))
    matches = list(GUARD_ARRAY.finditer(block))
    if len(matches) != 1:
        raise RuntimeError("Actual partial-result guard is not unique")
    match = matches[0]
    modes = json.loads(match.group("array"))
    if sys.argv[1:] == ["--expect-before"]:
        if modes != OLD_MODES:
            raise RuntimeError("Before mode requires actual unchanged five-mode guard")
        execute(app, block, "before", "ACTUAL UNCHANGED BEFORE CODE: expected defect")
        print("REGRESSION EXIT=0 RESULT=EXPECTED_DEFECT CURRENT_NOT_RUN", flush=True)
        return 0
    if modes != OLD_MODES + [TARGET]:
        raise RuntimeError("Current guard must be exactly the five old modes plus target")
    old_array = "[\n        " + ",\n        ".join(json.dumps(m) for m in OLD_MODES) + "\n      ]"
    predecessor = block[:match.start("array")] + old_array + block[match.end("array"):]
    execute(app, predecessor, "before",
            "IN-MEMORY PREDECESSOR GUARD FIXTURE: expected old behavior, not historical Git snapshot")
    execute(app, block, "current", "ACTUAL CURRENT CODE: complete behavioral regression")
    print("REGRESSION EXIT=0 RESULT=PASS CURRENT_NODE_EXIT=0", flush=True)
    print("LAST_EXAM_MISTAKES_PARTIAL_RESULT PASS", flush=True)
    return 0

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    try:
        raise SystemExit(main())
    except (AssertionError, OSError, RuntimeError, ValueError, subprocess.SubprocessError) as exc:
        print("REGRESSION EXIT=1 RESULT=FAIL: " + str(exc), file=sys.stderr, flush=True)
        raise SystemExit(1)
