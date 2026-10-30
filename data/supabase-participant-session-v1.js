/* Explicit participant session/cache boundary. Never patches native Storage or creates a client. */
(function(root,common){
"use strict";
function create(deps){
 const {model,createAuthAdapter,createAccessAdapter,client,cache,tabStorage,locks,now,newId,setTimer,clearTimer}=deps||{};
 function fail(code){const e=new Error(code);e.name="ParticipantSessionError";e.code=code;throw e;}
 function need(ok,code){if(!ok)fail(code);}
 need(model&&typeof model.restore==="function"&&typeof createAuthAdapter==="function"&&typeof createAccessAdapter==="function","invalid_dependencies");
 need(client?.auth&&typeof client.auth.getSession==="function"&&typeof client.auth.signInWithPassword==="function"&&typeof client.auth.signOut==="function"&&typeof client.auth.onAuthStateChange==="function"&&typeof client.from==="function","invalid_client");
 need([cache,tabStorage].every(s=>s&&["getItem","setItem"].every(k=>typeof s[k]==="function"))&&typeof locks?.request==="function"&&[now,newId,setTimer,clearTimer].every(f=>typeof f==="function"),"durable_storage_required");
 const service=model.createService(client),listeners=new Set();
 const auth=createAuthAdapter({auth:{getSession:()=>client.auth.getSession(),signInWithPassword:x=>client.auth.signInWithPassword(x),signOut:()=>client.auth.signOut({scope:"local"})}});
 const uuid=x=>typeof x==="string"&&/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(x);
 let phase="idle",code=null,owner=null,course=null,courses=[],state=null,rawRecovery=null,cacheKey=null,pointerKey=null,release=null;
 let durable=true,epoch=0,expires=0,accessLimit=0,timer=null,leaseTimer=null,flight=null,opening=null,disposed=false;
 function status(){return Object.freeze({phase,code,ownerId:owner,courseId:course,courses:Object.freeze(courses.map(x=>Object.freeze({...x}))),durable,pending:!!state?.pending,dirty:state?model.dirty(state):false,syncInProgress:flight!==null,version:state?.base.version??null,remoteVersion:state?.remote?.version??null});}
 function emit(){const value=status();for(const fn of listeners){try{fn(value);}catch{ /* A UI listener cannot change stored progress. */ }}}
 function cancelTimers(){if(timer!==null)clearTimer(timer);if(leaseTimer!==null)clearTimer(leaseTimer);timer=leaseTimer=null;}
 function lock(reason){epoch++;phase="locked";code=reason;cancelTimers();emit();}
 function live(){
  need(!disposed&&phase==="ready"&&state!==null&&release!==null,"session_locked");
  if(!Number.isFinite(now())||now()>=expires){lock("session_expired");fail("session_expired");}
 }
 function persist(next){
  state=next;const raw=model.serialize(next);
  try{cache.setItem(cacheKey,raw);need(cache.getItem(cacheKey)===raw,"cache_unconfirmed");durable=true;rawRecovery=null;}
  catch{durable=false;code="cache_unavailable";emit();fail("cache_unavailable");}
  emit();
 }
 function schedule(){if(timer!==null||disposed||phase!=="ready")return;timer=setTimer(()=>{timer=null;flush().catch(()=>{});},250);}
 async function reserve(id){
  let held=false,finish;
  const available=new Promise(resolve=>{finish=resolve;});
  const request=locks.request("accaoui-progress-v1:"+owner+":"+course+":"+id,{mode:"exclusive",ifAvailable:true},async lockValue=>{
   if(!lockValue||disposed){finish(false);return;}
   const lifetime=new Promise(resolve=>{release=resolve;});held=true;finish(true);await lifetime;
  });
  Promise.resolve(request).catch(()=>{if(!held)finish(false);else lock("cache_lock_lost");});
  return available;
 }
 function scopedAccess(id){
  const views={participants:"accaoui_progress_participant_v1",enrollments:"accaoui_progress_enrollment_v1",courses:"accaoui_progress_course_v1"};
  const limits={courseEnd:Infinity};
  const boundary={auth:client.auth,from(table){
   need(Object.hasOwn(views,table),"invalid_access_query");
   return {select(columns){return {async eq(column,value){
    let query=client.from(views[table]).select(columns).eq(column,value);
    if(table==="enrollments")query=query.eq("course_id",id);
    const response=await query; // Actual SDK request and unchanged response; no fabricated rows.
    if(table==="courses"&&response?.error===null&&Array.isArray(response.data)&&response.data.length===1){
     const end=response.data[0].end_date;
     if(end!==null){need(typeof end==="string"&&/^\d{4}-\d{2}-\d{2}$/.test(end),"access_invalid");limits.courseEnd=Date.parse(end+"T00:00:00Z")+86400000;}
    }
    return response;
   }};}};
  }};
  return {adapter:createAccessAdapter({client:boundary,utcNow:()=>new Date(now())}),limits};
 }
 async function resolveSession(){
  need(!disposed&&state===null,"reload_required");phase="authenticating";code=null;emit();
  try{
   const r=await auth.resolveSession();
   if(r.ok!==true){phase="login";code=r.code;emit();return status();}
   const context=await service.context();owner=context.ownerId;courses=context.courses.map(x=>({...x}));
   phase="choose_course";code=courses.length?null:"no_active_course";emit();return status();
  }catch(e){phase="login";code=e.code||"auth_unavailable";emit();throw e;}
 }
 async function signIn(credentials){
  need(!disposed&&state===null,"reload_required");
  const r=await auth.signIn(credentials);need(r.ok===true,r.code||"sign_in_failed");return resolveSession();
 }
 async function open(id){
  if(opening)return opening;
  need(!disposed&&phase==="choose_course"&&state===null&&release===null,"reload_required");
  need(uuid(id)&&courses.some(c=>c.id===id),"course_not_available");course=id;
  const initialEpoch=epoch;
  opening=(async()=>{
   phase="loading";code=null;emit();
   try{
    const access=scopedAccess(id),decision=await access.adapter.resolveAccess();
    need(decision.allowed===true&&decision.courseId===id,"access_denied");
    const current=await service.read(id);need(current.ownerId===owner,"account_changed");
    const response=await client.auth.getSession(),session=response?.data?.session;
    need(response?.error===null&&session?.user?.id===owner&&Number.isFinite(session.expires_at),"session_invalid");
    accessLimit=Math.min(decision.accessEndsAt?Date.parse(decision.accessEndsAt):Infinity,access.limits.courseEnd);expires=Math.min(session.expires_at*1000,accessLimit);
    need(Number.isFinite(expires)&&now()<expires,"session_expired");need(initialEpoch===epoch&&!disposed,"session_changed");
    pointerKey="accaoui_progress_tab_v1:"+owner+":"+course;
    let cacheId=tabStorage.getItem(pointerKey);if(!uuid(cacheId))cacheId=newId();need(uuid(cacheId),"invalid_cache_identity");
    if(!await reserve(cacheId)){cacheId=newId();need(uuid(cacheId)&&await reserve(cacheId),"cache_in_use");}
    need(initialEpoch===epoch&&!disposed,"session_changed");
    tabStorage.setItem(pointerKey,cacheId);need(tabStorage.getItem(pointerKey)===cacheId,"cache_unconfirmed");
    cacheKey="accaoui_progress_cache_v1:"+owner+":"+course+":"+cacheId;
    const saved=cache.getItem(cacheKey);
    if(saved===null)state=current;
    else{
     rawRecovery=saved;state=model.restore(saved,{ownerId:owner,courseId:course});
     need(current.base.version>=state.base.version,"server_version_regressed");
     if(current.base.version===state.base.version)need(JSON.stringify(current.base.document)===JSON.stringify(state.base.document),"server_version_mismatch");
     if(!model.dirty(state)&&state.phase==="ready")state=current;
    }
    phase="ready";persist(state);code=state.phase==="conflict"?"conflict":null;
    leaseTimer=setTimer(()=>lock("session_expired"),Math.min(2147483647,Math.max(1,expires-now())));
    if(model.dirty(state)&&state.phase!=="conflict")schedule();emit();return status();
   }catch(e){
    if(phase!=="locked"){phase=rawRecovery!==null?"recovery_required":"locked";code=e.code||"access_unavailable";}
    emit();throw e;
   }
  })();
  try{return await opening;}finally{opening=null;}
 }
 function storage(){
  live();const generation=epoch,scope=owner+":"+course;
  const check=()=>{live();need(epoch===generation&&owner+":"+course===scope,"session_changed");};
  const key=k=>need(model.KEYS.includes(k),"unapproved_progress_key");
  return Object.freeze({getItem(k){check();key(k);return state.document.values[k]??null;},setItem(k,value){check();key(k);persist(model.edit(state,k,String(value)));schedule();},removeItem(k){check();key(k);persist(model.edit(state,k,null));schedule();}});
 }
 async function flush(){
  if(flight)return flight;
  live();const generation=epoch;
  flight=Promise.resolve().then(async()=>{
   try{
    if(!durable)persist(state);
    if(state.phase==="conflict"){code="conflict";emit();return status();}
    if(!model.dirty(state)){code=null;emit();return status();}
    persist(model.begin(state,newId()));const sent=state;
    const reply=await service.commit(sent);live();need(epoch===generation,"session_changed");
    persist(model.acknowledge(state,reply));code=state.phase==="conflict"?"conflict":null;
    if(model.dirty(state)&&state.phase!=="conflict")schedule();emit();return status();
   }catch(e){
    if(["auth_required","account_changed","access_denied"].includes(e.code))lock(e.code);
    else if(phase==="ready"){code=e.code||"sync_unavailable";emit();}
    throw e;
   }finally{flight=null;emit();}
  });
  return flight;
 }
 function resolveConflict(choice){live();need(!flight,"sync_in_progress");persist(model.resolve(state,choice));code=null;if(model.dirty(state))schedule();emit();return status();}
 async function refresh(){
  live();need(!flight&&!model.dirty(state)&&state.phase==="ready","pending_input_requires_sync");
  const generation=epoch,current=await service.read(course);live();need(generation===epoch&&current.ownerId===owner,"account_changed");
  need(current.base.version>=state.base.version,"server_version_regressed");persist(current);code=null;emit();return status();
 }
 function importAnonymous(choice){
  live();need(choice==="replace_account_with_anonymous_copy","explicit_import_required");need(!flight&&state.pending===null&&state.phase==="ready","pending_input_requires_sync");
  const values={};for(const key of model.KEYS){const value=cache.getItem(key);if(value!==null)values[key]=value;}
  const document=model.document({schema:1,values});let next=state;
  for(const key of model.KEYS)next=model.edit(next,key,document.values[key]??null);
  persist(next);schedule();return status(); // Anonymous originals are never changed or removed.
 }
 function backup(){need(!disposed&&owner!==null&&now()<expires&&["ready","recovery_required"].includes(phase)&&code!=="cache_scope_mismatch","session_locked");return state?model.serialize(state):rawRecovery;}
 async function useServerCopy(confirmation){
  need(!disposed&&phase==="recovery_required"&&confirmation==="new_cache_preserve_previous_bytes"&&pointerKey!==null,"explicit_recovery_required");
  need(now()<expires,"session_expired");const generation=epoch;
  const current=await service.read(course);need(current.ownerId===owner&&generation===epoch&&!disposed,"account_changed");
  const previous={state,rawRecovery,cacheKey,release,durable};const id=newId();need(uuid(id),"invalid_cache_identity");
  const target="accaoui_progress_cache_v1:"+owner+":"+course+":"+id;
  need(cache.getItem(target)===null,"cache_identity_collision");
  try{
   need(await reserve(id),"cache_in_use");need(generation===epoch&&!disposed,"session_changed");
   const raw=model.serialize(current);cache.setItem(target,raw);need(cache.getItem(target)===raw,"cache_unconfirmed");
   tabStorage.setItem(pointerKey,id);need(tabStorage.getItem(pointerKey)===id,"cache_unconfirmed");
   state=current;cacheKey=target;rawRecovery=null;durable=true;phase="ready";code=null;
   if(previous.release)previous.release();
   leaseTimer=setTimer(()=>lock("session_expired"),Math.min(2147483647,Math.max(1,expires-now())));
   emit();return status();
  }catch(e){
   if(release!==previous.release&&release)release();
   state=previous.state;rawRecovery=previous.rawRecovery;cacheKey=previous.cacheKey;release=previous.release;durable=previous.durable;
   if(!disposed&&generation===epoch){phase="recovery_required";code=e.code||"recovery_unavailable";}emit();throw e;
  }
 }
 function quiesce(){live();persist(state);lock("reloading");return status();}
 async function signOut(){
  need(!disposed,"session_locked");if(state!==null)persist(state);
  lock("signing_out");const result=await auth.signOut();
  if(result.ok!==true){code=result.code||"sign_out_failed";emit();fail(code);}
  code="signed_out";emit();return status();
 }
 const authListener=client.auth.onAuthStateChange((_event,session)=>{
  if(owner!==null&&(!session||session.user?.id!==owner))lock("account_changed");
  else if(owner!==null&&phase==="ready"&&Number.isFinite(session?.expires_at)){
   expires=Math.min(session.expires_at*1000,accessLimit);
   if(leaseTimer!==null)clearTimer(leaseTimer);leaseTimer=setTimer(()=>lock("session_expired"),Math.min(2147483647,Math.max(1,expires-now())));
  }
 });
 function dispose(){if(disposed)return;disposed=true;epoch++;phase="closed";cancelTimers();if(release){release();release=null;}authListener?.data?.subscription?.unsubscribe();listeners.clear();}
 return Object.freeze({resolveSession,signIn,open,storage,flush,refresh,resolveConflict,importAnonymous,backup,useServerCopy,quiesce,signOut,status,subscribe(fn){need(typeof fn==="function","invalid_listener");listeners.add(fn);return()=>listeners.delete(fn);},dispose});
}
const api=Object.freeze({create});if(common?.exports)common.exports=api;
if(root&&root.ACCAOUI_PARTICIPANT_SESSION_FACTORY_V1===undefined)Object.defineProperty(root,"ACCAOUI_PARTICIPANT_SESSION_FACTORY_V1",{value:api,enumerable:true,writable:false,configurable:false});
})(typeof window!=="undefined"?window:null,typeof module!=="undefined"?module:null);
