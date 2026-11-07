from pathlib import Path
import subprocess, sys, re

def run_tests(base):
    try:
        p=subprocess.run([sys.executable,"-m","pytest","-q","tests"],
                         cwd=str(Path(base)/"demo_service"), capture_output=True,
                         text=True, timeout=25)
        output=(p.stdout or "") + (("\n"+p.stderr) if p.stderr else "")
        line=next((x for x in output.splitlines() if " passed" in x or " failed" in x),"")
        passed=int((re.search(r"(\\d+) passed",line) or [0,0])[1])
        failed=int((re.search(r"(\\d+) failed",line) or [0,0])[1])
        if p.returncode and failed == 0: failed=1
        return {"returncode":p.returncode,"passed":passed,"failed":failed,"output":output.strip() or "No output"}
    except Exception as e:
        return {"returncode":1,"passed":0,"failed":1,"output":str(e)}
