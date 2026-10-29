/* W05 content workflow. Pure local/synthetic contract; no live provider or bank mutation. */
(function (root, mod) {
"use strict";
const KEY="accaoui_content_workspace_v1";
const CATEGORIES=Object.freeze(["Recht der öffentlichen Sicherheit und Ordnung","Gewerberecht","Datenschutzrecht","Bürgerliches Gesetzbuch","Strafgesetzbuch und Strafverfahrensrecht","Unfallverhütungsvorschriften Wach- und Sicherungsdienste","Umgang mit Waffen","Umgang mit Menschen","Grundzüge der Sicherheitstechnik"]);
const CHECKS=Object.freeze(["facts","duplicates","rights","wording","answer","explanation","category"]);
const ROLES=new Set(["admin","instructor","participant"]);
const BANKS=new Set(["written","oral","card"]);
const STATES=new Set(["draft","review","approved","published","archived"]);
const id=v=>typeof v==="string"&&/^[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}$/.test(v);
const record=v=>v!==null&&typeof v==="object"&&!Array.isArray(v);
const text=(v,n=12000)=>typeof v==="string"&&v.trim().length>0&&v.length<=n;
const clone=v=>JSON.parse(JSON.stringify(v));
function fail(message){throw Error(message);}
function need(v,m){if(!v)fail(m);}
function day(v){if(typeof v!=="string"||!/^\d{4}-\d{2}-\d{2}$/.test(v)||Number(v.slice(0,4))<1)return false;const d=new Date(v+"T12:00:00Z");return Number.isFinite(+d)&&d.toISOString().slice(0,10)===v;}
function empty(){return {schema:1,revision:0,courses:[],sources:[],entries:[],audit:[]};}
function courseValid(c){return record(c)&&id(c.id)&&text(c.title,200)&&day(c.startDay)&&day(c.endDay)&&c.startDay<=c.endDay&&["active","archived"].includes(c.status)&&Array.isArray(c.instructorIds)&&c.instructorIds.every(id)&&new Set(c.instructorIds).size===c.instructorIds.length;}
function sourceValid(s){return record(s)&&id(s.id)&&text(s.title,200)&&text(s.locator,1000)&&["unknown","analysis","own"].includes(s.usage)&&typeof s.ownerReviewed==="boolean";}
function questionValid(e){
 if(!record(e)||!id(e.id)||!id(e.courseId)||!id(e.sourceId)||!BANKS.has(e.bank)||!CATEGORIES.includes(e.category)||!text(e.question))return false;
 if(e.bank==="written")return [1,2].includes(e.points)&&Array.isArray(e.answers)&&[4,5].includes(e.answers.length)&&e.answers.every(v=>text(v,2000))&&new Set(e.answers.map(v=>v.normalize("NFKC").trim().toLocaleLowerCase("de"))).size===e.answers.length&&Array.isArray(e.correct)&&e.correct.length===e.points&&new Set(e.correct).size===e.correct.length&&e.correct.every(v=>Number.isInteger(v)&&v>=0&&v<e.answers.length)&&text(e.explanation);
 if(e.bank==="oral")return text(e.modelAnswer)&&text(e.followUps)&&text(e.criticalMistakes);
 return text(e.back);
}
function valid(s){
 if(!record(s)||s.schema!==1||!Number.isSafeInteger(s.revision)||s.revision<0||!["courses","sources","entries","audit"].every(k=>Array.isArray(s[k]))||s.courses.length>200||s.sources.length>500||s.entries.length>2000||s.audit.length>1000)return false;
 if(!s.courses.every(courseValid)||!s.sources.every(sourceValid))return false;
 for(const a of [s.courses,s.sources,s.entries])if(new Set(a.map(v=>v.id)).size!==a.length)return false;
 return s.entries.every(e=>questionValid(e)&&s.courses.some(c=>c.id===e.courseId)&&s.sources.some(x=>x.id===e.sourceId)&&STATES.has(e.status)&&Number.isSafeInteger(e.version)&&e.version>=1&&id(e.createdBy)&&(e.approval===null||(record(e.approval)&&id(e.approval.actorId)))&&(!["approved","published"].includes(e.status)||(e.review&&CHECKS.every(k=>e.review.checks?.[k]===true)&&e.approval&&e.approval.actorId!==e.review.actorId))&&(e.review===null||(record(e.review)&&id(e.review.actorId)&&day(e.review.day)&&CHECKS.every(k=>typeof e.review.checks?.[k]==="boolean"))))&&s.audit.every(a=>record(a)&&Number.isSafeInteger(a.revision)&&id(a.actorId)&&text(a.action,100)&&text(a.entityId,80)&&text(a.utc,50));
}
function read(storage){
 try{const raw=storage.getItem(KEY);if(raw===null)return {ok:true,state:empty(),raw:null};if(raw.length>3000000)return {ok:false,error:"Der lokale Entwurf ist zu groß und wird nicht überschrieben."};const s=JSON.parse(raw);return valid(s)?{ok:true,state:s,raw}:{ok:false,error:"Der lokale Entwurf ist beschädigt und wird nicht überschrieben."};}
 catch(_){return {ok:false,error:"Der lokale Entwurf kann nicht sicher gelesen werden."};}
}
function fingerprint(e){return [e.bank,e.courseId,e.question.normalize("NFKC").toLocaleLowerCase("de").replace(/\s+/g," ").trim()].join("|");}
function actorValid(a){return record(a)&&id(a.id)&&a.active===true&&ROLES.has(a.role)&&Array.isArray(a.courseIds)&&a.courseIds.every(id);}
function courseAllowed(a,c){return a.role==="admin"||a.courseIds.includes(c);}
function can(a,action,courseId){
 if(!actorValid(a))return false;
 if(action==="courses"||action==="sources"||action==="approve"||action==="publish"||action==="archive-course")return a.role==="admin";
 if(action==="list")return a.role!=="participant";
 if(action==="view-published")return courseAllowed(a,courseId);
 return ["edit","review","archive","export"].includes(action)&&a.role!=="participant"&&courseAllowed(a,courseId);
}
function createRepository({storage,lock,utcNow=()=>new Date().toISOString()}={}){
 return {
  read:()=>read(storage),
  async change(revision,actor,action,entityId,mutate){
   need(typeof lock==="function","Sicheres lokales Speichern ist in diesem Browser nicht verfügbar.");
   return lock(async()=>{
    const old=read(storage);need(old.ok,old.error);need(old.state.revision===revision,"Der Entwurf wurde inzwischen in einem anderen Fenster geändert. Bitte neu laden; die Eingabe bleibt erhalten.");
    const next=clone(old.state);mutate(next);next.revision++;const utc=utcNow();need(Number.isFinite(Date.parse(utc)),"Ungültige Zeitquelle.");
    next.audit.push({revision:next.revision,actorId:actor.id,action,entityId,utc});next.audit=next.audit.slice(-1000);
    need(valid(next),"Der Entwurf enthält ungültige Daten.");
    const raw=JSON.stringify(next);need(storage.getItem(KEY)===old.raw,"Der Entwurf wurde inzwischen geändert. Bitte neu laden.");
    try{storage.setItem(KEY,raw);need(storage.getItem(KEY)===raw,"Speichern wurde nicht bestätigt.");}
    catch(_){fail("Der Entwurf wurde nicht sicher gespeichert. Die Eingabe bleibt erhalten.");}
    return clone(next);
   });
  }
 };
}
function createService({repository,resolveActor,baseline=[]}={}){
 async function actor(action,courseId){const a=typeof resolveActor==="function"?await resolveActor():null;need(can(a,action,courseId),"Kein berechtigter Redaktionszugang für diese Aktion.");return a;}
 function current(){const r=repository.read();need(r.ok,r.error);return r.state;}
 const exists=(s,courseId)=>{const c=s.courses.find(x=>x.id===courseId);need(c&&c.status==="active","Der Kurs ist nicht aktiv.");return c;};
 function noDuplicate(s,e,except){
  const fp=fingerprint(e);need(!s.entries.some(x=>x.id!==except&&x.status!=="archived"&&fingerprint(x)===fp)&&!baseline.some(x=>x.id!==except&&BANKS.has(x.bank)&&fingerprint({...x,courseId:e.courseId})===fp),"Dieser Inhalt ist bereits vorhanden. Dublette zuerst prüfen.");
 }
 async function write(action,courseId,revision,entityId,fn){const a=await actor(action,courseId);return repository.change(revision,a,action,entityId,s=>{if(a.role==="instructor")need(s.courses.some(c=>c.id===courseId&&c.instructorIds.includes(a.id)),"Keine Dozentenzuordnung für diesen Kurs.");fn(s,a);});}
 return Object.freeze({
  async list(){const a=await actor("list"),s=current();const courses=s.courses.filter(c=>courseAllowed(a,c.id)&&(a.role!=="instructor"||c.instructorIds.includes(a.id))),ids=new Set(courses.map(c=>c.id)),entries=s.entries.filter(e=>ids.has(e.courseId)),sourceIds=new Set(entries.map(e=>e.sourceId)),entityIds=new Set([...ids,...entries.map(e=>e.id)]);return clone({...s,courses,entries,sources:a.role==="admin"?s.sources:s.sources.filter(x=>sourceIds.has(x.id)),audit:a.role==="admin"?s.audit:s.audit.filter(x=>x.actorId===a.id||entityIds.has(x.entityId))});},
  async saveCourse(value,revision){return write("courses",null,revision,value.id,s=>{need(courseValid(value),"Kursname, eindeutige ID und gültiger Zeitraum sind erforderlich.");const old=s.courses.find(c=>c.id===value.id);if(old)Object.assign(old,clone(value));else s.courses.push(clone(value));});},
  async saveSource(value,revision){return write("sources",null,revision,value.id,s=>{need(sourceValid(value),"Quelle und eindeutige ID vollständig ausfüllen.");const old=s.sources.find(x=>x.id===value.id);if(old){Object.assign(old,clone(value));for(const e of s.entries.filter(x=>x.sourceId===old.id)){if(e.status!=="archived")e.status="draft";e.review=null;e.approval=null;e.version++;}}else s.sources.push(clone(value));});},
  async saveEntry(value,revision){return write("edit",value.courseId,revision,value.id,(s,a)=>{exists(s,value.courseId);need(questionValid(value),"Frage, Banktyp, Quelle, Kategorie und passende Antworten vollständig ausfüllen.");need(s.sources.some(x=>x.id===value.sourceId),"Die Quelle fehlt.");const old=s.entries.find(e=>e.id===value.id);need(!old||old.courseId===value.courseId&&old.bank===value.bank,"Banktyp und Kurs bestehender Inhalte bleiben getrennt.");need(!old||value.version===old.version,"Dieser Inhalt wurde inzwischen geändert. Bitte den aktuellen Inhalt erneut auswählen.");noDuplicate(s,value,value.id);const e={...clone(value),status:"draft",version:old?old.version+1:1,review:null,approval:null,createdBy:old?.createdBy||a.id};if(old)s.entries[s.entries.indexOf(old)]=e;else s.entries.push(e);});},
  async transition(entryId,target,review,revision){
   const snap=current(),entry=snap.entries.find(e=>e.id===entryId);need(entry,"Inhalt nicht gefunden.");
   const action={review:"review",approved:"approve",published:"publish",archived:"archive"}[target];need(action,"Ungültiger Review-Schritt.");
   return write(action,entry.courseId,revision,entryId,(s,a)=>{
    const e=s.entries.find(x=>x.id===entryId);exists(s,e.courseId);const src=s.sources.find(x=>x.id===e.sourceId);
    if(target==="review"){need(e.status==="draft","Nur ein Entwurf kann geprüft werden.");need(record(review)&&CHECKS.every(k=>review.checks?.[k]===true)&&day(review.day),"Alle sieben Review-Punkte und das Prüfdatum bestätigen.");e.review={actorId:a.id,day:review.day,checks:clone(review.checks)};e.approval=null;}
    else if(target==="approved"){need(e.status==="review"&&e.review&&CHECKS.every(k=>e.review.checks?.[k]===true)&&e.review.actorId!==a.id,"Freigabe erfordert eine unabhängige zweite prüfende Person.");need(src.ownerReviewed===true&&src.usage==="own","Nutzungsrechte und eigene Formulierung müssen geprüft sein.");e.approval={actorId:a.id};}
    else if(target==="published"){need(e.status==="approved"&&e.review&&CHECKS.every(k=>e.review.checks?.[k]===true)&&e.approval&&e.approval.actorId!==e.review.actorId,"Erst vollständig freigegebene Inhalte können veröffentlicht werden.");need(src.ownerReviewed===true&&src.usage==="own","Quellenfreigabe fehlt.");noDuplicate(s,e,e.id);}
    else need(e.status!=="archived","Der Inhalt ist bereits archiviert.");
    e.status=target;e.version++;
   });
  },
  async published(courseId,today){
   const a=await actor("view-published",courseId),s=current();need(day(today),"Gültiges Tagesdatum erforderlich.");const c=exists(s,courseId);need(a.role!=="instructor"||c.instructorIds.includes(a.id),"Keine Dozentenzuordnung für diesen Kurs.");need(today>=c.startDay&&today<=c.endDay,"Der Kurs liegt außerhalb des Zugangszeitraums.");
   return clone(s.entries.filter(e=>e.courseId===courseId&&e.status==="published"&&e.review&&CHECKS.every(k=>e.review.checks?.[k]===true)&&e.approval&&e.approval.actorId!==e.review.actorId&&s.sources.some(x=>x.id===e.sourceId&&x.ownerReviewed&&x.usage==="own"))).map(e=>({id:e.id,bank:e.bank,category:e.category,question:e.question,answers:e.answers,correct:e.correct,points:e.points,explanation:e.explanation,modelAnswer:e.modelAnswer,followUps:e.followUps,criticalMistakes:e.criticalMistakes,back:e.back,version:e.version}));
  },
  async importDrafts(input,revision){
   need(typeof input==="string"&&new TextEncoder().encode(input).length<=500000,"Import auf höchstens 500 KB begrenzen.");let batch;try{batch=JSON.parse(input);}catch(_){fail("Die Importdatei ist kein gültiges JSON.");}
   need(record(batch)&&batch.schema===1&&Array.isArray(batch.entries)&&batch.entries.length>0&&batch.entries.length<=100,"Ein Import enthält 1 bis100 Entwürfe im Schema1.");
   const a=await actor("edit",null);need(a.role==="admin","Nur die lokale Administration darf einen gemischten Import prüfen.");
   return repository.change(revision,a,"import","batch",s=>{
    for(const value of batch.entries){need(record(value)&&(!value.status||value.status==="draft")&&!value.review&&!value.approval,"Import darf keine Freigabe oder Veröffentlichung mitbringen.");need(questionValid(value),"Ungültiger Inhalt im Import.");exists(s,value.courseId);need(s.sources.some(x=>x.id===value.sourceId)&&!s.entries.some(x=>x.id===value.id),"Quelle fehlt oder Import-ID bereits vorhanden.");noDuplicate(s,value);s.entries.push({...clone(value),status:"draft",version:1,review:null,approval:null,createdBy:a.id});}
   });
  },
  async exportDrafts(courseId){await actor("export",courseId);const s=current();return JSON.stringify({schema:1,courseId,entries:s.entries.filter(e=>e.courseId===courseId).map(e=>({...clone(e),status:"draft",review:null,approval:null})),publicationAuthority:false},null,2);}
 });
}
const api=Object.freeze({KEY,CATEGORIES,CHECKS,empty,valid,read,can,questionValid,createRepository,createService});
if(mod)mod.exports=api;if(root)root.ACCAOUI_CONTENT_WORKSPACE_V1=api;
})(typeof window!=="undefined"?window:null,typeof module!=="undefined"?module:null);
