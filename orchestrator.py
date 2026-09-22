from agents import create_mock_agents
from predictor import predict_next_step, get_prediction_confidence
import pandas as pd

class Orchestrator:
    def __init__(self):
        self.agents = create_mock_agents()
        self.tick_count = 0
        self.conflicts = 0
        self.reservations = 0
        self.events = ["🟢 System Initialized", "🟢 Dynamic Additive engine online"]
        self.resources = {
            "LLM": {"used": 0, "total": 3},
            "GPU": {"used": 0, "total": 3},
            "Database": {"used": 0, "total": 2},
            "Python": {"used": 0, "total": 2},
            "Search": {"used": 0, "total": 2},
            "Storage": {"used": 0, "total": 2}
        }
        
    def get_agent_state_df(self):
        data = []
        for agent in self.agents:
            req = agent.get_current_resource()
            if agent.status == "Idle":
                current_task = "Idle (No request)"
            elif agent.status == "Waiting":
                current_task = f"Queued: {req}"
            else:
                current_task = f"Using: {req}"

            data.append({
                "Agent": agent.agent_id,
                "Score": round(agent.current_score, 1),
                "Urgency": agent.urgency,
                "Criticality": agent.criticality,
                "Current Service": current_task,
                "Predicted Next": predict_next_step(agent),
                "Probability": get_prediction_confidence(agent.agent_id, agent)
            })
        return pd.DataFrame(data)

    def run_tick(self):
        self.tick_count += 1
        self.events.insert(0, f"⏱️ Tick {self.tick_count} executed")
        self.conflicts = 0 
        self.reservations = 0
        
        for res in self.resources:
            self.resources[res]["used"] = 0
            
        def get_modifier(level):
            return 10 if level == "High" else 5 if level == "Medium" else 0

        for agent in self.agents:
            if agent.status == "Running":
                agent.waiting_time = 0
                agent.recently_allocated = True
                agent.pick_next_resource()
            elif agent.status == "Idle":
                agent.pick_next_resource()
            elif agent.status == "Waiting":
                agent.waiting_time += 2  
                agent.recently_allocated = False 
                
            if agent.status == "Waiting" and agent.current_request:
                prob_str = get_prediction_confidence(agent.agent_id, agent)
                prob_value = float(prob_str.strip('%'))
                urg_pts = get_modifier(agent.urgency)
                crit_pts = get_modifier(agent.criticality)
                penalty = 20 if agent.recently_allocated else 0
                agent.current_score = max(0, prob_value + urg_pts + crit_pts + agent.waiting_time - penalty)
            else:
                agent.current_score = 0.0
            
        sorted_agents = sorted(self.agents, key=lambda x: x.current_score, reverse=True)
        
        for agent in sorted_agents:
            if agent.status == "Idle" or not agent.current_request:
                continue
            req = agent.current_request
            if self.resources[req]["used"] < self.resources[req]["total"]:
                self.resources[req]["used"] += 1
                self.reservations += 1
                agent.status = "Running"
                self.events.insert(0, f"🟢 {agent.agent_id.split()[0]} (Score: {agent.current_score:.1f}) grabbed {req}")
            else:
                agent.status = "Waiting"
                self.events.insert(0, f"🟡 {agent.agent_id.split()[0]} safely queued for {req}")
        
        self.events = self.events[:6]

    def inject_crisis(self):
        self.events.insert(0, "🚨 CRISIS INJECTED: Resource pools slashed!")
        for res in self.resources:
            self.resources[res]["total"] = 1
        self.run_tick()