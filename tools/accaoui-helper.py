import os, subprocess, sys
from pathlib import Path

ALLOW = sys.argv[1] if len(sys.argv) > 1 else ""

def run(cmd, env=None):
    print("\n$ " + " ".join(cmd))
    p = subprocess.run(cmd, env=env)
    if p.returncode != 0:
        sys.exit(p.returncode)

root = Path.cwd()
master = root / "docs" / "PROJECT_MASTERLIST.md"

if master.exists():
    for line in master.read_text(encoding="utf-8").splitlines():
        if line.startswith("Stand:"):
            print(line)
            break

env = os.environ.copy()
if ALLOW:
    env["ACCAOUI_ALLOW_PROTECTED"] = ALLOW
    print("ACCAOUI_ALLOW_PROTECTED=" + ALLOW)

run(["py", "-3", "tools/check-supabase-migrations.py"], env=env)
run(["py", "-3", "tools/preflight.py"], env=env)
run(["git", "diff", "--check"])
run(["git", "status", "--short"])
