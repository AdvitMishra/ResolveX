# ResolveX AI
### From incident report to verified fix — with humans and AI agents working together.

**Team:** AURQENT | **Track:** Flip the Switch Hackathon — Track 01: Best Business Workflow

ResolveX is a hackathon MVP for coordinating software incident work. A human reports a bug, a triage role classifies it, an investigation role gathers repository evidence, a Codex-powered coding role proposes a fix and runs tests, and a human approves before irreversible actions.

## What is included
- Responsive premium incident-command dashboard.
- Flask API and local JSON incident history.
- Working deterministic local triage and investigation adapters.
- Isolated sample checkout service with a reproducible free-shipping bug.
- Real pytest subprocess execution and captured output.
- Explicit human approval gate; patch endpoint refuses to run without approval.
- Safe exact-line patcher that refuses to overwrite unexpected source.
- Reset/replay controls.
- Switch room template with two agent roles, aliases, room instructions and approval role.

## Honest operating modes
**Local demo mode:** triage/investigation are deterministic local adapters. The demo fix adapter applies a pre-defined patch only to the isolated sample service after human approval. It works without API keys.

**Live Switch mode:** import `switch/resolvex-room.yaml` in Switch Console, connect Codex, select the agent locations and working directories, start both sessions, then run the incident conversation in the Switch room. The live Codex agent should inspect and change the repository itself. The dashboard intentionally displays "Not connected yet"; it does not fake Switch connectivity or live agent output.

## Windows quick start
Requires Python 3.10+.

```powershell
cd ResolveX_AI
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5050

If activation is blocked in this terminal:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Reproduce the full local demo
1. Click **New incident**.
2. Title: `Checkout applies shipping to eligible orders`
3. Description: `Orders with a subtotal of INR 500 or more should have free shipping, but checkout still adds INR 49.`
4. Run triage, then investigation.
5. Run tests. Expected before fix: **2 passed, 2 failed**.
6. Click **Human approve** and enter approver name.
7. Apply approved fix.
8. Run tests again. Expected: **4 passed** and status resolved.
9. Reset demo to restore the original defect.

The sample fixture is isolated; it does not connect to a real payment service.

## Configure Switch
1. Install Switch Console and Docker Desktop.
2. Install and sign in to Codex.
3. Add the official Switch docs MCP server:
   `codex mcp add switch-docs --url https://docs.switchagents.ai/mcp`
4. Open Switch Console and confirm the Codex provider is signed in.
5. Import `switch/resolvex-room.yaml`; select bridge/provider and agent locations/directories.
6. Set the fix agent's working directory to this project repository; keep the triage directory separate.
7. Create the room and start both agent sessions. A room member without a running session is not an active agent.
8. Use `switch/ROOM_INSTRUCTIONS.md` to run the incident workflow. Keep `auto_approve: false`.

Official links:
- Hackathon resources: https://www.wemakedevs.org/hackathons/switch/resources
- Switch docs: https://docs.switchagents.ai/
- Switch docs MCP: https://docs.switchagents.ai/mcp

## Architecture
```text
Human team -> Switch shared room -> Triage agent
                                -> Codex fix agent -> patch + tests
Human approver <- evidence + diff <- test result
ResolveX dashboard: incident history + local reproducible test evidence
```

Switch is the live human-agent collaboration layer; the dashboard is a companion interface for local incident tracking and reproducible evidence.

## API
- `GET /api/health`, `/api/summary`, `/api/incidents`, `/api/demo/status`
- `POST /api/incidents`
- `GET /api/incidents/<id>`
- `POST /api/incidents/<id>/triage|investigate|tests|approve|fix`
- `POST /api/demo/reset`

## Safety and limitations
This is a local hackathon MVP, not a production incident platform. The local adapters are not autonomous LLM agents. The app binds to `127.0.0.1`. The demo patcher edits only one known sample file after exact-line validation. No production deployment, merge, payment action or PR is performed. JSON storage is intended for a single-user demo. Dashboard events are not automatically ingested from Switch; live coordination takes place in the Switch room.

## Team AURQENT
- Purnashish: architecture, Switch/Codex setup, integration and final testing
- Avni: triage/investigation workflow
- Advit: sample service, reproduction and tests
- Nikhil: documentation, demo assets and presentation
