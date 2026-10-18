#!/usr/bin/env python3
"""Actual dashboard-exam-date production code, synthetic DOM/storage and clocks only."""
from pathlib import Path
import json, os, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
NODE = Path(r'C:\Users\asarr\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe')
BEGIN = '// BEGIN ACCAOUI_V1_DASHBOARD_EXAM_DATES product'
END = '// END ACCAOUI_V1_DASHBOARD_EXAM_DATES product'
HARNESS = r'''
"use strict";
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const input=JSON.parse(fs.readFileSync(0,'utf8'));
const WK='accaoui_exam_date_written_v1', OK='accaoui_exam_date_oral_v1';
let count=0;
function test(name,fn){fn();count++;console.log('PASS '+name);}
function fixture(initial=[],options={}){
  const store=new Map(initial),writes=[],reads=[],faults={read:false,write:false,remove:false,ack:false,access:false};
  const timers=new Map(),observers=[],winEvents={},docEvents={};let nextTimer=0,main;
  let clock=new Date(2026,9,17,12,0).getTime();
  class E {
    constructor(tag){this.tagName=tag;this.attrs={};this.children=[];this.parentNode=null;this.events={};this.value='';this.hidden=false;this._text='';}
    get id(){return this.attrs.id||'';} set id(v){this.attrs.id=v;}
    setAttribute(k,v){this.attrs[k]=String(v);} getAttribute(k){return this.attrs[k]??null;}
    get textContent(){return this._text+this.children.map(x=>x.textContent).join('');}
    set textContent(v){this._text=String(v);this.children.forEach(x=>x.parentNode=null);this.children=[];}
    get isConnected(){return this===main||Boolean(this.parentNode?.isConnected);}
    appendChild(c){if(c.parentNode)c.remove();this.children.push(c);c.parentNode=this;return c;}
    insertAdjacentElement(where,c){assert.equal(where,'afterend');const p=this.parentNode;assert.ok(p);if(c.parentNode)c.remove();p.children.splice(p.children.indexOf(this)+1,0,c);c.parentNode=p;return c;}
    remove(){if(this.parentNode){this.parentNode.children=this.parentNode.children.filter(x=>x!==this);this.parentNode=null;observers.filter(x=>x.active).forEach(x=>x.callback());}}
    addEventListener(k,f){(this.events[k]??=[]).push(f);} removeEventListener(k,f){this.events[k]=(this.events[k]||[]).filter(x=>x!==f);}
    emit(k){for(const f of [...(this.events[k]||[])])f({preventDefault(){}});}
    focus(){doc.activeElement=this;}
    querySelector(s){return all(this).find(x=>matches(x,s))||null;}
  }
  function all(n){return n.children.flatMap(x=>[x,...all(x)]);}
  function matches(n,s){return s.startsWith('#')?n.id===s.slice(1):s.startsWith('.')?(n.attrs.class||'').split(/\s+/).includes(s.slice(1)):n.tagName===s;}
  main=new E('main');main.setAttribute('class','main-content');const hero=new E('section');hero.setAttribute('class','hero-grid');main.appendChild(hero);
  const doc={visibilityState:'visible',createElement:t=>new E(t),getElementById:id=>all(main).find(n=>n.id===id)||null,
    querySelector:s=>matches(main,s)?main:main.querySelector(s),
    addEventListener(k,f){(docEvents[k]??=[]).push(f);},removeEventListener(k,f){docEvents[k]=(docEvents[k]||[]).filter(x=>x!==f);}};
  class ClockDate extends Date{constructor(...a){super(...(a.length?a:[clock]));}static now(){return clock;}}
  class Observer{constructor(f){this.callback=f;this.active=false;observers.push(this);}observe(){this.active=true;}disconnect(){this.active=false;}}
  const storage={getItem(k){reads.push(k);if(faults.read&&k===WK)throw Error('synthetic-read');if(faults.ack&&k===WK)return null;return store.has(k)?store.get(k):null;},
    setItem(k,v){if(faults.write&&k===WK)throw Error('synthetic-quota');store.set(k,String(v));writes.push(['set',k,String(v)]);},
    removeItem(k){if(faults.remove&&k===WK)throw Error('synthetic-remove');store.delete(k);writes.push(['remove',k]);}};
  const ctx={document:doc,Date:ClockDate,console,MutationObserver:Observer,
    setTimeout(f,ms){const id=++nextTimer;timers.set(id,{f,ms});return id;},clearTimeout(id){timers.delete(id);},
    addEventListener(k,f){(winEvents[k]??=[]).push(f);},removeEventListener(k,f){winEvents[k]=(winEvents[k]||[]).filter(x=>x!==f);}};
  Object.defineProperty(ctx,'localStorage',{get(){if(faults.access)throw Error('synthetic-storage-access');return storage;}});
  ctx.window=ctx;vm.createContext(ctx);vm.runInContext(input.source,ctx);
  if(options.access)faults.access=true;
  if(options.read)faults.read=true;
  ctx.initDashboardExamDatesV1();
  const get=id=>doc.getElementById(id);
  const prefix=k=>k==='written'?'examDateWrittenV1':'examDateOralV1';
  return {ctx,store,writes,reads,faults,timers,observers,winEvents,docEvents,main,doc,get,
    input:k=>get(prefix(k)+'Input'),status:k=>get(prefix(k)+'Status').textContent,error:k=>get(prefix(k)+'Error').textContent,
    save(k,value){this.input(k).value=value;get(prefix(k)+'Form').emit('submit');},remove(k){get(prefix(k)+'Delete').emit('click');},
    event(k,arg={}){for(const f of [...(winEvents[k]||[])])f(arg);},visibility(v){doc.visibilityState=v;for(const f of [...(docEvents.visibilitychange||[])])f();},
    setClock(d){clock=d.getTime();},fireTimer(){const first=timers.entries().next().value;assert.ok(first);timers.delete(first[0]);first[1].f();}};
}

const pure=fixture().ctx;
test('strict input/calendar validation',()=>{
  for(const v of [null,undefined,0,[],{},'', '2026-2-01',' 2026-02-01','2026-02-01 ','0000-01-01','10000-01-01','2026-00-01','2026-13-01','2026-01-00','2026-04-31','2026-02-29','1900-02-29','2026-01-01T00:00:00Z','<script>'])assert.equal(pure.parseExamDateV1(v),null,String(v));
});
test('leap years and year bounds',()=>{for(const v of ['0001-01-01','0099-12-31','0100-01-01','2000-02-29','2028-02-29','9999-12-31'])assert.ok(pure.parseExamDateV1(v),v);assert.equal(pure.parseExamDateV1('0001-01-02').ordinal-pure.parseExamDateV1('0001-01-01').ordinal,1);});
test('today/tomorrow/yesterday',()=>{const n=new Date(2026,9,17,23,59);assert.equal(pure.examDateDisplayV1('2026-10-17',n).days,0);assert.equal(pure.examDateDisplayV1('2026-10-18',n).days,1);assert.equal(pure.examDateDisplayV1('2026-10-16',n).days,-1);assert.match(pure.examDateDisplayV1('2026-10-17',n).label,/heute/);assert.match(pure.examDateDisplayV1('2026-10-16',n).label,/vor 1 Tag/);});
test('month/year rollover',()=>{assert.equal(pure.examDateDisplayV1('2027-01-01',new Date(2026,11,31,23,59)).days,1);assert.equal(pure.examDateDisplayV1('2026-03-01',new Date(2026,1,28,23,59)).days,1);});
test('DST spring counts civil days',()=>{assert.equal(pure.examDateDisplayV1('2026-03-30',new Date(2026,2,28,23,59)).days,2);assert.equal(pure.examDateDisplayV1('2026-03-30',new Date(2026,2,29,0,1)).days,1);});
test('DST autumn counts civil days',()=>{assert.equal(pure.examDateDisplayV1('2026-10-26',new Date(2026,9,24,23,59)).days,2);assert.equal(pure.examDateDisplayV1('2026-10-26',new Date(2026,9,25,0,1)).days,1);});
test('UTC-near-midnight uses local date',()=>{const n=new Date('2026-10-17T23:30:00Z');const y=String(n.getFullYear()).padStart(4,'0'),m=String(n.getMonth()+1).padStart(2,'0'),d=String(n.getDate()).padStart(2,'0');assert.equal(pure.examDateDisplayV1(`${y}-${m}-${d}`,n).days,0);});
test('date formatting preserves literal date',()=>{assert.equal(pure.examDateDisplayV1('0001-01-02',new Date(2026,0,1)).date,'02.01.0001');assert.equal(pure.examDateDisplayV1('2026-10-17',new Date(2026,0,1)).date,'17.10.2026');});
test('empty is read-only and accessible',()=>{const f=fixture();assert.equal(f.writes.length,0);assert.match(f.status('written'),/Noch kein/);assert.match(f.status('oral'),/Noch kein/);assert.equal(f.input('written').getAttribute('type'),'date');assert.equal(f.get('examDateWrittenV1Error').getAttribute('role'),'alert');assert.equal(f.get('examDateWrittenV1Delete').hidden,true);});
test('two dates are independent; same date allowed',()=>{const f=fixture();f.save('written','2026-10-20');f.save('oral','2026-10-20');assert.equal(f.store.get(WK),'2026-10-20');assert.equal(f.store.get(OK),'2026-10-20');assert.match(f.status('written'),/Noch 3 Tage/);assert.equal(f.error('written'),'');});
test('change preserves other date',()=>{const f=fixture([[WK,'2026-10-20'],[OK,'2026-11-03']]);f.save('written','2026-10-22');assert.equal(f.store.get(WK),'2026-10-22');assert.equal(f.store.get(OK),'2026-11-03');});
test('delete preserves other date; reload',()=>{const f=fixture([[WK,'2026-10-20'],[OK,'2026-11-03']]);f.remove('written');assert.equal(f.store.has(WK),false);assert.equal(f.store.get(OK),'2026-11-03');const g=fixture([...f.store]);assert.match(g.status('written'),/Noch kein/);assert.equal(g.input('oral').value,'2026-11-03');g.remove('oral');assert.equal(g.store.size,0);assert.equal(fixture([...g.store]).writes.length,0);});
test('both dates reload exactly',()=>{const f=fixture();f.save('written','2028-02-29');f.save('oral','2029-03-01');const g=fixture([...f.store]);assert.equal(g.input('written').value,'2028-02-29');assert.equal(g.input('oral').value,'2029-03-01');assert.equal(g.writes.length,0);});
test('invalid/empty submit cannot change stored date',()=>{const f=fixture([[WK,'2026-10-20']]);for(const v of ['', '2026-02-29','2026-04-31','2026-10-20T01:00:00']){f.save('written',v);assert.equal(f.store.get(WK),'2026-10-20');assert.match(f.error('written'),/gültiges Datum/);assert.equal(f.doc.activeElement,f.input('written'));}assert.equal(f.writes.length,0);});
test('past and today remain editable and stored',()=>{const f=fixture([[WK,'2026-10-17'],[OK,'2026-10-16']]);assert.match(f.status('written'),/heute/);assert.match(f.status('oral'),/vor 1 Tag/);assert.equal(f.writes.length,0);f.save('oral','2026-11-01');assert.equal(f.store.get(OK),'2026-11-01');});
test('corrupt stored value is not executed or auto-repaired',()=>{const f=fixture([[WK,'<script>synthetic</script>'],[OK,'2026-11-01']]);assert.match(f.error('written'),/ungültig/);assert.equal(f.store.get(WK),'<script>synthetic</script>');assert.equal(f.writes.length,0);assert.equal(f.main.querySelector('script'),null);f.remove('written');assert.equal(f.store.has(WK),false);assert.equal(f.store.get(OK),'2026-11-01');});
test('read exception is contained',()=>{const f=fixture([[OK,'2026-11-01']],{read:true});assert.match(f.error('written'),/nicht gelesen/);assert.equal(f.input('oral').value,'2026-11-01');assert.equal(f.writes.length,0);});
test('localStorage accessor exception is contained',()=>{const f=fixture([],{access:true});assert.match(f.error('written'),/nicht gelesen/);assert.match(f.error('oral'),/nicht gelesen/);assert.equal(f.writes.length,0);});
test('quota/write error keeps draft and previous values',()=>{const f=fixture([[WK,'2026-10-20'],[OK,'2026-11-03']]);f.faults.write=true;f.save('written','2026-12-01');assert.equal(f.input('written').value,'2026-12-01');assert.equal(f.store.get(WK),'2026-10-20');assert.equal(f.store.get(OK),'2026-11-03');assert.match(f.error('written'),/nicht sicher gespeichert/);});
test('unconfirmed write never reports success',()=>{const f=fixture();f.faults.ack=true;f.save('written','2026-12-01');assert.match(f.error('written'),/nicht sicher gespeichert/);assert.equal(f.input('written').value,'2026-12-01');});
test('delete error preserves existing dates',()=>{const f=fixture([[WK,'2026-10-20'],[OK,'2026-11-03']]);f.faults.remove=true;f.remove('written');assert.equal(f.store.get(WK),'2026-10-20');assert.equal(f.store.get(OK),'2026-11-03');assert.match(f.error('written'),/Löschen konnte nicht bestätigt/);});
test('duplicate init creates no duplicate DOM/listeners/timers',()=>{const f=fixture();f.ctx.initDashboardExamDatesV1();assert.equal(f.main.children.filter(x=>x.id==='examDatesDashboardV1').length,1);assert.equal(f.winEvents.focus.length,1);assert.equal(f.winEvents.storage.length,1);assert.equal(f.docEvents.visibilitychange.length,1);assert.equal(f.timers.size,1);});
test('midnight and focus refresh without storage writes',()=>{const f=fixture([[WK,'2026-10-18']]);assert.match(f.status('written'),/Noch 1 Tag/);f.setClock(new Date(2026,9,18,0,0,1));f.fireTimer();assert.match(f.status('written'),/heute/);f.setClock(new Date(2026,9,19,12));f.event('focus');assert.match(f.status('written'),/vor 1 Tag/);assert.equal(f.writes.length,0);});
test('visibility pauses only own timer and preserves drafts',()=>{const f=fixture([[WK,'2026-10-20']]);f.input('written').value='2026-12-01';f.visibility('hidden');assert.equal(f.timers.size,0);f.visibility('visible');assert.equal(f.timers.size,1);assert.equal(f.input('written').value,'2026-12-01');assert.equal(f.writes.length,0);});
test('external date update; unrelated storage event ignored',()=>{const f=fixture([[WK,'2026-10-20']]);const n=f.reads.length;f.event('storage',{key:'unrelated'});assert.equal(f.reads.length,n);f.store.set(WK,'2026-11-01');f.event('storage',{key:WK});assert.equal(f.input('written').value,'2026-11-01');assert.equal(f.writes.length,0);});
test('removing dashboard disposes own listeners/timer',()=>{const f=fixture();f.get('examDatesDashboardV1').remove();assert.equal(f.timers.size,0);assert.equal(f.winEvents.focus.length,0);assert.equal(f.winEvents.storage.length,0);assert.equal(f.docEvents.visibilitychange.length,0);assert.ok(f.observers.every(x=>!x.active));});
test('existing sessions/history/progress remain byte-identical',()=>{
 const originals=['accaoui_exam_history','accaoui_topic_stats','accaoui_topic_mistakes','accaoui_answered_questions','accaoui_active_session','accaoui_active_learning_session','accaoui_active_flashcard_session','accaoui_flashcard_progress','accaoui_oral_exam_mistakes_v2324'].map((k,i)=>[k,JSON.stringify({synthetic:true,number:i,mode:'untouched',answers:[1,2]})]);
 const f=fixture(originals);f.save('written','2026-11-01');f.save('oral','2026-11-02');f.save('written','2026-11-03');f.remove('written');f.event('focus');for(const [k,v] of originals)assert.equal(f.store.get(k),v,k);assert.ok(f.writes.every(x=>x[1]===WK||x[1]===OK));
});
console.log(JSON.stringify({timezone:process.env.TZ,cases:count,result:'PASS'}));
'''

def main():
    if sys.argv[1:]: raise RuntimeError('No optional skip flags supported')
    if not NODE.is_file(): raise RuntimeError('Existing Node runtime is unavailable')
    app=(ROOT/'app.js').read_text(encoding='utf-8')
    if app.count(BEGIN)!=1 or app.count(END)!=1: raise RuntimeError('Production block is not unique')
    source=app[app.index(BEGIN):app.index(END)+len(END)]
    boot=app[app.index('function startLocalApp() {'):app.index('\nfunction renderLoginOrAccessNotice(')]
    if boot.count('  initDashboardExamDatesV1();')!=1: raise RuntimeError('Actual authorized local-app initialization call missing')
    for path in ('app.js','patch-v21.js'):
        p=subprocess.run([str(NODE),'--check',str(ROOT/path)],capture_output=True,text=True,encoding='utf-8')
        print('SYNTAX '+path+' EXIT='+str(p.returncode),flush=True)
        if p.returncode or p.stderr: raise RuntimeError(p.stderr or 'Actual JavaScript syntax error')
    total=0
    for timezone in ('Europe/Berlin','Pacific/Kiritimati','America/Los_Angeles'):
        env=os.environ.copy();env['TZ']=timezone
        p=subprocess.run([str(NODE),'-e',HARNESS],input=json.dumps({'source':source}),env=env,capture_output=True,text=True,encoding='utf-8',timeout=60)
        print(p.stdout,end='',flush=True)
        if p.stderr: print(p.stderr,end='',file=sys.stderr,flush=True)
        print('NODE '+timezone+' EXIT='+str(p.returncode),flush=True)
        if p.returncode or p.stderr: raise RuntimeError('Actual exam-date production regression failed')
        result=json.loads(p.stdout.strip().splitlines()[-1]);total+=result['cases']
    print('EXAM_DATES_CURRENT_PASS TOTAL_CASES='+str(total)+' TIMEZONES=3',flush=True)
    return 0

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8');sys.stderr.reconfigure(encoding='utf-8')
    try: raise SystemExit(main())
    except Exception as exc:
        print('EXAM_DATES_CURRENT_FAIL: '+str(exc),file=sys.stderr,flush=True)
        raise SystemExit(1)
