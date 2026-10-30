/* Participant account UI. Uses only an already supplied client; public live/init flags remain off. */
(function(root,doc){
"use strict";
if(!root||!doc||root.ACCAOUI_PARTICIPANT_SESSION_V1!==undefined)return;
const MODE="accaoui_participant_mode_v1",COURSE="accaoui_participant_course_v1";
let pageRequested=false,modeFailure=false;
try{const mode=root.sessionStorage.getItem(MODE);pageRequested=mode!==null;modeFailure=mode!==null&&mode!=="account";}catch{pageRequested=true;modeFailure=true;}
let controller=null,bootPromise=null,mounted=false,busy=false,courseSignature="",viewError="",viewErrorCode=null,unavailable=false,lastReadyStamp=null;
const nodes={};
const messages={
 client_unavailable:"Der Kontozugang ist hier noch nicht eingerichtet. Ihr lokaler Lernstand bleibt erhalten.",
 durable_storage_required:"Dieser Browser kann den Kontostand derzeit nicht sicher speichern. Bitte verwenden Sie einen Browser mit zugelassenem lokalem Speicher.",
 mode_unreadable:"Die Zuordnung dieses Browsers konnte nicht sicher gelesen werden. Vorhandene Daten werden nicht überschrieben.",
 local_guard_blocked:"Der Zugang ist derzeit gesperrt. Bitte klären Sie die angezeigte Zugangsbeschränkung.",
 no_active_course:"Für dieses Konto ist derzeit kein aktiver Kurs freigegeben.",
 credentials_invalid:"Bitte geben Sie E-Mail-Adresse und Passwort ein.",
 sign_in_failed:"Die Anmeldung ist fehlgeschlagen. Bitte prüfen Sie Ihre Eingaben.",
 auth_error:"Die Anmeldung konnte nicht bestätigt werden. Bitte versuchen Sie es erneut.",
 auth_required:"Die Anmeldung muss erneut bestätigt werden. Ihr gesicherter Stand bleibt erhalten.",
 session_missing:"Bitte melden Sie sich mit Ihrem Teilnehmerkonto an.",
 session_invalid:"Die Anmeldung konnte nicht bestätigt werden. Bitte melden Sie sich erneut an.",
 account_changed:"Die Anmeldung hat sich geändert. Die bisherige Ansicht wurde gesperrt; gesicherte Eingaben bleiben dem bisherigen Konto zugeordnet.",
 access_denied:"Der Kurszugang ist derzeit nicht freigegeben. Ihre bereits gesicherten Eingaben bleiben erhalten.",
 course_not_available:"Bitte wählen Sie einen freigegebenen Kurs.",
 transport_error:"Der Kontostand konnte noch nicht übertragen werden. Ihre Eingaben bleiben lokal gesichert. Sobald die Verbindung verfügbar ist, können Sie erneut synchronisieren.",
 cache_unavailable:"Die letzten Eingaben sind noch nicht sicher im Browser gespeichert. Bitte schließen oder wechseln Sie diese Seite noch nicht. Sie können den Stand herunterladen und die Speicherung erneut versuchen.",
 cache_unconfirmed:"Die Speicherung konnte nicht bestätigt werden. Vorhandene Daten bleiben erhalten.",
 session_expired:"Die Sitzung oder der Kurszugang ist abgelaufen. Bitte melden Sie sich erneut an. Gesicherte Eingaben bleiben erhalten.",
 conflict:"Es gibt einen anderen Kontostand. Ihre Eingaben wurden erhalten. Bitte wählen Sie ausdrücklich, welcher Stand weiterverwendet werden soll.",
 invalid_cache:"Der gespeicherte Stand konnte nicht gelesen werden. Die ursprünglichen Daten bleiben erhalten.",
 invalid_state:"Der gespeicherte Stand konnte nicht sicher zugeordnet werden. Die ursprünglichen Daten bleiben erhalten.",
 cache_scope_mismatch:"Der gespeicherte Stand gehört nicht zur aktuellen Konto- und Kurszuordnung. Er wird hier nicht angezeigt oder übernommen.",
 server_version_regressed:"Der Kontostand hat eine unerwartete ältere Version. Die lokale Speicherung bleibt erhalten; bitte wählen Sie die Wiederherstellung ausdrücklich.",
 server_version_mismatch:"Die gespeicherten Versionen stimmen nicht sicher überein. Der bisherige Stand bleibt erhalten.",
 pending_input_requires_sync:"Es liegen noch ausstehende Eingaben vor. Bitte synchronisieren oder klären Sie zuerst den angezeigten Konflikt.",
 sign_out_failed:"Die Abmeldung konnte nicht bestätigt werden. Bitte versuchen Sie es erneut.",
 invalid_document:"Diese Eingabe konnte nicht sicher gespeichert werden. Der bisherige Stand bleibt erhalten.",
 session_locked:"Der Kontostand ist gesperrt. Bitte bestätigen Sie Ihre Anmeldung erneut.",
 reloading:"Der gesicherte Kontostand wird geöffnet.",
 sync_in_progress:"Die Übertragung läuft noch. Bitte warten Sie kurz.",
 pending_form_input:"Bitte speichern Sie zuerst Ihre noch offenen Eingaben im Lernplan oder bei den Prüfungsterminen. Ihre Eingaben bleiben geöffnet.",
 explicit_import_required:"Bitte bestätigen Sie zuerst die gewünschte Übernahme des lokalen Lernstands."
};
function text(code){return messages[code]||"Der Vorgang konnte nicht sicher abgeschlossen werden. Ihre gespeicherten Daten bleiben erhalten.";}
function error(code){const e=new Error(code);e.code=code;throw e;}
function localAllowed(){if(typeof root.getCurrentAccessState==="function"&&root.getCurrentAccessState().isAllowed!==true)error("local_guard_blocked");}
function ensure(){
 localAllowed();if(modeFailure)error("mode_unreadable");if(controller)return controller;
 const client=root.ACCAOUI_SUPABASE_BOOTSTRAP?.getClient?.();if(!client)error("client_unavailable");
 if(!root.ACCAOUI_PARTICIPANT_SESSION_FACTORY_V1||!root.ACCAOUI_PARTICIPANT_PROGRESS_V1)error("client_unavailable");
 controller=root.ACCAOUI_PARTICIPANT_SESSION_FACTORY_V1.create({model:root.ACCAOUI_PARTICIPANT_PROGRESS_V1,createAuthAdapter:root.ACCAOUI_PARTICIPANT_AUTH_SESSION_ADAPTER_FACTORY,createAccessAdapter:root.ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY,client,cache:root.localStorage,tabStorage:root.sessionStorage,locks:root.navigator.locks,now:()=>Date.now(),newId:()=>root.crypto.randomUUID(),setTimer:(fn,ms)=>root.setTimeout(fn,ms),clearTimer:id=>root.clearTimeout(id)});
 controller.subscribe(render);return controller;
}
function element(tag,id,label){const e=doc.createElement(tag);if(id)e.id=id;if(label!==undefined)e.textContent=label;return e;}
function button(id,label,parent){const b=element("button",id,label);b.type="button";parent.appendChild(b);nodes[id]=b;return b;}
function field(form,id,label,type){const l=element("label",null,label),input=element("input",id);l.htmlFor=id;input.type=type;input.required=true;form.append(l,input);nodes[id]=input;return input;}
function visible(node,show){node.hidden=!show;}
function status(){return controller?.status()||{phase:"idle",code:null,courses:[],durable:true,dirty:false};}
function showDialog(){if(!mounted)return;if(!nodes.dialog.open)nodes.dialog.showModal();}
function gateNavigation(){const locked=pageRequested&&status().phase!=="ready";for(const id of ["mobileBottomNavV227","mobileMoreSheetV227","mobileMoreBackdropV227"]){const node=doc.getElementById(id);if(node){node.hidden=locked;node.inert=locked;}}const editor=doc.getElementById("contentAdminOpenV1");if(editor&&pageRequested)editor.hidden=true;}
function render(){
 if(!mounted)return;
 const s=status(),ready=s.phase==="ready",layout=doc.querySelector(".layout");
 if(ready&&s.durable&&!s.dirty&&!s.code&&["transport_error","cache_unavailable","cache_unconfirmed"].includes(viewErrorCode)){viewError="";viewErrorCode=null;}
 if(pageRequested&&layout){layout.hidden=!ready;layout.inert=!ready;}
 gateNavigation();
 const title=s.courses.find(c=>c.id===s.courseId)?.title;
 nodes.summary.textContent=ready?(title?"Konto · "+title:"Teilnehmerkonto"):pageRequested?"Teilnehmerkonto":"Lokaler Lernstand";
 let message=viewError||(s.code?text(s.code):"");
 if(!message&&ready)message=s.syncInProgress?"Der Stand wird übertragen.":s.dirty?"Ihre Eingaben sind in diesem Browser gesichert; die Übertragung steht noch aus.":"Ihr Kontostand ist aktuell.";
 if(!message&&s.phase==="choose_course")message=s.courses.length?"Bitte wählen Sie Ihren Kurs.":text("no_active_course");
 if(!message&&["authenticating","loading"].includes(s.phase))message="Ihr Zugang und Ihr Kontostand werden geladen.";
 nodes.message.textContent=message;nodes.banner.textContent=ready?message:pageRequested?message||"Kontostand wird geladen.":"In diesem Browser gespeichert";
 nodes.banner.dataset.state=!s.durable?"error":s.code==="conflict"?"conflict":s.dirty?"pending":"ready";
 visible(nodes.login,s.phase==="login"&&!unavailable);visible(nodes.courseForm,["choose_course","ready"].includes(s.phase)&&s.courses.length>0);
 visible(nodes.active,ready);visible(nodes.conflict,ready&&s.code==="conflict");visible(nodes.recovery,s.phase==="recovery_required");visible(nodes.retry,(s.phase==="locked"&&s.code!=="reloading")||(s.phase==="login"&&["transport_error","auth_error"].includes(s.code)));
 visible(nodes.close,!pageRequested||ready);visible(nodes.logout,controller!==null&&!["idle","authenticating","loading"].includes(s.phase));
 nodes.courseSubmit.textContent=pageRequested&&ready?"Kurs wechseln":"Konto öffnen";
 nodes.courseSubmit.disabled=busy||!s.durable;
 const signature=JSON.stringify(s.courses);
 if(signature!==courseSignature){const prior=nodes.course.value;nodes.course.replaceChildren();for(const c of s.courses){const option=element("option",null,c.title);option.value=c.id;nodes.course.appendChild(option);}if(s.courses.some(c=>c.id===prior))nodes.course.value=prior;else if(s.courseId)nodes.course.value=s.courseId;courseSignature=signature;}
 for(const b of nodes.dialog.querySelectorAll("button")){if(b!==nodes.close)b.disabled=busy;}
 nodes.courseSubmit.disabled=busy||!s.durable;nodes.recoveryDownload.disabled=busy||s.code==="cache_scope_mismatch";
 nodes.sync.disabled=busy||s.code==="conflict";nodes.refresh.disabled=busy||s.dirty||!s.durable;
 if(pageRequested&&["login","choose_course","locked","recovery_required"].includes(s.phase)&&s.code!=="reloading")showDialog();
 if(!ready||s.dirty||!s.durable||s.code)lastReadyStamp=null;
 else if(pageRequested&&!s.syncInProgress){
  let draft=false;
  try{const storage=controller.storage();for(const [id,key]of [["examDateWrittenV1Input","accaoui_exam_date_written_v1"],["examDateOralV1Input","accaoui_exam_date_oral_v1"]]){const input=doc.getElementById(id);if(input&&input.value!==(storage.getItem(key)||""))draft=true;}const plan=doc.getElementById("learningGuidanceV1");if(plan?.hasUnsavedParticipantInputV1?.())draft=true;}catch{draft=true;}
  const stamp=s.ownerId+":"+s.courseId+":"+s.version;
  if(!draft&&stamp!==lastReadyStamp){lastReadyStamp=stamp;root.dispatchEvent(new CustomEvent("accaoui-progress-updated-v1"));}
 }
}
async function run(fn){
 if(busy)return;busy=true;viewError="";viewErrorCode=null;render();
 try{await fn();}catch(e){viewErrorCode=e.code;viewError=text(e.code);showDialog();}finally{busy=false;render();}
}
function prepareChange(requireDurable=true){
 if(typeof root.prepareParticipantScopeChangeV1==="function")root.prepareParticipantScopeChangeV1();
 if(requireDurable&&pageRequested&&controller?.status().durable!==true)error("cache_unavailable");
}
function selection(id){
 root.sessionStorage.setItem(COURSE,id);if(root.sessionStorage.getItem(COURSE)!==id)error("cache_unconfirmed");
 root.sessionStorage.setItem(MODE,"account");if(root.sessionStorage.getItem(MODE)!=="account")error("cache_unconfirmed");
}
function reload(){root.location.reload();}
function backup(){
 const raw=ensure().backup();if(typeof raw!=="string")error("invalid_cache");
 const blob=new Blob([raw],{type:"application/json"}),url=URL.createObjectURL(blob),a=element("a");
 a.href=url;a.download="accaoui-mein-lernstand-"+new Date().toISOString().slice(0,10)+".json";doc.body.appendChild(a);a.click();a.remove();root.setTimeout(()=>URL.revokeObjectURL(url),10000);
}
async function openDialog(){
 mount();if(typeof root.closeMobileMoreMenuV227==="function")root.closeMobileMoreMenuV227();showDialog();await run(async()=>{const c=ensure();unavailable=false;if(["idle","login"].includes(c.status().phase))await c.resolveSession();});
}
function mount(){
 if(mounted)return;mounted=true;
 const sidebar=doc.querySelector(".sidebar"),tools=element("section","participantAccountToolsV1");tools.className="participant-account-tools-v1";
 button("participantAccountOpenV1","Mein Konto",tools).addEventListener("click",()=>openDialog());
 nodes.banner=element("p","participantAccountStatusV1");nodes.banner.setAttribute("role","status");nodes.banner.setAttribute("aria-live","polite");tools.appendChild(nodes.banner);(sidebar||doc.body).appendChild(tools);
 function placeTools(){const mobile=root.matchMedia("(max-width: 820px)").matches,grid=doc.querySelector("#mobileMoreSheetV227 .mobile-more-grid-v227"),target=mobile&&grid?grid:sidebar||doc.body;if(tools.parentNode!==target)target.appendChild(tools);gateNavigation();}
 root.addEventListener("resize",placeTools);if(typeof root.MutationObserver==="function"){const observer=new root.MutationObserver(placeTools);observer.observe(doc.body,{childList:true});}placeTools();
 const dialog=element("dialog","participantAccountDialogV1");dialog.className="participant-account-dialog-v1";dialog.setAttribute("aria-labelledby","participantAccountTitleV1");nodes.dialog=dialog;
 dialog.appendChild(element("h2","participantAccountTitleV1","Mein Lernkonto"));nodes.summary=element("p","participantAccountSummaryV1");dialog.appendChild(nodes.summary);
 nodes.message=element("p","participantAccountMessageV1");nodes.message.setAttribute("role","status");nodes.message.setAttribute("aria-live","polite");dialog.appendChild(nodes.message);
 const login=element("form","participantAccountLoginV1");nodes.login=login;
 const email=field(login,"participantAccountEmailV1","E-Mail-Adresse","email");email.autocomplete="username";
 const password=field(login,"participantAccountPasswordV1","Passwort","password");password.autocomplete="current-password";
 const signIn=button("participantAccountSignInV1","Anmelden",login);signIn.type="submit";
 login.addEventListener("submit",event=>{event.preventDefault();run(async()=>{await ensure().signIn({email:email.value,password:password.value});password.value="";});});dialog.appendChild(login);
 const courseForm=element("form","participantAccountCourseFormV1"),label=element("label",null,"Kurs");label.htmlFor="participantAccountCourseV1";nodes.course=element("select","participantAccountCourseV1");courseForm.append(label,nodes.course);
 nodes.courseForm=courseForm;nodes.courseSubmit=button("participantAccountCourseOpenV1","Konto öffnen",courseForm);nodes.courseSubmit.type="submit";
 courseForm.addEventListener("submit",event=>{event.preventDefault();run(async()=>{const c=ensure(),id=nodes.course.value;if(!c.status().courses.some(x=>x.id===id))error("course_not_available");prepareChange();
  if(pageRequested&&c.status().phase==="ready"){if(id===c.status().courseId){dialog.close();return;}c.quiesce();selection(id);reload();return;}
  await c.open(id);selection(id);if(pageRequested)c.quiesce();reload();
 });});dialog.appendChild(courseForm);
 const active=element("section","participantAccountActiveV1");nodes.active=active;
 nodes.sync=button("participantAccountSyncV1","Jetzt synchronisieren",active);nodes.sync.addEventListener("click",()=>run(async()=>{prepareChange(false);await ensure().flush();}));
 nodes.refresh=button("participantAccountRefreshV1","Kontostand neu laden",active);nodes.refresh.addEventListener("click",()=>run(async()=>{prepareChange();const c=ensure();await c.refresh();c.quiesce();reload();}));
 button("participantAccountDownloadV1","Stand herunterladen",active).addEventListener("click",()=>run(async()=>{try{prepareChange(false);}catch(e){if(e.code!=="cache_unavailable"||controller?.status().durable!==false)throw e;}backup();}));
 const conflict=element("section","participantAccountConflictV1");nodes.conflict=conflict;
 conflict.appendChild(element("p",null,"Der andere Kontostand und Ihre Eingaben werden nicht automatisch vermischt. Die Auswahl gilt für den gesamten Lernstand dieses Kurses."));
 button("participantAccountUseLocalV1","Meine Eingaben weiterverwenden",conflict).addEventListener("click",()=>run(async()=>{prepareChange();ensure().resolveConflict("local");await ensure().flush();}));
 button("participantAccountUseRemoteV1","Anderen Kontostand übernehmen",conflict).addEventListener("click",()=>run(async()=>{prepareChange();const c=ensure();c.resolveConflict("remote");c.quiesce();reload();}));active.appendChild(conflict);
 const migration=element("details","participantAccountMigrationV1");migration.appendChild(element("summary",null,"Bisherigen lokalen Lernstand übernehmen"));
 migration.appendChild(element("p",null,"Der bisherige Stand dieses Browsers kann den Lernstand im gewählten Konto und Kurs ersetzen. Ihre ursprünglichen lokalen Daten bleiben erhalten. Laden Sie bei Bedarf vorher Ihren Kontostand herunter."));
 const migrationLabel=element("label"),migrationConfirm=element("input","participantAccountMigrationConfirmV1");migrationConfirm.type="checkbox";migrationLabel.append(migrationConfirm,doc.createTextNode(" Ich möchte den Kontostand durch eine Kopie des lokalen Lernstands ersetzen."));migration.appendChild(migrationLabel);
 button("participantAccountImportV1","Lokalen Stand übernehmen",migration).addEventListener("click",()=>run(async()=>{if(!migrationConfirm.checked)error("explicit_import_required");prepareChange();const c=ensure();c.importAnonymous("replace_account_with_anonymous_copy");migrationConfirm.checked=false;c.quiesce();reload();}));active.appendChild(migration);dialog.appendChild(active);
 const recovery=element("section","participantAccountRecoveryV1");nodes.recovery=recovery;
 recovery.appendChild(element("p",null,"Sie können den Kontostand in einer neuen lokalen Speicherung öffnen. Die bisherigen gespeicherten Daten bleiben dabei unverändert erhalten."));
 nodes.recoveryDownload=button("participantAccountRecoveryDownloadV1","Bisherigen Stand herunterladen",recovery);nodes.recoveryDownload.addEventListener("click",()=>run(async()=>backup()));
 button("participantAccountRecoverV1","Kontostand in neuer Speicherung öffnen",recovery).addEventListener("click",()=>run(async()=>{const c=ensure();await c.useServerCopy("new_cache_preserve_previous_bytes");c.quiesce();reload();}));dialog.appendChild(recovery);
 nodes.retry=button("participantAccountRetryV1","Anmeldung erneut prüfen",dialog);nodes.retry.addEventListener("click",()=>run(async()=>{if(status().durable!==true)error("cache_unavailable");reload();}));
 nodes.logout=button("participantAccountLogoutV1","Abmelden",dialog);nodes.logout.addEventListener("click",()=>run(async()=>{if(status().phase==="ready")prepareChange();await ensure().signOut();root.sessionStorage.removeItem(MODE);root.sessionStorage.removeItem(COURSE);reload();}));
 nodes.close=button("participantAccountCloseV1","Schließen",dialog);nodes.close.addEventListener("click",()=>dialog.close());dialog.addEventListener("cancel",event=>{if(pageRequested&&status().phase!=="ready")event.preventDefault();});
 doc.body.appendChild(dialog);render();
}
function boot(){
 if(!pageRequested)return Promise.resolve();if(bootPromise)return bootPromise;
 bootPromise=(async()=>{mount();await run(async()=>{const c=ensure();unavailable=false;await c.resolveSession();if(c.status().phase!=="choose_course")return;const id=root.sessionStorage.getItem(COURSE);if(c.status().courses.some(x=>x.id===id)){await c.open(id);if(c.status().phase==="ready"&&nodes.dialog.open)nodes.dialog.close();}});return status();})();
 return bootPromise;
}
const api=Object.freeze({requested:()=>pageRequested,ready:()=>controller?.status().phase==="ready",storage(){if(!pageRequested||!controller)error("session_locked");return controller.storage();},boot,status});
Object.defineProperty(root,"ACCAOUI_PARTICIPANT_SESSION_V1",{value:api,enumerable:true,writable:false,configurable:false});
if(doc.readyState==="loading")doc.addEventListener("DOMContentLoaded",mount,{once:true});else mount();
root.addEventListener("online",()=>{if(pageRequested&&controller?.status().phase==="ready")controller.flush().catch(()=>{});});
})(typeof window!=="undefined"?window:null,typeof document!=="undefined"?document:null);
