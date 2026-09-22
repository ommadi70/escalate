from flask import Flask, render_template, jsonify, request
from orchestrator import Orchestrator

app = Flask(__name__)
orch = Orchestrator()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/state")
def get_state():
    df = orch.get_agent_state_df()
    return jsonify({
        "agents": df.to_dict(orient="records"),
        "metrics": {
            "active": sum(1 for a in orch.agents if a.status != "Idle"),
            "total": len(orch.agents),
            "reservations": orch.reservations,
            "conflicts": orch.conflicts
        },
        "resources": orch.resources,
        "events": orch.events
    })

@app.route("/api/sync", methods=["POST"])
def sync_offline_data():
    global orch 
    actions = request.json.get("actions", [])
    
    for action in actions:
        if action == "/api/tick":
            orch.run_tick()
        elif action == "/api/crisis":
            orch.inject_crisis()
        elif action == "/api/reset":
            orch = Orchestrator()
            
    if actions:
        orch.events.insert(0, f"📡 SYNCED: {len(actions)} offline actions reconciled.")
        orch.events = orch.events[:6]
        
    return get_state()

@app.route("/api/tick", methods=["POST"])
def tick():
    orch.run_tick()
    return jsonify({"status": "success"})

@app.route("/api/crisis", methods=["POST"])
def crisis():
    orch.inject_crisis()
    return jsonify({"status": "success"})

@app.route("/api/reset", methods=["POST"])
def reset():
    global orch
    orch = Orchestrator() 
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)