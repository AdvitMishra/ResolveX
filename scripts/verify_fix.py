import json, re, subprocess, sys, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"],
                   cwd=ROOT / "demo_service", capture_output=True, text=True)
out = r.stdout + r.stderr

def count(word):
    m = re.search(rf"(\d+) {word}", out)
    return int(m.group(1)) if m else 0

result = {
    "time": datetime.datetime.now().isoformat(timespec="seconds"),
    "passed": count("passed"),
    "failed": count("failed"),
    "verdict": "VERIFIED" if r.returncode == 0 else "NOT VERIFIED",
    "tail": out.strip().splitlines()[-6:],
}
(ROOT / "evidence").mkdir(exist_ok=True)
(ROOT / "evidence" / "last_run.json").write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
sys.exit(0 if r.returncode == 0 else 1)
