import random

def predict_next_step(agent):
    profile = agent.resource_profile
    top_resources = sorted([k for k in profile.keys() if k != "Idle"], key=lambda k: profile[k], reverse=True)
    return top_resources[0] if top_resources else "-"

def get_prediction_confidence(agent_id, agent):
    profile = agent.resource_profile
    predicted = predict_next_step(agent)
    base_probability = profile.get(predicted, 0.5) * 100
    noise = random.randint(-5, 10) 
    final_confidence = min(99, max(50, int(base_probability + noise)))
    return f"{final_confidence}%"