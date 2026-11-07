from datetime import datetime, timezone
import uuid
from core.fixer import apply_fix, reset_code
from core.test_runner import run_tests

def stamp(): return datetime.now(timezone.utc).isoformat(timespec="seconds")

class Workflow:
    def __init__(self, base, store): self.base, self.store = base, store
    def event(self, x, actor, message, kind="activity"):
        x.setdefault("timeline",[]).append({"at":stamp(),"actor":actor,"message":message,"kind":kind})
    def save(self,x): x["updated_at"]=stamp(); return self.store.save(x)
    def create(self,title,desc):
        x={"id":"RX-"+uuid.uuid4().hex[:6].upper(),"title":title,"description":desc,
           "severity":"Pending","category":"Unclassified","status":"reported","created_at":stamp(),
           "updated_at":stamp(),"owner":"Unassigned","root_cause":"","recommendation":"",
           "approval":None,"test_runs":[],"fix_applied":False,"timeline":[]}
        self.event(x,"You","Incident submitted to ResolveX.")
        return self.store.save(x)
    def action(self,iid,action,data):
        x=self.store.get(iid)
        if not x: return None,"Incident not found"
        if action=="triage":
            t=(x["title"]+" "+x["description"]).lower()
            if any(w in t for w in ("checkout","payment","cart","purchase","order")):
                x.update(category="Checkout & Payments",severity="High",owner="Checkout Squad")
            elif any(w in t for w in ("login","auth","password","session")):
                x.update(category="Authentication",severity="High",owner="Identity Squad")
            elif any(w in t for w in ("slow","latency","timeout")):
                x.update(category="Performance",severity="Medium",owner="Platform Squad")
            else: x.update(category="Application / General",severity="Medium",owner="Engineering")
            x["status"]="triaged"; self.event(x,"Triage Agent",f"Classified {x['category']} · {x['severity']} severity.")
        elif action=="investigate":
            if x["status"]=="reported": return None,"Run triage before investigation."
            t=(x["title"]+" "+x["description"]).lower()
            if any(w in t for w in ("checkout","cart","payment","purchase")):
                x["root_cause"]="Sample checkout applies a shipping fee even when subtotal qualifies for free shipping."
                x["recommendation"]="Return zero shipping for eligible orders, then run checkout regression tests."
            else:
                x["root_cause"]="Insufficient repository-specific evidence for a confident root-cause claim."
                x["recommendation"]="Attach logs, environment details and a minimal reproduction."
            x["status"]="investigated"; self.event(x,"Investigation Agent","First-pass repository analysis completed.")
        elif action=="tests":
            r=run_tests(self.base); x["test_runs"].append({"at":stamp(),**r})
            x["status"]="resolved" if r["failed"]==0 and x["fix_applied"] else "testing"
            self.event(x,"Test Runner",f"Actual pytest result: {r['passed']} passed, {r['failed']} failed.",
                       "success" if r["failed"]==0 else "warning")
        elif action=="approve":
            if x["status"] not in ("investigated","testing"): return None,"Investigate before approval."
            if data.get("approved") is not True: return None,"Explicit approval is required."
            who=str(data.get("approver","Team Lead"))[:80]
            x["approval"]={"approved":True,"approver":who,"at":stamp()}
            self.event(x,who,"Approved the proposed fix for the isolated demo repository.","success")
        elif action=="fix":
            if not x.get("approval",{}).get("approved"): return None,"Human approval is required before applying a code change."
            if x["fix_applied"]: return None,"Fix already applied. Reset demo to replay."
            ok,msg=apply_fix(self.base)
            if not ok: return None,msg
            x["fix_applied"]=True; x["status"]="fix_applied"
            self.event(x,"Codex Fix Agent (demo adapter)",msg,"success")
        else: return None,"Unknown workflow action."
        return self.save(x),None
    def reset(self): reset_code(self.base)
    def demo_status(self):
        code=(self.base/"demo_service"/"checkout.py").read_text(encoding="utf-8")
        return {"bug_present":"shipping = 49 if subtotal < 500 else 49" in code,
                "fix_applied":"shipping = 0 if subtotal >= 500 else 49" in code}
