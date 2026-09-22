import random

AGENT_DB = {
    "Research Agent": {"LLM": 0.5, "Search": 0.3, "Database": 0.1, "Idle": 0.1},
    "Coding Agent": {"Python": 0.5, "GPU": 0.3, "Storage": 0.1, "Idle": 0.1},
    "Report Agent": {"Database": 0.4, "LLM": 0.3, "Storage": 0.2, "Idle": 0.1},
    "Data Agent": {"GPU": 0.4, "Python": 0.4, "Database": 0.1, "Idle": 0.1},
    "Customer Agent": {"Search": 0.5, "Database": 0.3, "LLM": 0.1, "Idle": 0.1}
}

class Agent:
    def __init__(self, agent_id, urgency, criticality):
        self.agent_id = agent_id
        self.resource_profile = AGENT_DB[agent_id]
        
        self.urgency = urgency  
        self.criticality = criticality 
        self.waiting_time = 0 
        self.recently_allocated = False
        self.current_score = 0.0
        
        self.current_request = None
        self.status = "Idle"
        self.pick_next_resource()

    def pick_next_resource(self):
        resources = list(self.resource_profile.keys())
        weights = list(self.resource_profile.values())
        choice = random.choices(resources, weights=weights, k=1)[0]
        
        if choice == "Idle":
            self.current_request = None
            self.status = "Idle"
        else:
            self.current_request = choice
            self.status = "Waiting"

    def get_current_resource(self):
        return self.current_request

def create_mock_agents():
    return [
        Agent("Research Agent", urgency="Low", criticality="Medium"),
        Agent("Coding Agent", urgency="High", criticality="High"),
        Agent("Report Agent", urgency="Medium", criticality="High"),
        Agent("Data Agent", urgency="Medium", criticality="High"),
        Agent("Customer Agent", urgency="High", criticality="Low")
    ]