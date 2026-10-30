/* W06 private-development material contract. No SDK bootstrap, keys or storage patch. */
(function(root,common){
"use strict";
const LIMIT=262144,UUID=/^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i,HASH=/^[0-9a-f]{64}$/;
const own=Object.prototype.hasOwnProperty,states=new WeakSet();
function fail(code){const e=new Error(code);e.code=code;throw e;}
function need(v,code){if(!v)fail(code);}
function record(v){return v!==null&&typeof v==="object"&&!Array.isArray(v)&&[Object.prototype,null].includes(Object.getPrototypeOf(v));}
function exact(v,names){return record(v)&&Object.keys(v).length===names.length&&names.every(k=>own.call(v,k));}
function integer(n,min=0){return Number.isSafeInteger(n)&&n>=min&&n<=2147483646;}
function uuid(v){return typeof v==="string"&&UUID.test(v);}
function utf8(v){need(typeof v==="string","invalid_text");const b=new TextEncoder().encode(v);need(new TextDecoder("utf-8",{fatal:true}).decode(b)===v&&!/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f-\u009f]/.test(v),"invalid_text");return b;}
function date(v){return typeof v==="string"&&/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/.test(v)&&Number(v.slice(0,4))>=1&&Number.isFinite(Date.parse(v))&&new Date(v).toISOString()===v;}
function jsonSafe(v,depth=0){if(depth>12)return false;if(v===null||typeof v==="boolean")return true;if(typeof v==="number")return Number.isFinite(v)&&Math.abs(v)<=Number.MAX_SAFE_INTEGER;if(typeof v==="string"){try{return utf8(v).length<=LIMIT;}catch{return false;}}if(Array.isArray(v))return v.length<=2000&&v.every(x=>jsonSafe(x,depth+1));return record(v)&&Object.keys(v).length<=2000&&Object.entries(v).every(([k,x])=>[...k].length<=200&&!["__proto__","prototype","constructor"].includes(k)&&jsonSafe(x,depth+1));}
function freeze(v){if(v&&typeof v==="object"){for(const x of Object.values(v))freeze(x);Object.freeze(v);}return v;}
function clone(v){return JSON.parse(JSON.stringify(v));}
function draft(value){
 need(exact(value,["id","title","filename","mime","body","state","expiresAt"]),"invalid_draft");
 need(uuid(value.id)&&typeof value.title==="string"&&value.title===value.title.trim()&&value.title.length>0&&[...value.title].length<=200&&!/[\r\n\t]/.test(value.title),"invalid_draft");utf8(value.title);
 need(typeof value.filename==="string"&&/^[A-Za-z0-9][A-Za-z0-9_-]{0,59}\.(txt|json)$/.test(value.filename),"invalid_filename");
 need(["text/plain","application/json"].includes(value.mime)&&value.filename.endsWith(value.mime==="text/plain"?".txt":".json"),"invalid_mime");
 need(["draft","published"].includes(value.state)&&(value.expiresAt===null||date(value.expiresAt)),"invalid_draft");
 const bytes=utf8(value.body);need(bytes.length>0&&bytes.length<=LIMIT,"invalid_size");
 if(value.mime==="application/json"){let parsed;try{parsed=JSON.parse(value.body);}catch{fail("invalid_json");}need(jsonSafe(parsed),"invalid_json");}
 return freeze({id:value.id,title:value.title,filename:value.filename,mime:value.mime,body:value.body,state:value.state,expiresAt:value.expiresAt});
}
function metadata(v){
 need(exact(v,["id","courseId","title","filename","mime","version","state","expiresAt","sha256","bytes"]),"invalid_response");
 need(uuid(v.id)&&uuid(v.courseId)&&integer(v.version,1)&&["draft","published","revoked"].includes(v.state)&&typeof v.sha256==="string"&&HASH.test(v.sha256)&&integer(v.bytes,1)&&v.bytes<=LIMIT,"invalid_response");
 draft({id:v.id,title:v.title,filename:v.filename,mime:v.mime,body:v.mime==="text/plain"?"x":"{}",state:v.state==="revoked"?"draft":v.state,expiresAt:v.expiresAt});return freeze(clone(v));
}
function command(v){
 need(exact(v,["schema","ownerId","courseId","operationId","action","materialId","expectedVersion","draft"])&&v.schema===1&&uuid(v.ownerId)&&uuid(v.courseId)&&uuid(v.operationId)&&uuid(v.materialId),"invalid_command");
 need(["save","revoke","download"].includes(v.action)&&integer(v.expectedVersion,v.action==="save"?0:1),"invalid_command");
 const value=v.action==="save"?draft(v.draft):null;need(v.action==="save"?value.id===v.materialId:v.draft===null,"invalid_command");return freeze({...v,draft:value});
}
function checkedState(s){
 if(states.has(s))return s;
 need(exact(s,["schema","ownerId","courseId","draft","pending","confirmed","remoteVersion","problem","needsReload"])&&s.schema===1&&uuid(s.ownerId)&&uuid(s.courseId)&&integer(s.remoteVersion)&&[null,"transport_error","conflict","denied","expired","revoked","not_found","operation_mismatch","invalid_request","stale_ack"].includes(s.problem)&&typeof s.needsReload==="boolean","invalid_state");
 const d=s.draft===null?null:draft(s.draft),p=s.pending===null?null:command(s.pending),c=s.confirmed===null?null:metadata(s.confirmed);
 need((!p||(p.ownerId===s.ownerId&&p.courseId===s.courseId))&&(!c||c.courseId===s.courseId),"invalid_state");
 const result=freeze({...s,draft:d,pending:p,confirmed:c});states.add(result);return result;
}
function create({ownerId,courseId}){return checkedState({schema:1,ownerId,courseId,draft:null,pending:null,confirmed:null,remoteVersion:0,problem:null,needsReload:false});}
function edit(s,value){s=checkedState(s);return checkedState({...s,draft:draft(value),problem:s.pending?s.problem:null});}
function begin(s,{action,materialId,expectedVersion,operationId}){s=checkedState(s);need(s.pending===null,"pending_exists");return checkedState({...s,pending:command({schema:1,ownerId:s.ownerId,courseId:s.courseId,operationId,action,materialId,expectedVersion,draft:action==="save"?s.draft:null}),problem:null});}
function transportFailure(s){s=checkedState(s);need(s.pending!==null,"missing_pending");return checkedState({...s,problem:"transport_error"});}
function accept(s,response){
 s=checkedState(s);need(s.pending!==null&&record(response)&&typeof response.status==="string","invalid_response");
 if(response.status!=="ready"){
  need(["conflict","denied","expired","revoked","not_found","operation_mismatch","invalid_request"].includes(response.status),"invalid_response");
  const remote=response.status==="conflict"?response.currentVersion:s.remoteVersion;need(integer(remote),"invalid_response");return checkedState({...s,problem:response.status,remoteVersion:remote});
 }
 const c=s.pending,m=metadata(response.material);need(response.ownerId===s.ownerId&&response.courseId===s.courseId&&response.operationId===c.operationId&&m.id===c.materialId&&m.courseId===s.courseId&&integer(response.currentVersion,m.version),"invalid_response");
 need(m.version===(c.action==="download"?c.expectedVersion:c.expectedVersion+1),"invalid_response");
 if(c.action==="save")need(m.title===c.draft.title&&m.filename===c.draft.filename&&m.mime===c.draft.mime&&m.state===c.draft.state&&m.expiresAt===c.draft.expiresAt&&m.bytes===utf8(c.draft.body).length,"invalid_response");
 if(c.action==="revoke")need(m.state==="revoked","invalid_response");
 return checkedState({...s,pending:null,confirmed:m,remoteVersion:response.currentVersion,problem:response.currentVersion>m.version?"stale_ack":null,needsReload:response.currentVersion>m.version});
}
function resolveConflict(s,choice){s=checkedState(s);need(s.problem==="conflict"&&s.pending!==null&&choice==="keep_draft","explicit_resolution_required");return checkedState({...s,pending:null,problem:null,needsReload:true});}
function serialize(s){return JSON.stringify(checkedState(s));}
function restore(raw,{ownerId,courseId}){need(typeof raw==="string"&&raw.length<=6*LIMIT,"invalid_state");let s;try{s=JSON.parse(raw);}catch{fail("invalid_state");}s=checkedState(s);need(s.ownerId===ownerId&&s.courseId===courseId,"wrong_scope");return s;}
async function hashText(text){const b=utf8(text);need(globalThis.crypto?.subtle,"digest_unavailable");return [...new Uint8Array(await globalThis.crypto.subtle.digest("SHA-256",b))].map(x=>x.toString(16).padStart(2,"0")).join("");}
async function verifyBody(result,{receipt=false}={}){
 const m=metadata(result.material),bytes=utf8(result.body);need(bytes.length===m.bytes&&bytes.length<=LIMIT&&await hashText(result.body)===m.sha256,"invalid_download");
 if(receipt){const r=result.receipt;need(exact(r,["id","ownerId","courseId","materialId","version","sha256","downloadedAt"])&&uuid(r.id)&&r.ownerId===result.ownerId&&r.courseId===result.courseId&&r.materialId===m.id&&r.version===m.version&&r.sha256===m.sha256&&date(r.downloadedAt),"invalid_download");}
 return bytes;
}
function createService(client){
 need(client&&typeof client.rpc==="function"&&typeof client.auth?.getUser==="function","client_unavailable");
 async function call(action,courseId=null,materialId=null,expectedVersion=null,operationId=null,value=null,owner=null){
  let identity;try{identity=await client.auth.getUser();}catch{fail("transport_error");}
  if(identity.error)fail(["AuthRetryableFetchError","TypeError"].includes(identity.error.name)||identity.error.status===0?"transport_error":"access_denied");
  need(uuid(identity.data?.user?.id),"access_denied");const actor=identity.data.user.id;need(owner===null||owner===actor,"access_denied");
  let response;try{response=await client.rpc("accaoui_training_material_v1",{p_owner_id:actor,p_action:action,p_course_id:courseId,p_material_id:materialId,p_expected_version:expectedVersion,p_operation_id:operationId,p_draft:value});}catch{fail("transport_error");}
  if(response.error){const status=Number(response.error.status||response.status);fail([401,403].includes(status)?"access_denied":"transport_error");}
  const r=response.data;need(record(r)&&typeof r.status==="string","invalid_response");
  if(r.status==="ready")need(r.ownerId===actor&&(courseId===null||r.courseId===courseId),"invalid_response");return r;
 }
 async function context(){const r=await call("context");need(r.status==="ready"&&Array.isArray(r.courses),r.status==="denied"?"access_denied":"invalid_response");for(const c of r.courses)need(exact(c,["id","title","role"])&&uuid(c.id)&&typeof c.title==="string"&&["participant","admin","dozent"].includes(c.role),"invalid_response");return freeze(clone(r));}
 async function list(course){need(uuid(course),"invalid_scope");const r=await call("list",course);need(r.status==="ready"&&Array.isArray(r.materials),r.status==="denied"?"access_denied":"invalid_response");for(const x of r.materials)need(metadata(x).courseId===course,"invalid_response");return freeze(clone(r));}
 async function inspect(course,id){need(uuid(course)&&uuid(id),"invalid_scope");const r=await call("inspect",course,id);need(r.status==="ready",r.status==="denied"?"access_denied":r.status);need(r.material.id===id,"invalid_response");await verifyBody(r);return freeze(clone(r));}
 async function send(value){const c=command(value),r=await call(c.action,c.courseId,c.materialId,c.expectedVersion,c.operationId,c.draft,c.ownerId);if(r.status==="ready"){
   const m=metadata(r.material);need(r.operationId===c.operationId&&m.id===c.materialId,"invalid_response");
   if(c.action==="save")need(await hashText(c.draft.body)===m.sha256,"invalid_response");
   if(c.action==="download")await verifyBody(r,{receipt:true});
  }else need(["conflict","denied","expired","revoked","not_found","operation_mismatch","invalid_request"].includes(r.status),"invalid_response");return freeze(clone(r));}
 async function receipts(course){need(uuid(course),"invalid_scope");const r=await call("receipts",course);need(r.status==="ready"&&Array.isArray(r.receipts),r.status==="denied"?"access_denied":"invalid_response");for(const v of r.receipts)need(exact(v,["id","ownerId","courseId","materialId","version","sha256","downloadedAt"])&&uuid(v.id)&&uuid(v.ownerId)&&v.courseId===course&&uuid(v.materialId)&&integer(v.version,1)&&typeof v.sha256==="string"&&HASH.test(v.sha256)&&date(v.downloadedAt),"invalid_response");return freeze(clone(r));}
 return Object.freeze({context,list,inspect,send,receipts});
}
function exportInventory(courseId,items){need(uuid(courseId)&&Array.isArray(items)&&items.length<=1000,"invalid_export");const values=items.map(x=>metadata(x));need(values.every(x=>x.courseId===courseId),"wrong_scope");return JSON.stringify({schema:1,kind:"synthetic_training_material_inventory",courseId,publicationAuthority:false,materials:values},null,2)+"\n";}
const api=Object.freeze({LIMIT,uuid,draft,metadata,command,create,edit,begin,transportFailure,accept,resolveConflict,serialize,restore,hashText,verifyBody,createService,exportInventory});
if(common?.exports)common.exports=api;if(root&&root.ACCAOUI_MATERIAL_DOCUMENT_V1===undefined)Object.defineProperty(root,"ACCAOUI_MATERIAL_DOCUMENT_V1",{value:api,enumerable:true,writable:false,configurable:false});
})(typeof window!=="undefined"?window:null,typeof module!=="undefined"?module:null);
