/* Local W04 calendar, review and daily-plan rules. No network or client creation. */
(function (root, common) {
"use strict";
const KEY = "accaoui_learning_guidance_v1";
const INTERVALS = Object.freeze([1, 3, 7, 14, 30]);
const record = x => x !== null && typeof x === "object" && !Array.isArray(x);
const count = x => Number.isInteger(x) && x >= 0 && x <= 1000000;
function ordinal(value) {
  if (typeof value !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return null;
  const y=Number(value.slice(0,4)),m=Number(value.slice(5,7)),d=Number(value.slice(8));
  if(y<1 || m<1 || m>12 || d<1 || d>31)return null;
  const date=new Date(0);date.setUTCFullYear(y,m-1,d);date.setUTCHours(0,0,0,0);
  return date.getUTCFullYear()===y && date.getUTCMonth()===m-1 && date.getUTCDate()===d ? date.getTime()/86400000 : null;
}
function day(now=new Date()) {
  if (!(now instanceof Date) || !Number.isFinite(now.getTime()) || now.getFullYear()<1 || now.getFullYear()>9999) throw Error("invalid calendar clock");
  return String(now.getFullYear()).padStart(4,"0")+"-"+String(now.getMonth()+1).padStart(2,"0")+"-"+String(now.getDate()).padStart(2,"0");
}
function addDays(value, amount) {
  const n=ordinal(value);
  if(n===null || !Number.isInteger(amount))return null;
  const date=new Date((n+amount)*86400000);
  if(date.getUTCFullYear()<1 || date.getUTCFullYear()>9999)return null;
  return String(date.getUTCFullYear()).padStart(4,"0")+"-"+String(date.getUTCMonth()+1).padStart(2,"0")+"-"+String(date.getUTCDate()).padStart(2,"0");
}
function validReview(value,today) {
  return record(value) && value.schema===1 && Number.isInteger(value.stage) && value.stage>=0 && value.stage<=5 &&
    ordinal(value.reviewedDay)!==null && value.reviewedDay<=today &&
    value.dueDay===addDays(value.reviewedDay,INTERVALS[Math.max(0,value.stage-1)]);
}
function reviewOf(entry, now=new Date()) {
  const today=day(now);
  if(!record(entry) || !["known","unknown"].includes(entry.lastStatus))return null;
  if(validReview(entry.review,today) && (entry.lastStatus==="unknown" ? entry.review.stage===0 : entry.review.stage>0))return {...entry.review,legacy:false};
  // Old ratings have no spaced-review history: at most one day, never infer mastery from their count.
  const previous=typeof entry.updatedAt==="string" ? new Date(entry.updatedAt) : null;
  let reviewed=today,dated=false;
  if(previous && Number.isFinite(previous.getTime())) {
    const candidate=day(previous);if(candidate<=today){reviewed=candidate;dated=true;}
  }
  return {schema:1,stage:0,reviewedDay:reviewed,dueDay:entry.review || !dated ? today : (addDays(reviewed,1)||today),legacy:true};
}
function nextReview(entry,status,now=new Date()) {
  if(!["known","unknown"].includes(status))throw Error("invalid card rating");
  const today=day(now),old=reviewOf(entry,now);
  let stage=0;
  if(status==="known" && old && !old.legacy && old.stage>0 && old.dueDay>today)return {schema:1,stage:old.stage,reviewedDay:old.reviewedDay,dueDay:old.dueDay};
  if(status==="known") {
    stage=old && !old.legacy ? old.stage : 0;
    if(!old || old.legacy || stage===0 || (old.reviewedDay<today && old.dueDay<=today))stage=Math.min(5,stage+1);
  }
  return {schema:1,stage,reviewedDay:today,dueDay:addDays(today,INTERVALS[Math.max(0,stage-1)])||today};
}
function dueKeys(store, keys, now=new Date()) {
  if(!record(store) || !Array.isArray(keys))return [];
  const today=day(now),seen=new Set();
  return keys.filter(key=>{
    if(typeof key!=="string" || seen.has(key))return false;
    seen.add(key);
    if(!Object.prototype.hasOwnProperty.call(store,key))return false;
    const review=reviewOf(store[key],now);
    return review!==null && review.dueDay<=today;
  });
}
function defaults() {
  return {schema:1,revision:0,preferences:{minutes:20,pausedUntil:null,reminders:false,reminderTime:"18:00"},daily:{day:null,answers:0,correct:0,cardRatings:0}};
}
function validPreferences(p) {
  return record(p) && Number.isInteger(p.minutes) && p.minutes>=10 && p.minutes<=120 &&
    (p.pausedUntil===null || ordinal(p.pausedUntil)!==null) && typeof p.reminders==="boolean" &&
    typeof p.reminderTime==="string" && /^([01]\d|2[0-3]):[0-5]\d$/.test(p.reminderTime);
}
function validState(s) {
  return record(s) && s.schema===1 && count(s.revision) && validPreferences(s.preferences) &&
    record(s.daily) && (s.daily.day===null || ordinal(s.daily.day)!==null) &&
    count(s.daily.answers) && count(s.daily.correct) && s.daily.correct<=s.daily.answers && count(s.daily.cardRatings);
}
function readState(storage) {
  try {
    const raw=storage.getItem(KEY);
    if(raw===null)return {ok:true,state:defaults(),empty:true};
    const state=JSON.parse(raw);
    return validState(state) ? {ok:true,state,empty:false} : {ok:false,code:"invalid_saved_plan"};
  } catch(_error) { return {ok:false,code:"unreadable_saved_plan"}; }
}
function changeState(storage, update) {
  const read=readState(storage);if(!read.ok)return read;
  const state=JSON.parse(JSON.stringify(read.state));
  try {
    update(state);state.revision++;
    if(!validState(state))return {ok:false,code:"invalid_plan_input"};
    const raw=JSON.stringify(state);
    storage.setItem(KEY,raw);
    if(storage.getItem(KEY)!==raw)return {ok:false,code:"unconfirmed_plan_write"};
    return {ok:true,state};
  } catch(_error) {return {ok:false,code:"plan_not_saved"};}
}
function savePreferences(storage, preferences) {
  if(!validPreferences(preferences))return {ok:false,code:"invalid_plan_input"};
  return changeState(storage,s=>{s.preferences={...preferences};});
}
function activity(storage, kind, amount, correct, now=new Date()) {
  if(!["written","card"].includes(kind) || !count(amount) || !count(correct) || correct>amount || (kind==="card" && correct!==0))return {ok:false,code:"invalid_activity"};
  const today=day(now);
  return changeState(storage,s=>{
    if(s.daily.day!==today)s.daily={day:today,answers:0,correct:0,cardRatings:0};
    if(kind==="written"){s.daily.answers+=amount;s.daily.correct+=correct;}
    else s.daily.cardRatings+=amount;
  });
}
function reset(storage) {
  try {storage.removeItem(KEY);return storage.getItem(KEY)===null ? {ok:true,state:defaults()} : {ok:false,code:"unconfirmed_plan_delete"};}
  catch(_error){return {ok:false,code:"plan_not_deleted"};}
}
function buildPlan(preferences, deadlines=[], now=new Date()) {
  if(!validPreferences(preferences))throw Error("invalid preferences");
  const today=day(now),n=ordinal(today);
  const next=deadlines.filter(x=>ordinal(x)!==null && ordinal(x)>=n).sort()[0]||null;
  const days=next===null?null:ordinal(next)-n;
  const paused=preferences.pausedUntil!==null && preferences.pausedUntil>=today;
  const blocks=[];
  if(!paused) {
    let left=preferences.minutes,index=0;
    while(left>0) {
      const minutes=preferences.minutes<=25 && preferences.minutes>=20 && index===0 ? Math.ceil(left/2) : Math.min(left,25);
      blocks.push({kind:index%2===0?"next":"recall",minutes});
      left-=minutes;index++;
      if(left>0 && minutes===25)blocks.push({kind:"break",minutes:5});
    }
  }
  const minute=String(now.getHours()).padStart(2,"0")+":"+String(now.getMinutes()).padStart(2,"0");
  return {today,deadline:next,days,paused,blocks,studyMinutes:paused?0:preferences.minutes,breakMinutes:blocks.filter(b=>b.kind==="break").reduce((a,b)=>a+b.minutes,0),reviewPriority:days!==null && days<=3,reminder:!paused && preferences.reminders && minute>=preferences.reminderTime};
}
const api=Object.freeze({KEY,INTERVALS,ordinal,day,addDays,reviewOf,nextReview,dueKeys,defaults,validPreferences,validState,readState,savePreferences,activity,reset,buildPlan});
if(common)common.exports=api;
if(root && root.ACCAOUI_LEARNING_GUIDANCE_V1===undefined)Object.defineProperty(root,"ACCAOUI_LEARNING_GUIDANCE_V1",{value:api,writable:false,configurable:false});
})(typeof window!=="undefined"?window:null,typeof module!=="undefined"?module:null);
