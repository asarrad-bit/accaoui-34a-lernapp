/* W03 model + real private DB/Auth acceptance; no browser/full-app claim. */
"use strict";
const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto"),assert=require("node:assert/strict");
const api=require("../data/supabase-participant-progress-v1.js");
const mode=process.argv[2],cfg=JSON.parse(fs.readFileSync(process.argv[3],"utf8"));
assert.ok(["pure","real"].includes(mode));assert.ok(Array.isArray(cfg.expectedCases));
assert.ok(path.resolve(cfg.resultPath).startsWith(path.resolve(cfg.evidenceDirectory)+path.sep));
assert.equal(fs.existsSync(cfg.resultPath),false);assert.equal(new Set(cfg.expectedCases).size,cfg.expectedCases.length);
const sha=b=>crypto.createHash("sha256").update(b).digest("hex");
const root=path.resolve(__dirname,".."),rows=[],cleanup=[];
let active="setup",failure=null,lastResponse=null;
for(const [name,p] of Object.entries(cfg.sourcePins)){const b=fs.readFileSync(path.join(root,name));assert.equal(b.length,p.bytes);assert.equal(sha(b),p.sha256);}
async function check(name,fn){active=name;await fn();rows.push({id:name,status:"PASS"});}
const uid=()=>crypto.randomUUID(),doc=value=>api.document({schema:1,values:value});
const A="11111111-1111-4111-8111-111111111111",B="22222222-2222-4222-8222-222222222222",C="33333333-3333-4333-8333-333333333333";
const initial=()=>api.create({ownerId:A,courseId:C},{version:0,document:api.empty()});
const changed=()=>api.edit(initial(),"accaoui_topic_stats",'{"Gewerberecht":{"answered":1,"correct":1}}');
const pending=()=>api.begin(changed(),"44444444-4444-4444-8444-444444444444");
const receipt=s=>({status:"committed",ownerId:s.ownerId,courseId:s.courseId,operationId:s.pending.id,version:s.base.version+1,document:s.pending.document,currentVersion:s.base.version+1,currentDocument:s.pending.document});
const throws=(fn,code)=>assert.throws(fn,e=>e.code===code);
async function pure(){
 await check("pure:empty-is-frozen-and-clean",()=>{const s=initial();assert.ok(Object.isFrozen(s)&&Object.isFrozen(s.document.values));assert.equal(api.dirty(s),false);});
 await check("pure:unknown-storage-key-denied",()=>throws(()=>api.edit(initial(),"other","{}"),"invalid_key"));
 await check("pure:invalid-json-denied",()=>throws(()=>doc({accaoui_topic_stats:"{"}),"invalid_document"));
 await check("pure:wrong-root-type-denied",()=>throws(()=>doc({accaoui_exam_history:"{}"}),"invalid_document"));
 await check("pure:unknown-envelope-field-denied",()=>throws(()=>api.document({schema:1,values:{},extra:1}),"invalid_document"));
 await check("pure:prototype-payload-denied",()=>throws(()=>doc({accaoui_topic_stats:'{"__proto__":{"admin":true}}'}),"invalid_document"));
 await check("pure:unsafe-number-denied",()=>throws(()=>doc({accaoui_topic_stats:'{"v":1e100}'}),"invalid_document"));
 await check("pure:valid-leap-date",()=>assert.equal(doc({accaoui_exam_date_written_v1:"2028-02-29"}).values.accaoui_exam_date_written_v1,"2028-02-29"));
 await check("pure:invalid-date-denied",()=>throws(()=>doc({accaoui_exam_date_written_v1:"2027-02-29"}),"invalid_document"));
 await check("pure:year-zero-denied",()=>throws(()=>doc({accaoui_exam_date_written_v1:"0000-01-01"}),"invalid_document"));
 await check("pure:oversize-value-denied",()=>throws(()=>doc({accaoui_topic_stats:'{"v":"'+"x".repeat(262144)+'"}'}),"invalid_document"));
 await check("pure:edit-preserves-source",()=>{const s=initial(),before=api.serialize(s);api.edit(s,"accaoui_answered_questions",'{"q":true}');assert.equal(api.serialize(s),before);});
 await check("pure:begin-retains-stable-operation",()=>{const s=pending();assert.equal(api.begin(s,uid()).pending.id,s.pending.id);});
 await check("pure:pending-payload-immutable-after-new-edit",()=>{const s=pending(),n=api.edit(s,"accaoui_topic_mistakes",'{"q":1}');assert.equal(n.pending.document.values.accaoui_topic_mistakes,undefined);assert.equal(n.document.values.accaoui_topic_mistakes,'{"q":1}');});
 await check("pure:ack-preserves-newer-local-draft",()=>{const s=pending(),n=api.edit(s,"accaoui_topic_mistakes",'{"q":1}'),a=api.acknowledge(n,receipt(s));assert.equal(a.base.version,1);assert.equal(api.dirty(a),true);assert.equal(a.document.values.accaoui_topic_mistakes,'{"q":1}');});
 await check("pure:foreign-receipt-denied",()=>{const s=pending();throws(()=>api.acknowledge(s,{...receipt(s),ownerId:B}),"receipt_scope_mismatch");});
 await check("pure:wrong-ack-version-denied",()=>{const s=pending();throws(()=>api.acknowledge(s,{...receipt(s),version:2}),"invalid_receipt");});
 await check("pure:wrong-ack-document-denied",()=>{const s=pending();throws(()=>api.acknowledge(s,{...receipt(s),document:api.empty()}),"invalid_receipt");});
 const conflict=()=>{const s=pending();return api.acknowledge(s,{status:"conflict",ownerId:A,courseId:C,operationId:s.pending.id,version:2,document:doc({accaoui_answered_questions:'{"remote":true}'})});};
 await check("pure:conflict-keeps-local-input",()=>{const s=conflict();assert.equal(s.document.values.accaoui_topic_stats,changed().document.values.accaoui_topic_stats);assert.equal(s.phase,"conflict");});
 await check("pure:conflict-cannot-auto-upgrade",()=>throws(()=>api.begin(conflict(),uid()),"conflict_requires_explicit_resolution"));
 await check("pure:explicit-local-resolution",()=>{const s=api.resolve(conflict(),"local");assert.equal(s.base.version,2);assert.equal(api.dirty(s),true);assert.equal(s.pending,null);});
 await check("pure:explicit-remote-resolution",()=>{const s=api.resolve(conflict(),"remote");assert.equal(s.base.version,2);assert.equal(api.dirty(s),false);});
 await check("pure:serialize-restore-retains-pending-intent",()=>{const s=pending();assert.equal(api.serialize(api.restore(api.serialize(s),{ownerId:A,courseId:C})),api.serialize(s));});
 await check("pure:large-conflict-cache-roundtrip-retains-all-four-documents",()=>{
  const raw=JSON.stringify({value:"x".repeat(200000)}),large=doc({accaoui_topic_stats:raw,accaoui_topic_mistakes:raw,accaoui_answered_questions:raw});
  let s=api.create({ownerId:A,courseId:C},{version:0,document:large});s=api.begin(api.edit(s,"accaoui_active_learning_session",'{"p":1}'),uid());
  s=api.acknowledge(s,{status:"conflict",ownerId:A,courseId:C,operationId:s.pending.id,version:1,document:large});
  const saved=api.serialize(s);assert.ok(Buffer.byteLength(saved)>2200000);assert.equal(api.serialize(api.restore(saved,{ownerId:A,courseId:C})),saved);
 });
 await check("pure:restore-other-owner-denied",()=>throws(()=>api.restore(api.serialize(pending()),{ownerId:B,courseId:C}),"cache_scope_mismatch"));
 await check("pure:restore-other-course-denied",()=>throws(()=>api.restore(api.serialize(pending()),{ownerId:A,courseId:B}),"cache_scope_mismatch"));
 await check("pure:invalid-cache-preserved-by-rejection",()=>throws(()=>api.restore("{",{ownerId:A,courseId:C}),"invalid_cache"));
 await check("pure:late-ack-keeps-known-newer-server",()=>{const s=conflict(),a=api.acknowledge(s,receipt(s));assert.equal(a.phase,"conflict");assert.equal(a.remote.version,2);});
 await check("pure:old-replay-keeps-server-conflict",()=>{const s=pending(),r={...receipt(s),status:"replayed",currentVersion:3,currentDocument:api.empty()};const a=api.acknowledge(s,r);assert.equal(a.phase,"conflict");assert.equal(a.remote.version,3);});
 await check("pure:unchanged-state-creates-no-intent",()=>assert.equal(api.begin(initial(),uid()).pending,null));
 await check("pure:version-limit-does-not-reset-data",()=>{let s=api.create({ownerId:A,courseId:C},{version:Number.MAX_SAFE_INTEGER,document:api.empty()});s=api.edit(s,"accaoui_topic_stats","{}");throws(()=>api.begin(s,uid()),"version_exhausted");assert.equal(s.document.values.accaoui_topic_stats,"{}");});
 await check("pure:invalid-client-denied",()=>throws(()=>api.createService({}),"invalid_client"));
 await check("pure:auth-switch-blocks-before-rpc",async()=>{let calls=0;const s=api.createService({auth:{getUser:async()=>({data:{user:{id:B}},error:null})},rpc:async()=>{calls++;}});await assert.rejects(s.commit(pending()),e=>e.code==="account_changed");assert.equal(calls,0);});
 await check("pure:transport-failure-keeps-pending",async()=>{const s=pending(),before=api.serialize(s),service=api.createService({auth:{getUser:async()=>({data:{user:{id:A}},error:null})},rpc:async()=>{throw Error("injected offline");}});await assert.rejects(service.commit(s),e=>e.code==="transport_error");assert.equal(api.serialize(s),before);});
 await check("pure:identity-network-throw-keeps-pending",async()=>{const s=pending(),before=api.serialize(s);let calls=0;const service=api.createService({auth:{getUser:async()=>{throw new TypeError("injected network failure");}},rpc:async()=>{calls++;}});await assert.rejects(service.commit(s),e=>e.code==="transport_error");assert.equal(api.serialize(s),before);assert.equal(calls,0);});
 await check("pure:sdk-network-error-is-retryable-without-data-loss",async()=>{const s=pending(),before=api.serialize(s);const service=api.createService({auth:{getUser:async()=>({data:{user:null},error:{name:"AuthRetryableFetchError",status:0}})},rpc:async()=>assert.fail("no RPC without identity")});await assert.rejects(service.commit(s),e=>e.code==="transport_error");assert.equal(api.serialize(s),before);});
 await check("pure:sdk-service-error-is-retryable-without-data-loss",async()=>{const s=pending(),before=api.serialize(s);const service=api.createService({auth:{getUser:async()=>({data:{user:null},error:{name:"AuthRetryableFetchError",status:503}})},rpc:async()=>assert.fail("no RPC without identity")});await assert.rejects(service.commit(s),e=>e.code==="transport_error");assert.equal(api.serialize(s),before);});
 await check("pure:auth-denial-cannot-become-offline-access",async()=>{const s=pending(),before=api.serialize(s);const service=api.createService({auth:{getUser:async()=>({data:{user:null},error:{name:"AuthApiError",status:401}})},rpc:async()=>assert.fail("no RPC without identity")});await assert.rejects(service.commit(s),e=>e.code==="auth_required");assert.equal(api.serialize(s),before);});
 await check("pure:cloned-known-document-extra-envelope-still-denied",()=>{const known=api.empty(),copy=JSON.parse(JSON.stringify(known));copy.extra=true;throws(()=>api.document(copy),"invalid_document");});
 await check("pure:validated-object-raw-cannot-satisfy-array-key",()=>{doc({accaoui_topic_stats:"{}"});throws(()=>doc({accaoui_exam_history:"{}"}),"invalid_document");});
 await check("pure:changed-unsafe-raw-still-denied-after-validation",()=>{doc({accaoui_topic_stats:'{"safe":true}'});throws(()=>doc({accaoui_topic_stats:'{"constructor":{"unsafe":true}}'}),"invalid_document");});
 await check("pure:cloned-known-state-extra-field-still-denied",()=>{const copy={...initial(),extra:true};throws(()=>api.serialize(copy),"invalid_state");});
 await check("pure:cloned-receipt-document-unknown-key-still-denied",()=>{const s=pending(),r=receipt(s);r.document=JSON.parse(JSON.stringify(r.document));r.document.values.other="{}";throws(()=>api.acknowledge(s,r),"invalid_document");});
 await check("pure:equivalent-distinct-owned-documents-remain-clean",()=>{const base=doc({accaoui_topic_stats:"{}",accaoui_answered_questions:"{}"});let s=api.create({ownerId:A,courseId:C},{version:1,document:base});s=api.edit(s,"accaoui_topic_stats","{}");assert.equal(api.dirty(s),false);assert.equal(api.begin(s,uid()).pending,null);});
}
function memoryStorage(initialValues={}){
 const data=new Map(Object.entries(initialValues));
 return {getItem:k=>data.get(k)??null,setItem:(k,v)=>data.set(k,v),removeItem:k=>data.delete(k),snapshot:()=>Object.fromEntries(data)};
}
async function real(){
 const {createClient}=require("@supabase/supabase-js");
 const lifecycle=await import("/work/lifecycle.mjs");
 const config=lifecycle.credentials();assert.equal(config.url,"http://api:8000");
 const runId=cfg.runId;assert.match(runId,/^[0-9a-f-]{36}$/);
 const prefix="w03-"+runId;const createdUsers=[],participantIds=[],courseIds=[],profileIds=[];
 let admin;
 const fetchState={offline:false};
 function make(key,storage=memoryStorage(),keyName=uid(),switchState=null){
  return createClient(config.url,key,{global:{fetch:(input,init={})=>{
   const u=new URL(typeof input==="string"||input instanceof URL?input:input.url);assert.equal(u.origin,config.url);
   if(switchState?.offline)throw new TypeError("Injected offline transport");
   return fetch(input,{...init,redirect:"error",signal:AbortSignal.timeout(15000)});
  }},auth:{persistSession:true,autoRefreshToken:false,detectSessionInUrl:false,storage,storageKey:keyName}});
 }
 function ok(r){lastResponse={errorCode:r.error?.code??null,status:r.data?.status??null};assert.equal(r.error,null);return r.data;}
 const get=async(client,owner,course)=>ok(await client.rpc("accaoui_progress_read_v1",{p_owner_id:owner,p_course_id:course}));
 let a,a2,b,staff,sa,sa2,sb,users,shared,ownA,ownB,enrollA,latest,oldIntent,replayed,serialized;
 try{
  admin=make(config.adminKey);
  await check("real:create-only-synthetic-confirmed-users",async()=>{
   users=[];
   for(const label of ["a","b","staff"]){
    const email=prefix+"-"+label+"@accaoui.invalid",password="Local-"+crypto.randomBytes(24).toString("base64url")+"-9aA!";
    const r=await admin.auth.admin.createUser({email,password,email_confirm:true,app_metadata:{accaoui_w03_run:runId}});
    const u=ok(r).user;assert.ok(u?.id);createdUsers.push(u.id);users.push({id:u.id,email,password});
   }
  });
  await check("real:seed-only-owned-course-participant-fixtures",async()=>{
   for(let attempt=0;attempt<20;attempt++){
    const r=await admin.from("participants").select("id").limit(0);
    if(!r.error)break;
    if(!["PGRST205","PGRST204"].includes(r.error.code)||attempt===19)ok(r);
    await new Promise(resolve=>setTimeout(resolve,500));
   }
   const courseRows=["a","b","shared"].map(label=>({id:uid(),title:prefix+"-"+label,course_type:"sachkunde_34a",status:"active"}));
   ok(await admin.from("courses").insert(courseRows));courseIds.push(...courseRows.map(x=>x.id));[ownA,ownB,shared]=courseIds;
   const pRows=users.slice(0,2).map((u,i)=>({id:uid(),auth_user_id:u.id,first_name:"Synthetic",last_name:"W03",email:u.email,status:"active"}));
   ok(await admin.from("participants").insert(pRows));participantIds.push(...pRows.map(x=>x.id));
   const enroll=[{id:uid(),participant_id:pRows[0].id,course_id:ownA},{id:uid(),participant_id:pRows[0].id,course_id:shared},{id:uid(),participant_id:pRows[1].id,course_id:ownB},{id:uid(),participant_id:pRows[1].id,course_id:shared}];
   ok(await admin.from("enrollments").insert(enroll));enrollA=enroll[1].id;
   const profile={id:uid(),auth_user_id:users[2].id,display_name:prefix+"-staff",role:"support",status:"active"};
   ok(await admin.from("admin_profiles").insert(profile));profileIds.push(profile.id);
  });
  const authStore=memoryStorage(),authKey=uid();a=make(config.anonymousKey,authStore,authKey,fetchState);a2=make(config.anonymousKey);b=make(config.anonymousKey);staff=make(config.anonymousKey);
  await check("real:three-independent-sessions-sign-in",async()=>{
   for(const [client,user]of [[a,users[0]],[a2,users[0]],[b,users[1]],[staff,users[2]]])ok(await client.auth.signInWithPassword({email:user.email,password:user.password}));
   const t1=(await a.auth.getSession()).data.session.access_token,t2=(await a2.auth.getSession()).data.session.access_token;
   assert.notEqual(JSON.parse(Buffer.from(t1.split(".")[1],"base64url")).session_id,JSON.parse(Buffer.from(t2.split(".")[1],"base64url")).session_id);
   sa=api.createService(a);sa2=api.createService(a2);sb=api.createService(b);
  });
  await check("real:context-lists-only-enrolled-courses",async()=>{const c=await sa.context();assert.equal(c.ownerId,users[0].id);assert.deepEqual(c.courses.map(x=>x.id).sort(),[ownA,shared].sort());});
  await check("real:unenrolled-staff-has-no-progress-access",async()=>{const s=api.createService(staff);assert.deepEqual((await s.context()).courses,[]);await assert.rejects(s.read(shared),e=>e.code==="access_denied");});
  await check("real:unenrolled-course-denied",async()=>await assert.rejects(sa.read(ownB),e=>e.code==="access_denied"));
  await check("real:initial-progress-is-empty-without-write",async()=>{latest=await sa.read(shared);assert.equal(latest.base.version,0);assert.deepEqual(latest.document.values,{});});
  await check("real:narrow-views-exclude-foreign-owner-and-course",async()=>{
   assert.deepEqual(ok(await a.from("accaoui_progress_participant_v1").select("id,auth_user_id,status").eq("auth_user_id",users[1].id)),[]);
   assert.deepEqual(ok(await a.from("accaoui_progress_enrollment_v1").select("id").eq("participant_id",participantIds[1])),[]);
   assert.deepEqual(ok(await a.from("accaoui_progress_course_v1").select("id").eq("id",ownB)),[]);
   const own=ok(await a.from("accaoui_progress_participant_v1").select("id,auth_user_id,status"));assert.equal(own.length,1);assert.equal(own[0].auth_user_id,users[0].id);
  });
  await check("real:unchanged-auth-access-adapters-through-actual-scoped-view-queries",async()=>{
   const {createParticipantAuthSessionAdapter}=require("../data/supabase-participant-auth-session-adapter.js");
   const {createParticipantAccessAdapter}=require("../data/supabase-participant-access-adapter.js");
   const {create}=require("../data/supabase-participant-session-v1.js");
   const timerMap=new Map();let n=0;
   const s=create({model:api,createAuthAdapter:createParticipantAuthSessionAdapter,createAccessAdapter:createParticipantAccessAdapter,client:a,cache:memoryStorage(),tabStorage:memoryStorage(),locks:{request:async(_name,_options,fn)=>fn({})},now:()=>Date.now(),newId:uid,setTimer(fn,ms){timerMap.set(++n,{fn,ms});return n;},clearTimer(id){timerMap.delete(id);}});
   try{assert.equal((await s.resolveSession()).phase,"choose_course");await s.open(shared);assert.equal(s.status().ownerId,users[0].id);assert.equal(s.status().courseId,shared);assert.equal(s.storage().getItem("accaoui_topic_stats"),null);assert.equal(s.status().version,0);}
   finally{s.dispose();}
   // Storage/lock/clock scheduling above are labelled dependency fakes; only the SDK/DB/Auth accesses are real.
  });
  await check("real:first-save-is-durable",async()=>{let s=api.begin(api.edit(latest,"accaoui_topic_stats",'{"Gewerberecht":{"answered":1,"correct":1}}'),uid());latest=api.acknowledge(s,await sa.commit(s));assert.equal(latest.base.version,1);assert.equal((await sa2.read(shared)).document.values.accaoui_topic_stats,s.document.values.accaoui_topic_stats);});
  await check("real:shared-course-rls-hides-other-user-row",async()=>{const r=ok(await b.from("accaoui_participant_progress_v1").select("*").eq("owner_id",users[0].id));assert.deepEqual(r,[]);});
  await check("real:second-user-has-own-isolated-progress",async()=>{let s=await sb.read(shared);s=api.begin(api.edit(s,"accaoui_answered_questions",'{"b":true}'),uid());const saved=api.acknowledge(s,await sb.commit(s));assert.equal(saved.base.version,1);assert.equal((await sa.read(shared)).document.values.accaoui_answered_questions,undefined);});
  await check("real:same-user-other-course-is-isolated",async()=>assert.equal((await sa.read(ownA)).base.version,0));
  await check("real:direct-authenticated-table-writes-denied",async()=>{
   for(const r of [await a.from("accaoui_participant_progress_v1").insert({owner_id:users[0].id,course_id:ownA,version:1,document:api.empty()}),await a.from("accaoui_participant_progress_v1").update({version:99}).eq("owner_id",users[0].id),await a.from("accaoui_participant_progress_v1").delete().eq("owner_id",users[0].id)])assert.equal(r.error?.code,"42501");
  });
  await check("real:two-clients-cas-allows-exactly-one-writer",async()=>{
   const x=await sa.read(shared),y=await sa2.read(shared);
   const p=api.begin(api.edit(x,"accaoui_answered_questions",'{"first":true}'),uid()),q=api.begin(api.edit(y,"accaoui_answered_questions",'{"second":true}'),uid());
   const rr=await Promise.all([sa.commit(p),sa2.commit(q)]);assert.deepEqual(rr.map(x=>x.status).sort(),["committed","conflict"]);
   const loser=rr[0].status==="conflict"?api.acknowledge(p,rr[0]):api.acknowledge(q,rr[1]);
   assert.equal(loser.phase,"conflict");assert.equal(loser.base.version,1);assert.equal(loser.remote.version,2);
   latest=api.resolve(loser,"local");
  });
  await check("real:only-explicit-resolution-can-retry",async()=>{latest=api.begin(latest,uid());latest=api.acknowledge(latest,await sa.commit(latest));assert.equal(latest.base.version,3);});
  await check("real:lost-ack-intent-remains-serializable",async()=>{oldIntent=api.begin(api.edit(latest,"accaoui_topic_mistakes",'{"q":1}'),uid());const r=await sa.commit(oldIntent);assert.equal(r.status,"committed");serialized=api.serialize(oldIntent);assert.equal(oldIntent.base.version,3);});
  await check("real:new-client-restores-session-and-idempotent-retry",async()=>{
   const restored=make(config.anonymousKey,memoryStorage(authStore.snapshot()),authKey);const srv=api.createService(restored);
   const current=await srv.read(shared),pending=api.restore(serialized,{ownerId:current.ownerId,courseId:shared});
   const r=await srv.commit(pending);assert.equal(r.status,"replayed");replayed=api.acknowledge(pending,r);assert.equal(replayed.base.version,4);assert.equal(api.dirty(replayed),false);
  });
  await check("real:second-writer-after-ack-loss-is-not-overwritten",async()=>{
   let s=await sa2.read(shared);s=api.begin(api.edit(s,"accaoui_answered_questions",'{"newer-device":true}'),uid());s=api.acknowledge(s,await sa2.commit(s));assert.equal(s.base.version,5);
   const r=await sa.commit(oldIntent);assert.equal(r.status,"replayed");const conflict=api.acknowledge(oldIntent,r);assert.equal(conflict.remote.version,5);assert.equal(conflict.phase,"conflict");latest=api.resolve(conflict,"remote");
  });
  await check("real:edits-during-flight-survive-acknowledgement",async()=>{
   const sent=api.begin(api.edit(latest,"accaoui_topic_stats",'{"v":2}'),uid());const response=sa.commit(sent);
   const draft=api.edit(sent,"accaoui_active_learning_session",'{"mode":"test","position":2}');
   latest=api.acknowledge(draft,await response);assert.equal(latest.base.version,6);assert.equal(api.dirty(latest),true);assert.ok(latest.document.values.accaoui_active_learning_session);
   latest=api.begin(latest,uid());latest=api.acknowledge(latest,await sa.commit(latest));assert.equal(latest.base.version,7);
  });
  await check("real:operation-id-reuse-with-other-payload-is-rejected",async()=>{
   const r=ok(await a.rpc("accaoui_progress_write_v1",{p_owner_id:users[0].id,p_course_id:shared,p_expected_version:oldIntent.pending.expectedVersion,p_operation_id:oldIntent.pending.id,p_document:api.empty()}));assert.equal(r.status,"operation_mismatch");assert.equal((await sa.read(shared)).base.version,7);
  });
  await check("real:injected-offline-transport-retains-pending-input",async()=>{
   latest=api.begin(api.edit(latest,"accaoui_flashcard_progress",'{"q":{"known":true}}'),uid());const before=api.serialize(latest);fetchState.offline=true;
   try{await assert.rejects(sa.commit(latest),e=>["auth_required","transport_error"].includes(e.code));}finally{fetchState.offline=false;}
   assert.equal(api.serialize(latest),before);assert.equal((await sa2.read(shared)).base.version,7);
  });
  await check("real:reconnect-retries-same-intent",async()=>{const id=latest.pending.id;const r=await sa.commit(latest);assert.equal(r.operationId,id);latest=api.acknowledge(latest,r);assert.equal(latest.base.version,8);});
  let revokedPending;
  await check("real:enrollment-revocation-denies-read-and-write",async()=>{
   revokedPending=api.begin(api.edit(latest,"accaoui_topic_stats",'{"after-reconnect":true}'),uid());const raw=api.serialize(revokedPending);
   ok(await admin.from("enrollments").update({access_status:"blocked"}).eq("id",enrollA));await assert.rejects(sa.read(shared),e=>e.code==="access_denied");await assert.rejects(sa.commit(revokedPending),e=>e.code==="access_denied");assert.equal(api.serialize(revokedPending),raw);
  });
  await check("real:restored-enrollment-keeps-pending-intent",async()=>{ok(await admin.from("enrollments").update({access_status:"allowed"}).eq("id",enrollA));latest=api.acknowledge(revokedPending,await sa.commit(revokedPending));assert.equal(latest.base.version,9);});
  await check("real:blocked-participant-denied",async()=>{ok(await admin.from("participants").update({status:"blocked"}).eq("id",participantIds[0]));await assert.rejects(sa.read(shared),e=>e.code==="access_denied");ok(await admin.from("participants").update({status:"active"}).eq("id",participantIds[0]));});
  await check("real:archived-course-denied",async()=>{ok(await admin.from("courses").update({status:"archived"}).eq("id",shared));await assert.rejects(sa.read(shared),e=>e.code==="access_denied");ok(await admin.from("courses").update({status:"active"}).eq("id",shared));});
  await check("real:expired-enrollment-denied",async()=>{ok(await admin.from("enrollments").update({access_ends_at:new Date(Date.now()-60000).toISOString()}).eq("id",enrollA));await assert.rejects(sa.read(shared),e=>e.code==="access_denied");ok(await admin.from("enrollments").update({access_ends_at:null}).eq("id",enrollA));});
  await check("real:future-enrollment-denied",async()=>{ok(await admin.from("enrollments").update({access_starts_at:new Date(Date.now()+3600000).toISOString()}).eq("id",enrollA));await assert.rejects(sa.read(shared),e=>e.code==="access_denied");ok(await admin.from("enrollments").update({access_starts_at:null}).eq("id",enrollA));});
  await check("real:expired-course-date-denied",async()=>{ok(await admin.from("courses").update({end_date:new Date(Date.now()-86400000).toISOString().slice(0,10)}).eq("id",shared));await assert.rejects(sa.read(shared),e=>e.code==="access_denied");ok(await admin.from("courses").update({end_date:null}).eq("id",shared));});
  await check("real:foreign-owner-parameter-denied-by-server",async()=>{assert.equal((await get(a,users[1].id,shared)).status,"denied");const r=ok(await a.rpc("accaoui_progress_write_v1",{p_owner_id:users[1].id,p_course_id:shared,p_expected_version:1,p_operation_id:uid(),p_document:api.empty()}));assert.equal(r.status,"denied");});
  await check("real:auth-switch-cannot-write-old-users-state",async()=>{
   const old=api.begin(api.edit(latest,"accaoui_topic_stats",'{"wrong-account":true}'),uid());ok(await a2.auth.signInWithPassword({email:users[1].email,password:users[1].password}));
   await assert.rejects(sa2.commit(old),e=>e.code==="account_changed");assert.equal((await sb.read(shared)).base.version,1);
   ok(await a2.auth.signInWithPassword({email:users[0].email,password:users[0].password}));
  });
  await check("real:unknown-storage-key-denied-by-sql",async()=>{const r=ok(await a.rpc("accaoui_progress_write_v1",{p_owner_id:users[0].id,p_course_id:shared,p_expected_version:9,p_operation_id:uid(),p_document:{schema:1,values:{unapproved:"{}"}}}));assert.equal(r.status,"invalid_document");});
  await check("real:missing-schema-field-denied-by-sql",async()=>{const r=ok(await a.rpc("accaoui_progress_write_v1",{p_owner_id:users[0].id,p_course_id:shared,p_expected_version:9,p_operation_id:uid(),p_document:{other:1,values:{}}}));assert.equal(r.status,"invalid_document");});
  await check("real:anonymous-rpc-and-table-access-denied",async()=>{const n=make(config.anonymousKey);assert.ok((await n.rpc("accaoui_progress_read_v1",{p_owner_id:users[0].id,p_course_id:shared})).error);assert.ok((await n.from("accaoui_participant_progress_v1").select("*")).error);});
  await check("real:anonymous-and-unenrolled-staff-cannot-read-new-views",async()=>{const n=make(config.anonymousKey);for(const view of ["accaoui_progress_participant_v1","accaoui_progress_enrollment_v1","accaoui_progress_course_v1"]){assert.ok((await n.from(view).select("*")).error);assert.deepEqual(ok(await staff.from(view).select("*")),[]);}});
  await check("real:private-operation-ledger-not-exposed",async()=>assert.ok((await a.from("progress_operations_v1").select("*")).error));
  const rawRpc=async(token,body)=>{const r=await fetch(config.url+"/rest/v1/rpc/accaoui_progress_read_v1",{method:"POST",headers:{apikey:config.anonymousKey,Authorization:"Bearer "+token,"Content-Type":"application/json"},body:JSON.stringify(body),redirect:"error",signal:AbortSignal.timeout(15000)});return {http:r.status,data:await r.json()};};
  await check("real:cryptographically-valid-expired-token-denied",async()=>{
   const token=(await a.auth.getSession()).data.session.access_token,parts=token.split("."),header=JSON.parse(Buffer.from(parts[0],"base64url"));assert.equal(header.alg,"HS256");
   const claims=JSON.parse(Buffer.from(parts[1],"base64url"));claims.exp=Math.floor(Date.now()/1000)-60;claims.iat=claims.exp-60;
   const secretLine=/^JWT_SECRET=(.+)$/m.exec(fs.readFileSync("/work/.local/compose.env","utf8"));assert.ok(secretLine);
   const secret=secretLine[1].trim().replace(/^["']|["']$/g,"");const prefix=parts[0]+"."+Buffer.from(JSON.stringify(claims)).toString("base64url");const expired=prefix+"."+crypto.createHmac("sha256",secret).update(prefix).digest("base64url");
   assert.equal((await rawRpc(expired,{p_owner_id:users[0].id,p_course_id:shared})).http,401);
  });
  await check("real:actual-session-refresh-keeps-access",async()=>{ok(await a.auth.refreshSession());assert.equal((await sa.read(shared)).base.version,9);});
  await check("real:logout-denies-the-same-still-unexpired-jwt",async()=>{
   const token=(await a.auth.getSession()).data.session.access_token,body={p_owner_id:users[0].id,p_course_id:shared};
   assert.equal((await rawRpc(token,body)).data.status,"ready");ok(await a.auth.signOut({scope:"local"}));
   const r=await rawRpc(token,body);assert.equal(r.http,200);assert.equal(r.data.status,"denied");
   const table=await fetch(config.url+"/rest/v1/accaoui_participant_progress_v1?select=owner_id&owner_id=eq."+users[0].id,{headers:{apikey:config.anonymousKey,Authorization:"Bearer "+token},redirect:"error",signal:AbortSignal.timeout(15000)});
   assert.equal(table.status,200);assert.deepEqual(await table.json(),[]);
   for(const view of ["accaoui_progress_participant_v1","accaoui_progress_enrollment_v1","accaoui_progress_course_v1"]){const r=await fetch(config.url+"/rest/v1/"+view+"?select=*",{headers:{apikey:config.anonymousKey,Authorization:"Bearer "+token},redirect:"error",signal:AbortSignal.timeout(15000)});assert.equal(r.status,200);assert.deepEqual(await r.json(),[]);}
  });
  await check("real:logout-rls-hides-rows-and-other-clients-survive",async()=>{
   assert.equal((await sa2.read(shared)).base.version,9);assert.equal((await sb.read(shared)).base.version,1);
   assert.equal((await a.auth.getSession()).data.session,null);
  });
 }finally{
  const attempt=async(name,fn)=>{try{await fn();cleanup.push({name,status:"PASS"});}catch{cleanup.push({name,status:"FAIL"});}};
  if(admin){
   for(const id of participantIds)await attempt("remove-own-synthetic-participant",async()=>{const r=ok(await admin.from("participants").select("email").eq("id",id));assert.equal(r.length,1);assert.ok(r[0].email.startsWith(prefix+"-")&&r[0].email.endsWith("@accaoui.invalid"));ok(await admin.from("participants").delete().eq("id",id));});
   for(const id of profileIds)await attempt("remove-own-synthetic-staff-profile",async()=>{const r=ok(await admin.from("admin_profiles").select("display_name").eq("id",id));assert.equal(r[0].display_name,prefix+"-staff");ok(await admin.from("admin_profiles").delete().eq("id",id));});
   for(const id of courseIds)await attempt("remove-own-synthetic-course",async()=>{const r=ok(await admin.from("courses").select("title").eq("id",id));assert.ok(r[0].title.startsWith(prefix+"-"));ok(await admin.from("courses").delete().eq("id",id));});
   for(const id of createdUsers)await attempt("remove-own-synthetic-auth-user",async()=>{const r=await admin.auth.admin.getUserById(id);assert.equal(ok(r).user.app_metadata.accaoui_w03_run,runId);ok(await admin.auth.admin.deleteUser(id));});
  }
 }
 assert.ok(cleanup.every(x=>x.status==="PASS"),"own fixture cleanup must pass");
}
(async()=>{
 try{if(mode==="pure")await pure();else await real();assert.deepEqual(rows.map(x=>x.id),cfg.expectedCases);}
 catch(e){failure={case:active,type:e.name,code:e.code??null,response:lastResponse};}
 for(const [name,p]of Object.entries(cfg.sourcePins)){const b=fs.readFileSync(path.join(root,name));if(b.length!==p.bytes||sha(b)!==p.sha256)failure={case:"source-after-run",type:"SourceChanged"};}
 const report={schema:1,state:failure?"W03_BACKEND_ACCEPTANCE_NOT_PASSED":mode==="pure"?"W03_PURE_PROGRESS_MODEL_CASES_PASS":"W03_REAL_PRIVATE_PROGRESS_BACKEND_CASES_PASS",mode,at:new Date().toISOString(),runId:cfg.runId,cases:rows,cleanup,failure,sourcePins:cfg.sourcePins,fullW03Acceptance:false,applicationIntegrated:false,browserClientsTested:false,physicalDevicesTested:false,realParticipantDataUsed:false,liveFlagsChanged:false,secretValuesLogged:false};
 fs.writeFileSync(cfg.resultPath,JSON.stringify(report,null,2)+"\n",{flag:"wx",mode:0o600});
 console.log(JSON.stringify({state:report.state,passed:rows.length,cleanup:cleanup.length,failure,fullW03Acceptance:false}));
 if(failure)process.exitCode=1;
})();
