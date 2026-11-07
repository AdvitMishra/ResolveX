from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
from core.store import Store
from core.workflow import Workflow

BASE = Path(__file__).resolve().parent
app = Flask(__name__, static_folder="static", static_url_path="/static")
store = Store(BASE / "data" / "incidents.json")
flow = Workflow(BASE, store)

@app.get("/")
def home():
    return send_from_directory(BASE / "static", "index.html")

@app.get("/api/health")
def health():
    return jsonify(ok=True, name="ResolveX AI", mode="local-demo", switch_connected=False)

@app.get("/api/summary")
def summary():
    items = store.all()
    return jsonify(total=len(items), open=sum(x["status"] != "resolved" for x in items),
                   resolved=sum(x["status"] == "resolved" for x in items),
                   high=sum(x["severity"] == "High" for x in items), incidents=items[:8])

@app.get("/api/incidents")
def incidents():
    return jsonify(store.all())

@app.post("/api/incidents")
def create():
    d = request.get_json(silent=True) or {}
    title, desc = str(d.get("title", "")).strip(), str(d.get("description", "")).strip()
    if len(title) < 4 or len(desc) < 8:
        return jsonify(error="Enter a clear title and at least 8 characters of detail."), 400
    return jsonify(flow.create(title, desc)), 201

@app.get("/api/incidents/<iid>")
def detail(iid):
    item = store.get(iid)
    return (jsonify(item), 200) if item else (jsonify(error="Incident not found"), 404)

@app.post("/api/incidents/<iid>/<action>")
def action(iid, action):
    d = request.get_json(silent=True) or {}
    result, error = flow.action(iid, action, d)
    return (jsonify(error=error), 409 if error else 200) if error else jsonify(result)

@app.post("/api/demo/reset")
def reset():
    flow.reset()
    return jsonify(ok=True, message="Sample checkout bug restored.")

@app.get("/api/demo/status")
def demo_status():
    return jsonify(flow.demo_status())

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=False)
