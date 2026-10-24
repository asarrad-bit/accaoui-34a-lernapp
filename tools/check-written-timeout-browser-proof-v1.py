#!/usr/bin/env python3
"""Independent W01 raw-evidence verifier. Synthetic self-tests never certify a real run."""
from pathlib import Path
import argparse,copy,datetime,hashlib,json,math,re,sys
CORE=("run-context.json","timer-trace.ndjson","browser-events.ndjson","console-events.ndjson","storage-snapshots.ndjson")
def require(ok,why):
    if not ok:raise ValueError(why)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def seconds(display):
    a,b=display.split(":");require(a.isdigit() and b.isdigit() and 0<=int(b)<60,"valid observed timer");return int(a)*60+int(b)
def parse_store(row,key,default=None):
    value=row["storage"].get(key)
    return default if value is None else json.loads(value)
def earned(q,selected):
    c=set(q["correct"]);s=set(selected)
    if not s or not s<=c:return 0
    return float(q["points"]) if s==c else (1 if float(q["points"])==2 and len(c)>=2 else 0)
def verify(root,allow_synthetic=False):
    root=Path(root).resolve();require(root.is_dir() and not root.is_symlink(),"regular private evidence directory")
    manifest=json.loads((root/"evidence-manifest.json").read_text(encoding="utf-8"))
    require(manifest["schema"]==1 and manifest["complete"] is True and manifest["status"]=="COMPLETE" and manifest["naturalClock"] is True and manifest["reconstructed"] is False,"complete natural prospective manifest")
    require([d["path"] for d in manifest["streams"]]==list(CORE),"exact five relative original core paths")
    raws={};streams={}
    for desc in manifest["streams"]:
        name=desc["path"];p=root/name
        require(p.is_file() and not p.is_symlink() and p.resolve().parent==root,"contained regular original stream")
        raw=p.read_bytes();raws[name]=raw
        require(len(raw)==desc["bytes"] and sha(raw)==desc["sha256"] and desc["complete"] is True,"full raw bytes/hash/complete "+name)
        text=raw.decode("utf-8",errors="strict")
        rows=[json.loads(line) for line in text.splitlines()] if name.endswith(".ndjson") else [json.loads(text)]
        require(rows and all(r["runId"]==manifest["runId"] for r in rows),"same real run identity "+name)
        times=[r["monotonic"] for r in rows]
        require(all(isinstance(t,(int,float)) and math.isfinite(t) for t in times) and times==sorted(times),"real nondecreasing monotonic stream "+name)
        for r in rows:datetime.datetime.fromisoformat(r["utc"].replace("Z","+00:00"))
        require(desc["utcStart"]==rows[0]["utc"] and desc["utcEnd"]==rows[-1]["utc"] and desc["monotonicStart"]==times[0] and desc["monotonicEnd"]==times[-1],"actual metadata spans "+name)
        streams[name]=rows
    context=streams[CORE[0]][0];timers=streams[CORE[1]];events=streams[CORE[2]];console=streams[CORE[3]];stores=streams[CORE[4]]
    require(allow_synthetic or not context.get("syntheticFixture",False),"synthetic fixture cannot be a real natural acceptance")
    require(context["task"]=="ACCAOUI_DEVELOPMENT_SEQUENCE_W01" and context["origin"]=="http://127.0.0.1:8765" and context["minimumNaturalSeconds"]==7200 and context["maximumSeconds"]==7800,"exact authorized task/origin/original budgets")
    require(context["captureBeforeNavigation"] is True and context["captureBeforeExamStart"] is True and context["clockManipulated"] is False and context["reconstructed"] is False and context["syntheticOnly"] is True and context["isolatedContext"] is True and context["liveSupabase"] is False,"unmodified clocks and isolated prospective capture")
    require(all(streams[n][0].get("kind")=="capture-opened" and streams[n][0]["beforeBrowserCreation"] is True for n in CORE[1:]),"all streams opened prospectively")
    kinds=lambda name:[r for r in events if r.get("kind")==name]
    one=lambda name:single(kinds(name),name)
    server=one("server-bound");browser=one("isolated-browser-created");nav=one("navigation-request")
    require(server["host"]=="127.0.0.1" and server["port"]==8765 and server["portClaimedExclusively"] is True and server["pid"]>0 and browser["cookiesAtCreation"]==0 and browser["syntheticOnly"] is True,"actual private server and empty isolated browser")
    require(context["monotonic"]<server["monotonic"]<browser["monotonic"]<nav["monotonic"],"capture/server/browser/navigation order")
    require(not any(r.get("kind") in {"fatal-error","manual-finish","forbidden-external-request","browser-page-crash"} for r in events),"no fatal/manual/foreign action")
    request=one("action-full-start-request");start=one("exam-start-ui");terminal=one("terminal-render");checked=one("terminal-state-checked");reload=one("reload-state-checked")
    require(start["target"]=="full-simulation-card" and terminal["automaticObservation"] is True and checked["automatic"] is True,"one observed UI start and automatic terminal")
    observed=[r for r in timers if r.get("kind")=="timer-observed"]
    require(len(observed)>=121 and observed[0]["display"]=="120:00" and observed[-1]["display"]=="00:00" and sum(r["display"]=="00:00" for r in observed)==1,"real 120:00 to one observed 00:00")
    values=[seconds(r["display"]) for r in observed]
    require(all(a>b for a,b in zip(values,values[1:])),"strictly natural descending observed countdown")
    require(all(b["monotonic"]-a["monotonic"]<=60 for a,b in zip(observed,observed[1:])),"timer observation gaps at most original 60s")
    zero=observed[-1]
    natural=zero["monotonic"]-request["monotonic"]
    renderer=(zero["pagePerformanceMs"]-start["pagePerformanceMs"])/1000
    require(zero["documentId"]==start["documentId"] and natural>=7200 and renderer>=7200,"independent actual host and renderer natural >=7200s")
    require(request["monotonic"]<=start["monotonic"]<=observed[0]["monotonic"] and zero["monotonic"]<=terminal["monotonic"]<=checked["monotonic"]<reload["monotonic"],"actual timer/terminal/reload order")
    require(manifest["monotonic"]-context["monotonic"]<=7800,"unchanged 7800s complete evidence budget")
    checkpoints=kinds("capture-checkpoint")
    require(len(checkpoints)>=121 and all(c["completePrefixRead"] is True and c["gapSeconds"]<=60 for c in checkpoints),"prospective flush/full readback at most 60s")
    for cp in checkpoints:
        require([f["path"] for f in cp["files"]]==list(CORE),"all core read at checkpoint")
        for f in cp["files"]:
            require(0<=f["bytes"]<=len(raws[f["path"]]) and sha(raws[f["path"]][:f["bytes"]])==f["sha256"],"actual fully read prefix checkpoint")
    snapshots={r["phase"]:r for r in stores if r.get("kind")=="storage-snapshot"}
    require({"before-exam","exam-start","synthetic-answers-set","natural-countdown","terminal","after-reload"}<=snapshots.keys(),"all original storage stages including natural/reload")
    rows=[r for r in stores if r.get("kind")=="storage-snapshot"]
    require(all(b["monotonic"]-a["monotonic"]<=60 for a,b in zip(rows,rows[1:])),"real storage observation gaps at most 60s")
    clean=snapshots["before-exam"]
    require(not clean["storage"].get("accaoui_active_session") and not clean["storage"].get("accaoui_exam_history"),"fresh synthetic storage")
    initial=parse_store(snapshots["exam-start"],"accaoui_active_session");answered=parse_store(snapshots["synthetic-answers-set"],"accaoui_active_session")
    final=parse_store(snapshots["terminal"],"accaoui_active_session");history=parse_store(snapshots["terminal"],"accaoui_exam_history",[])
    after=snapshots["after-reload"];history_after=parse_store(after,"accaoui_exam_history",[]);session_after=parse_store(after,"accaoui_active_session")
    require(initial["examType"]=="full" and initial["attemptStatus"]=="active" and initial["secondsLeft"]==7200 and snapshots["exam-start"]["timer"]=="120:00" and not initial["answers"],"actual full empty 120:00 start storage")
    require(len(initial["questions"])==82 and sum(float(q["points"]) for q in initial["questions"])==120 and len({q["id"] for q in initial["questions"]})==82,"82 unique actual questions and 120 possible points")
    require(initial["questions"]==answered["questions"]==final["questions"] and initial["attemptId"]==answered["attemptId"]==final["attemptId"],"same original shuffled questions/attempt")
    cases=one("grading-cases-bound")["cases"]
    require([c["kind"] for c in cases]==["full-one","full-two","partial-two","wrong"] and len({c["index"] for c in cases})==4,"four distinct genuine scoring cases")
    for c in cases:
        q=initial["questions"][c["index"]];actual=answered["answers"].get(str(c["index"]),[])
        require(sorted(actual)==sorted(c["selected"]) and earned(q,actual)==c["expected"],"actual persisted UI grading case "+c["kind"])
    require([c["expected"] for c in cases]==[1,2,1,0] and sum(c["expected"] for c in cases)==4,"full/partial/wrong oracle points")
    points=sum(earned(q,final["answers"].get(str(i),[])) for i,q in enumerate(final["questions"]))
    correct=sum(bool(final["answers"].get(str(i),[])) and set(final["answers"][str(i)])==set(q["correct"]) for i,q in enumerate(final["questions"]))
    open_count=sum(not final["answers"].get(str(i),[]) for i in range(82));wrong=82-correct-open_count
    require(points==4 and correct==2 and wrong==2 and open_count==78 and final["answers"]==answered["answers"] and final["attemptStatus"]=="completed" and final["secondsLeft"]==0,"all final open/full/partial/wrong answers unchanged and correct")
    require(len(history)==1 and history[0]["attemptId"]==initial["attemptId"] and history[0]["total"]==82 and history[0]["points"]["max"]==120 and history[0]["points"]["reached"]==points and history[0]["correct"]==correct and history[0]["wrong"]==wrong and history[0]["unanswered"]==open_count,"exactly one actual correctly graded history")
    require(checked["stats"]==dict(snapshots["terminal"]["stats"]) and all(checked["stats"].get(k)==v for k,v in {"Gesamtfragen":"82","Richtig":"2","Falsch":"2","Unbeantwortet":"78","Punkte":"4/120"}.items()),"actual terminal UI agrees")
    require(history_after==history and not after["timer"] and after["resultCount"]==0 and after["resumeOffered"] is False and (not session_after or session_after["attemptStatus"]=="completed") and reload["historyRecords"]==1 and reload["resumeOffered"] is False and reload["timerPresent"] is False,"reload preserves exactly one result and prevents false resume")
    require(not any(r.get("kind")=="page-error" or (r.get("kind")=="console-message" and r.get("level")=="error" and not (r.get("expectedOptional404") is True and "404" in r.get("text","") and str(r.get("location",{}).get("url","")).startswith(context["origin"]+"/data/supabase-config.local.js"))) for r in console),"all console/page errors observed; no unexpected error")
    return {"state":"CONTRACT_FIXTURE_VALIDATED" if context.get("syntheticFixture") else "REAL_NATURAL_BROWSER_PROOF_PASS","runId":context["runId"],"actualNaturalRun":not context.get("syntheticFixture",False),"naturalHostSeconds":natural,"naturalRendererSeconds":renderer,"timerObservations":len(observed),"checkpoints":len(checkpoints),"storageSnapshots":len(rows),"questionCount":82,"maxPoints":120,"points":points,"correct":correct,"wrong":wrong,"unanswered":open_count,"historyRecords":1,"originalFiveStreamsFullyReadAndHashed":True,"consoleMessages":sum(r.get("kind")=="console-message" for r in console),"expectedOptional404":sum(r.get("expectedOptional404") is True for r in console),"clockManipulated":False}
def single(rows,name):
    require(len(rows)==1,"exactly one "+name);return rows[0]
def main():
    parser=argparse.ArgumentParser();parser.add_argument("--verify",type=Path,required=True);args=parser.parse_args()
    try:print(json.dumps(verify(args.verify),ensure_ascii=False));return 0
    except Exception as exc:print(json.dumps({"state":"STOPP_NOT_VERIFIED","error":str(exc),"actualNaturalAcceptance":False},ensure_ascii=False));return 1
if __name__=="__main__":raise SystemExit(main())
