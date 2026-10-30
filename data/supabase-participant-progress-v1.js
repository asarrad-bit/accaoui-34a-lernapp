/* W03 scoped progress model and real-client RPC boundary. No client creation or live switch. */
(function(root,common){
"use strict";
const UUID=/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i,MAX=Number.MAX_SAFE_INTEGER;
const KEYS=Object.freeze(["accaoui_exam_history","accaoui_topic_stats","accaoui_topic_mistakes","accaoui_answered_questions","accaoui_active_session","accaoui_active_learning_session","accaoui_flashcard_progress","accaoui_active_flashcard_session","accaoui_oral_exam_mistakes_v2324","accaoui_exam_date_written_v1","accaoui_exam_date_oral_v1","accaoui_learning_guidance_v1"]);
const arrays=new Set(["accaoui_exam_history","accaoui_oral_exam_mistakes_v2324"]);
const dates=new Set(["accaoui_exam_date_written_v1","accaoui_exam_date_oral_v1"]);
// Only records created and deeply frozen by this module are trusted again.
// Restored, SDK, cloned and caller-created objects still pass the full validators.
const ownedDocuments=new WeakSet(),ownedStates=new WeakSet(),documentEncoding=new WeakMap(),lastValidRaw=new Map();
const plain=x=>x!==null&&typeof x==="object"&&!Array.isArray(x)&&Object.getPrototypeOf(x)===Object.prototype;
function fail(code){const e=new Error(code);e.name="ParticipantProgressError";e.code=code;throw e;}
function need(ok,code){if(!ok)fail(code);}
function uuid(x){need(typeof x==="string"&&UUID.test(x),"invalid_scope");return x.toLowerCase();}
function version(x){need(Number.isSafeInteger(x)&&x>=0,"invalid_version");return x;}
function bytes(x){return new TextEncoder().encode(x).length;}
function freeze(x){if(x&&typeof x==="object"){Object.values(x).forEach(freeze);Object.freeze(x);}return x;}
const clone=x=>JSON.parse(JSON.stringify(x));
function safe(x,depth=0){
 if(depth>12)return false;
 if(x===null||typeof x==="boolean")return true;
 if(typeof x==="number")return Number.isFinite(x)&&Math.abs(x)<=MAX;
 if(typeof x==="string")return bytes(x)<=262144;
 if(Array.isArray(x))return x.length<=2000&&x.every(v=>safe(v,depth+1));
 return plain(x)&&Object.keys(x).length<=2000&&Object.entries(x).every(([k,v])=>k.length<=200&&!["__proto__","constructor","prototype"].includes(k)&&safe(v,depth+1));
}
function document(value){
 if(value&&typeof value==="object"&&ownedDocuments.has(value))return value;
 need(plain(value)&&Object.keys(value).length===2&&value.schema===1&&plain(value.values),"invalid_document");
 const values={};
 for(const key of Object.keys(value.values).sort()){
  const raw=value.values[key];need(KEYS.includes(key)&&typeof raw==="string"&&bytes(raw)<=262144,"invalid_document");
  if(lastValidRaw.get(key)===raw){values[key]=raw;continue;}
  if(dates.has(key)){
   need(/^\d{4}-\d{2}-\d{2}$/.test(raw)&&Number(raw.slice(0,4))>=1,"invalid_document");const d=new Date(raw+"T00:00:00Z");
   need(Number.isFinite(d.getTime())&&d.toISOString().slice(0,10)===raw,"invalid_document");
  }else{
   let parsed;try{parsed=JSON.parse(raw);}catch{fail("invalid_document");}
   need((arrays.has(key)?Array.isArray(parsed):plain(parsed))&&safe(parsed),"invalid_document");
  }
  lastValidRaw.set(key,raw);values[key]=raw;
 }
 const result={schema:1,values},encoded=JSON.stringify(result);need(bytes(encoded)<=1048576,"invalid_document");freeze(result);ownedDocuments.add(result);documentEncoding.set(result,encoded);return result;
}
const empty=()=>document({schema:1,values:{}});
const equal=(a,b)=>documentEncoding.get(document(a))===documentEncoding.get(document(b));
function snapshot(x){need(plain(x),"invalid_response");return freeze({version:version(x.version),document:document(x.document)});}
function state(value){
 if(value&&typeof value==="object"&&ownedStates.has(value))return value;
 need(plain(value)&&Object.keys(value).sort().join(",")==="base,courseId,document,ownerId,pending,phase,remote,schema"&&value.schema===1,"invalid_state");
 need(plain(value.base)&&Object.keys(value.base).sort().join(",")==="document,version","invalid_state");
 const ownerId=uuid(value.ownerId),courseId=uuid(value.courseId),base=snapshot(value.base),doc=document(value.document);
 need(["ready","conflict"].includes(value.phase),"invalid_state");
 let pending=null,remote=null;
 if(value.pending!==null){
  const p=value.pending;need(plain(p)&&Object.keys(p).sort().join(",")==="document,expectedVersion,id","invalid_state");
  pending={id:uuid(p.id),expectedVersion:version(p.expectedVersion),document:document(p.document)};
  need(pending.expectedVersion===base.version&&pending.expectedVersion<MAX,"invalid_state");
 }
 if(value.remote!==null){need(plain(value.remote)&&Object.keys(value.remote).sort().join(",")==="document,version","invalid_state");remote=snapshot(value.remote);}
 need((value.phase==="conflict")===(remote!==null),"invalid_state");
 const result=freeze({schema:1,ownerId,courseId,base,document:doc,pending,remote,phase:value.phase});ownedStates.add(result);return result;
}
function create(scope,initial){
 need(plain(scope),"invalid_scope");const base=snapshot(initial);
 return state({schema:1,ownerId:uuid(scope.ownerId),courseId:uuid(scope.courseId),base,document:base.document,pending:null,remote:null,phase:"ready"});
}
function edit(input,key,raw){
 const s=state(input);need(KEYS.includes(key),"invalid_key");
 const values={...s.document.values};
 if(raw===null)delete values[key];else{need(typeof raw==="string","invalid_document");values[key]=raw;}
 return state({...s,document:document({schema:1,values})});
}
function dirty(input){const s=state(input);return !equal(s.document,s.base.document)||s.pending!==null;}
function begin(input,id){
 const s=state(input);need(s.phase==="ready","conflict_requires_explicit_resolution");
 if(s.pending!==null)return s;
 if(!dirty(s))return s;
 need(s.base.version<MAX,"version_exhausted");
 return state({...s,pending:{id:uuid(id),expectedVersion:s.base.version,document:s.document}});
}
function acknowledge(input,reply){
 const s=state(input);need(s.pending!==null&&plain(reply),"unexpected_receipt");
 need(reply.ownerId===s.ownerId&&reply.courseId===s.courseId&&reply.operationId===s.pending.id,"receipt_scope_mismatch");
 if(reply.status==="conflict"){
  let remote=snapshot(reply);need(remote.version!==s.pending.expectedVersion,"invalid_receipt");
  if(s.remote&&s.remote.version===remote.version)need(equal(s.remote.document,remote.document),"invalid_receipt");
  if(s.remote&&s.remote.version>remote.version)remote=s.remote;
  return state({...s,remote,phase:"conflict"});
 }
 need(["committed","replayed"].includes(reply.status),"invalid_receipt");
 const committed=snapshot(reply);need(committed.version===s.pending.expectedVersion+1&&equal(committed.document,s.pending.document),"invalid_receipt");
 const current=snapshot({version:reply.currentVersion,document:reply.currentDocument});
 need(current.version>=committed.version,"invalid_receipt");
 if(current.version===committed.version)need(equal(current.document,committed.document),"invalid_receipt");
 if(s.remote&&s.remote.version===current.version)need(equal(s.remote.document,current.document),"invalid_receipt");
 const latest=s.remote&&s.remote.version>current.version?s.remote:current;
 return state({...s,base:committed,pending:null,remote:latest.version>committed.version?latest:null,phase:latest.version>committed.version?"conflict":"ready"});
}
function resolve(input,choice){
 const s=state(input);need(s.phase==="conflict"&&s.remote!==null,"no_conflict");
 need(choice==="local"||choice==="remote","invalid_resolution");
 return state({...s,base:s.remote,document:choice==="remote"?s.remote.document:s.document,pending:null,remote:null,phase:"ready"});
}
function serialize(input){return JSON.stringify(state(input));}
function restore(raw,scope){
 need(typeof raw==="string"&&bytes(raw)<=5*1048576,"invalid_cache");
 let parsed;try{parsed=JSON.parse(raw);}catch{fail("invalid_cache");}
 const s=state(parsed);need(s.ownerId===uuid(scope.ownerId)&&s.courseId===uuid(scope.courseId),"cache_scope_mismatch");return s;
}
function createService(client){
 need(client&&client.auth&&typeof client.auth.getUser==="function"&&typeof client.rpc==="function","invalid_client");
 async function identity(){
  let result;try{result=await client.auth.getUser();}catch(e){
   if(e instanceof TypeError||e?.name==="AuthRetryableFetchError")fail("transport_error");
   fail("auth_required");
  }
  if(result?.error?.name==="AuthRetryableFetchError"&&(result.error.status===0||(result.error.status>=500&&result.error.status<=599)))fail("transport_error");
  need(result&&result.error===null&&result.data&&result.data.user,"auth_required");return uuid(result.data.user.id);
 }
 async function call(name,args){
  let r;try{r=await client.rpc(name,args);}catch{fail("transport_error");}
  need(r&&r.error===null&&plain(r.data),"transport_error");
  if(r.data.status==="denied")fail("access_denied");
  return r.data;
 }
 async function context(){
  const owner=await identity(),r=await call("accaoui_progress_context_v1",{p_owner_id:owner});
  need(r.status==="ready"&&r.ownerId===owner&&Array.isArray(r.courses),"invalid_response");
  const seen=new Set();const courses=r.courses.map(x=>{need(plain(x)&&typeof x.title==="string","invalid_response");const id=uuid(x.id);need(!seen.has(id),"invalid_response");seen.add(id);return freeze({id,title:x.title});});
  return freeze({ownerId:owner,courses});
 }
 async function read(course){
  const owner=await identity(),id=uuid(course),r=await call("accaoui_progress_read_v1",{p_owner_id:owner,p_course_id:id});
  need(r.status==="ready"&&r.ownerId===owner&&r.courseId===id,"invalid_response");
  return create({ownerId:owner,courseId:id},snapshot(r));
 }
 async function commit(input){
  const s=state(input);need(s.phase==="ready"&&s.pending!==null,"no_pending_operation");
  need(await identity()===s.ownerId,"account_changed");
  const r=await call("accaoui_progress_write_v1",{p_owner_id:s.ownerId,p_course_id:s.courseId,p_expected_version:s.pending.expectedVersion,p_operation_id:s.pending.id,p_document:s.pending.document});
  if(["invalid_document","invalid_request","operation_mismatch","version_exhausted"].includes(r.status))fail(r.status);
  acknowledge(s,r); // Validate against the sent operation; the caller applies to its latest draft.
  const result={status:r.status,ownerId:r.ownerId,courseId:r.courseId,operationId:r.operationId,version:r.version,document:document(r.document)};
  if(r.status!=="conflict"){result.currentVersion=version(r.currentVersion);result.currentDocument=document(r.currentDocument);}
  return freeze(result);
 }
 return Object.freeze({context,read,commit});
}
const api=Object.freeze({KEYS,empty,document,create,edit,dirty,begin,acknowledge,resolve,serialize,restore,createService});
if(common&&common.exports)common.exports=api;
if(root&&root.ACCAOUI_PARTICIPANT_PROGRESS_V1===undefined)Object.defineProperty(root,"ACCAOUI_PARTICIPANT_PROGRESS_V1",{value:api,enumerable:true,writable:false,configurable:false});
})(typeof window!=="undefined"?window:null,typeof module!=="undefined"?module:null);
