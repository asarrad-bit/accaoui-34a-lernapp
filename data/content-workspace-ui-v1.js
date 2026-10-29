/* W05 local editorial workspace. Public administration remains closed. */
(function(){
"use strict";
const A=window.ACCAOUI_CONTENT_WORKSPACE_V1;if(!A)return;
let dialog,repository,service,active=false,dirty=false,busy=false,revision=0,selected=null,selectedVersion=null,role="admin-a";
const local=["localhost","127.0.0.1","[::1]"].includes(location.hostname);
const $=id=>document.getElementById("content"+id+"V1");
const make=(tag,text,attrs={})=>{const n=document.createElement(tag);if(text!==null)n.textContent=text;for(const [k,v]of Object.entries(attrs))n.setAttribute(k,v);return n;};
function status(text,error=false){$("Status").textContent=text;$("Status").setAttribute("role",error?"alert":"status");}
function actor(){
 const s=repository.read();const courses=s.ok?s.state.courses.map(c=>c.id):[];
 return {id:role==="admin-a"?"demo-owner":role==="admin-b"?"demo-reviewer":role==="instructor"?"demo-teacher":"demo-participant",role:role.startsWith("admin")?"admin":role,active:true,courseIds:courses};
}
function download(name,text){const url=URL.createObjectURL(new Blob([text],{type:"application/json"}));const a=make("a","",{href:url,download:name});document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);}
function options(node,values){const keep=node.value;node.replaceChildren(make("option","Bitte auswählen",{value:""}),...values.map(v=>make("option",v.title||v.id,{value:v.id})));if([...node.options].some(o=>o.value===keep))node.value=keep;}
function renderBank(){const bank=$("Bank").value;for(const b of ["written","oral","card"])$("Fields-"+b).hidden=b!==bank;}
function newEntry(){selected=null;selectedVersion=null;$("EntryForm").reset();$("Id").readOnly=false;$("Bank").disabled=false;$("EntryCourse").disabled=false;$("ReviewDay").value=new Date().toISOString().slice(0,10);renderBank();dirty=false;}
async function refresh(){
 if(!active)return;const r=repository.read();if(!r.ok){status(r.error,true);return;}revision=r.state.revision;$("Revision").textContent="Gespeicherter Stand "+revision;
 const a=actor();$("EditArea").hidden=a.role==="participant";$("AdminArea").hidden=a.role!=="admin";
 const courses=r.state.courses.filter(c=>a.role!=="instructor"||c.instructorIds.includes(a.id));
 options($("EntryCourse"),courses);options($("PreviewCourse"),courses);options($("Source"),r.state.sources);
 $("CourseList").replaceChildren(...courses.map(c=>make("li",c.title+" · "+c.id+" · "+c.startDay+" bis "+c.endDay+" · "+c.status+" · Dozenten: "+(c.instructorIds.join(", ")||"keine"))));
 $("SourceList").replaceChildren(...r.state.sources.map(s=>make("li",s.title+" · "+s.id+" · "+s.usage+" · "+(s.ownerReviewed?"lokal bestätigt":"Prüfung offen"))));
 const entries=r.state.entries.filter(e=>courses.some(c=>c.id===e.courseId)).filter(e=>(!$("FilterBank").value||e.bank===$("FilterBank").value)&&(!$("FilterStatus").value||e.status===$("FilterStatus").value)&&e.question.toLocaleLowerCase("de").includes($("Search").value.toLocaleLowerCase("de")));
 $("Entries").replaceChildren(...entries.map(e=>{
  const li=make("li",null),title=make("strong",e.question),meta=make("p",e.id+" · "+e.bank+" · "+e.category+" · "+e.status+" · Version "+e.version);
  li.append(title,meta);const button=make("button","Öffnen",{type:"button","data-entry-id":e.id});button.onclick=()=>loadEntry(e);li.append(button);return li;
 }));
 $("Count").textContent=entries.length+" Inhalte im gewählten lokalen Ausschnitt";
 $("Audit").replaceChildren(...r.state.audit.slice(-15).reverse().filter(x=>a.role==="admin"||x.actorId===a.id).map(x=>make("li",x.utc+" · "+x.actorId+" · "+x.action+" · "+x.entityId+" · Stand "+x.revision)));
}
function loadEntry(e){
 if(dirty&&!window.confirm("Ungespeicherte Eingabe verwerfen und diesen Inhalt öffnen?"))return;
 selected=e.id;selectedVersion=e.version;
 $("Id").value=e.id;$("Id").readOnly=true;$("Bank").value=e.bank;$("Bank").disabled=true;$("EntryCourse").value=e.courseId;$("EntryCourse").disabled=true;$("Source").value=e.sourceId;$("Category").value=e.category;$("Question").value=e.question;
 $("Answers").value=(e.answers||[]).join("\n");$("Correct").value=(e.correct||[]).map(i=>i+1).join(",");$("Points").value=e.points||1;$("Explanation").value=e.explanation||"";$("ModelAnswer").value=e.modelAnswer||"";$("FollowUps").value=e.followUps||"";$("Critical").value=e.criticalMistakes||"";$("Back").value=e.back||"";
 A.CHECKS.forEach(k=>$("Check-"+k).checked=false);$("ReviewDay").value=new Date().toISOString().slice(0,10);renderBank();dirty=false;status("Inhalt "+e.id+" geöffnet · "+e.status+" · Version "+e.version);
 $("Question").focus();
}
function value(){
 const bank=$("Bank").value;const e={id:$("Id").value.trim(),bank,courseId:$("EntryCourse").value,sourceId:$("Source").value,category:$("Category").value,question:$("Question").value.trim()};
 if(selectedVersion!==null)e.version=selectedVersion;
 if(bank==="written")Object.assign(e,{points:Number($("Points").value),answers:$("Answers").value.split("\n").map(s=>s.trim()).filter(Boolean),correct:$("Correct").value.split(",").map(s=>Number(s.trim())-1),explanation:$("Explanation").value.trim()});
 if(bank==="oral")Object.assign(e,{modelAnswer:$("ModelAnswer").value.trim(),followUps:$("FollowUps").value.trim(),criticalMistakes:$("Critical").value.trim()});
 if(bank==="card")e.back=$("Back").value.trim();
 return e;
}
async function run(fn,message){
 if(busy)return;busy=true;$("Status").setAttribute("aria-busy","true");
 const buttons=[...dialog.querySelectorAll("button")].map(b=>[b,b.disabled]);for(const [b]of buttons)b.disabled=true;
 try{await fn();dirty=false;await refresh();status(typeof message==="function"?message():message);return true;}catch(e){status(e.message||String(e),true);return false;}
 finally{for(const [b,disabled]of buttons)b.disabled=disabled;busy=false;$("Status").setAttribute("aria-busy","false");}
}
async function transition(target){
 if(!selected){status("Zuerst einen gespeicherten Inhalt öffnen.",true);return;}
 const review={day:$("ReviewDay").value,checks:Object.fromEntries(A.CHECKS.map(k=>[k,$("Check-"+k).checked]))};
 const saved=await run(()=>service.transition(selected,target,review,revision),"Lokaler Schritt gespeichert: "+target+". Die Teilnehmerbanken bleiben unverändert.");if(!saved)return;
 const r=repository.read();if(r.ok){const e=r.state.entries.find(x=>x.id===selected);if(e)selectedVersion=e.version;}
}
function open(){
 if(!dialog)build();dialog.showModal();$("Close").focus();
}
function build(){
 dialog=make("dialog",null,{id:"contentWorkspaceV1","aria-labelledby":"contentTitleV1"});
 dialog.innerHTML='<header><h2 id="contentTitleV1">Redaktion und Kurse</h2><button id="contentCloseV1" type="button">Schließen</button></header><p id="contentBoundaryV1">Der echte Redaktionszugang ist gesperrt, bis Anmeldung und serverseitige Rollen angebunden und geprüft sind.</p><div id="contentStartV1"><p>Auf diesem Rechner kannst du ausschließlich einen lokalen Arbeitsentwurf mit synthetischen Testrollen ausprobieren. Er veröffentlicht keine Inhalte in die Lern-App und verbindet keine Datenbank.</p><label><input id="contentConsentV1" type="checkbox"> Ich verwende ausschließlich eigene synthetische Testinhalte.</label><button id="contentEnableV1" type="button">Lokalen Arbeitsentwurf öffnen</button></div><p id="contentStatusV1" role="status" aria-live="polite"></p><div id="contentWorkspaceBodyV1" hidden><p class="content-local-note">Lokaler Arbeitsentwurf · Testrollen sind kein geschütztes Benutzerkonto. Fachliche Prüfung, Quellenfreigabe und echte Rollenabnahme bleiben offen.</p><label>Testrolle <select id="contentRoleV1"><option value="admin-a">Testadministration A</option><option value="admin-b">Testadministration B</option><option value="instructor">Testdozent</option><option value="participant">Testteilnehmer</option></select></label><span id="contentRevisionV1"></span><button id="contentReloadV1" type="button">Gespeicherten Stand laden</button><p>Ein Review und die Freigabe benötigen unterschiedliche Testpersonen. Alle Freigabeschritte gelten ausschließlich für diesen lokalen Entwurf.</p><div id="contentAdminAreaV1"><details><summary>Kurse und Dozentenzuordnung</summary><form id="contentCourseFormV1"><label>Kurs-ID <input id="contentCourseIdV1" required maxlength="80"></label><label>Kursname <input id="contentCourseTitleV1" required maxlength="200"></label><label>Beginn <input id="contentCourseStartV1" type="date" required></label><label>Ende <input id="contentCourseEndV1" type="date" required></label><label>Testdozenten-IDs, mit Komma getrennt <input id="contentInstructorsV1" value="demo-teacher"></label><label>Kursstatus <select id="contentCourseStatusV1"><option value="active">Aktiv</option><option value="archived">Archiviert</option></select></label><button type="submit">Kurs speichern</button></form><ul id="contentCourseListV1"></ul></details><details><summary>Quellen und Nutzungsprüfung</summary><p>Kein Drive-Import: Hier werden nur lokale Testangaben erfasst. Für echte Quellen muss der Eigentümer konkrete Dateien und Nutzungsrechte benennen.</p><form id="contentSourceFormV1"><label>Quellen-ID <input id="contentSourceIdV1" required maxlength="80"></label><label>Bezeichnung <input id="contentSourceTitleV1" required maxlength="200"></label><label>Fundstelle / Testreferenz <input id="contentLocatorV1" required maxlength="1000"></label><label>Nutzung <select id="contentUsageV1"><option value="unknown">Ungeklärt</option><option value="analysis">Nur Analyse</option><option value="own">Eigene Formulierung</option></select></label><label><input id="contentOwnerReviewedV1" type="checkbox"> Nutzungsprüfung im lokalen Test bestätigt</label><button type="submit">Quelle speichern</button></form><ul id="contentSourceListV1"></ul></details></div><div id="contentEditAreaV1"><details open><summary>Inhalt bearbeiten</summary><form id="contentEntryFormV1"><label>Inhalts-ID <input id="contentIdV1" required maxlength="80"></label><label>Banktyp <select id="contentBankV1"><option value="written">Schriftliche Frage</option><option value="oral">Mündliche Frage</option><option value="card">Lernkarte</option></select></label><label>Kurs <select id="contentEntryCourseV1" required></select></label><label>Quelle <select id="contentSourceV1" required></select></label><label>Sachgebiet <select id="contentCategoryV1" required></select></label><label>Frage / Vorderseite <textarea id="contentQuestionV1" required maxlength="12000"></textarea></label><div id="contentFields-writtenV1"><label>Antworten: je eine Zeile, vier oder fünf Optionen <textarea id="contentAnswersV1" maxlength="10000"></textarea></label><label>Richtige Antwortpositionen: 1 bis5, mit Komma getrennt <input id="contentCorrectV1" maxlength="8"></label><label>Punkte <select id="contentPointsV1"><option>1</option><option>2</option></select></label><label>Erklärung <textarea id="contentExplanationV1" maxlength="12000"></textarea></label></div><div id="contentFields-oralV1" hidden><label>Musterantwort <textarea id="contentModelAnswerV1" maxlength="12000"></textarea></label><label>Folgefragen <textarea id="contentFollowUpsV1" maxlength="12000"></textarea></label><label>Kritische Fehler <textarea id="contentCriticalV1" maxlength="12000"></textarea></label></div><div id="contentFields-cardV1" hidden><label>Rückseite <textarea id="contentBackV1" maxlength="12000"></textarea></label></div><button id="contentSaveV1" type="submit">Als Entwurf speichern</button><button id="contentNewV1" type="button">Neuer Inhalt</button></form><fieldset><legend>Lokale Review-Probe für den geöffneten Inhalt</legend><div id="contentChecksV1"></div><label>Prüfdatum <input id="contentReviewDayV1" type="date"></label><div class="content-actions"><button id="contentReviewV1" type="button">Review speichern</button><button id="contentApproveV1" type="button">Lokal freigeben</button><button id="contentPublishV1" type="button">Lokal veröffentlichen</button><button id="contentArchiveV1" type="button">Archivieren</button></div></fieldset></details><details><summary>Lokaler Entwurfsimport und Export</summary><p>Nur synthetisches JSON im Schema1; höchstens100 Einträge / 500 KB. Mitgebrachte Freigaben werden abgelehnt. Der Export ist immer ein Entwurf.</p><label>Importdatei <input id="contentImportFileV1" type="file" accept="application/json,.json"></label><button id="contentImportV1" type="button">Testentwürfe prüfen und importieren</button><button id="contentExportV1" type="button">Entwürfe des gewählten Kurses exportieren</button></details><label>Bankfilter <select id="contentFilterBankV1"><option value="">Alle Banktypen</option><option value="written">Schriftlich</option><option value="oral">Mündlich</option><option value="card">Lernkarten</option></select></label><label>Statusfilter <select id="contentFilterStatusV1"><option value="">Alle Zustände</option><option value="draft">Entwurf</option><option value="review">Review</option><option value="approved">Freigegeben</option><option value="published">Lokal veröffentlicht</option><option value="archived">Archiviert</option></select></label><label>Suche <input id="contentSearchV1" type="search"></label><p id="contentCountV1"></p><ul id="contentEntriesV1"></ul></div><details><summary>Teilnehmer-Vorschau des lokalen Entwurfs</summary><label>Kurs <select id="contentPreviewCourseV1"></select></label><label>Vorschautag <input id="contentPreviewDayV1" type="date"></label><button id="contentPreviewV1" type="button">Freigegebene Inhalte anzeigen</button><ul id="contentPreviewListV1"></ul></details><details><summary>Lokales Änderungsprotokoll</summary><ul id="contentAuditV1"></ul></details></div>';
 document.body.append(dialog);
 $("Start").hidden=!local;$("Close").onclick=()=>{if(!dirty||window.confirm("Ungespeicherte Eingabe verwerfen?")){dialog.close();dirty=false;}};
 dialog.addEventListener("cancel",e=>{if(dirty&&!window.confirm("Ungespeicherte Eingabe verwerfen?"))e.preventDefault();});
 dialog.addEventListener("input",e=>{if(e.target.closest("form"))dirty=true;});
 $("Enable").onclick=async()=>{
  if(!local||!$("Consent").checked){status("Den lokalen Testumfang zuerst bestätigen.",true);return;}
  const lock=navigator.locks?fn=>navigator.locks.request(A.KEY,fn):null;
  repository=A.createRepository({storage:localStorage,lock});service=A.createService({repository,resolveActor:async()=>active?actor():null});
  const r=repository.read();if(!r.ok){status(r.error,true);return;}active=true;$("Start").hidden=true;$("WorkspaceBody").hidden=false;
  $("Boundary").textContent="Echter Redaktionszugang bleibt gesperrt. Geöffnet ist ausschließlich der lokale Arbeitsentwurf.";
  $("Category").replaceChildren(...A.CATEGORIES.map(v=>make("option",v,{value:v})));
  const labels={facts:"Fachinhalt",duplicates:"Dubletten",rights:"Nutzungsrechte / keine Originalkopie",wording:"Eigene verständliche Formulierung",answer:"Antwortlogik",explanation:"Erklärung / Musterantwort",category:"Kategorie und Punkte"};
  $("Checks").replaceChildren(...A.CHECKS.map(k=>{const l=make("label",null),c=make("input",null,{type:"checkbox",id:"contentCheck-"+k+"V1"});l.append(c,document.createTextNode(labels[k]));return l;}));
  for(const field of ["CourseStart","CourseEnd","ReviewDay","PreviewDay"])$(field).value=new Date().toISOString().slice(0,10);
  await refresh();status("Lokaler Arbeitsentwurf geöffnet. Keine Inhalte werden in die Lern-App übernommen.");
 };
 $("Role").onchange=async()=>{role=$("Role").value;await refresh();status("Testrolle gewechselt. Kein echtes Benutzerkonto.");};
 $("Bank").onchange=renderBank;
 $("Reload").onclick=async()=>{await refresh();status("Gespeicherten Stand geladen. Zum Überschreiben eines geänderten Inhalts diesen zuerst erneut öffnen.");};
 $("New").onclick=()=>{if(!dirty||window.confirm("Ungespeicherte Eingabe verwerfen?"))newEntry();};
 $("CourseForm").onsubmit=async e=>{e.preventDefault();await run(()=>service.saveCourse({id:$("CourseId").value.trim(),title:$("CourseTitle").value.trim(),startDay:$("CourseStart").value,endDay:$("CourseEnd").value,status:$("CourseStatus").value,instructorIds:$("Instructors").value.split(",").map(s=>s.trim()).filter(Boolean)},revision),"Lokaler Kurs gespeichert.");};
 $("SourceForm").onsubmit=async e=>{e.preventDefault();await run(()=>service.saveSource({id:$("SourceId").value.trim(),title:$("SourceTitle").value.trim(),locator:$("Locator").value.trim(),usage:$("Usage").value,ownerReviewed:$("OwnerReviewed").checked},revision),"Lokale Quellenangabe gespeichert; betroffene Freigaben wurden zurückgesetzt.");};
 $("EntryForm").onsubmit=async e=>{e.preventDefault();const v=value();const savedSuccessfully=await run(()=>service.saveEntry(v,revision),"Inhalt als lokaler Entwurf gespeichert.");if(!savedSuccessfully)return;const r=repository.read();if(r.ok){const saved=r.state.entries.find(x=>x.id===v.id);if(saved){selected=saved.id;selectedVersion=saved.version;$("Id").readOnly=true;$("Bank").disabled=true;$("EntryCourse").disabled=true;}}};
 for(const [id,target]of [["Review","review"],["Approve","approved"],["Publish","published"],["Archive","archived"]])$(id).onclick=()=>transition(target);
 for(const n of ["FilterBank","FilterStatus","Search"])$(n).addEventListener("input",()=>refresh());
 $("Preview").onclick=async()=>{let count=0;$("PreviewList").replaceChildren();await run(async()=>{const entries=await service.published($("PreviewCourse").value,$("PreviewDay").value);count=entries.length;$("PreviewList").replaceChildren(...entries.map(e=>make("li",e.bank+" · "+e.question)));},()=>count+" lokal veröffentlichte Inhalte in der Vorschau.");};
 $("Import").onclick=async()=>{const file=$("ImportFile").files[0];if(!file||file.size>500000){status("Eine synthetische JSON-Datei bis500 KB auswählen.",true);return;}await run(async()=>service.importDrafts(await file.text(),revision),"Lokale Testentwürfe atomar importiert.");};
 $("Export").onclick=async()=>{try{const json=await service.exportDrafts($("EntryCourse").value);download("accaoui-local-drafts.json",json);status("Lokale Entwurfsdatei erstellt; keine Veröffentlichungsbefugnis.");}catch(e){status(e.message,true);}};
}
document.addEventListener("click",e=>{if(e.target.closest("#contentAdminOpenV1"))open();});
window.addEventListener("storage",e=>{if(active&&e.key===A.KEY&&dialog?.open)status("Der Entwurf wurde in einem anderen Fenster geändert. Die Eingabe bleibt erhalten; vor dem Speichern aktuellen Stand laden und Inhalt prüfen.",true);});
})();
