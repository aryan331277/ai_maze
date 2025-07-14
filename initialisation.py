import time
import random

shared_environment = {}

agent_alpha_id="agent_alpha"
agent_alpha_signal={
    "vector":[0.9, 0.3,-0.4],
    "status":"observing",
    "target_id":None
}

shared_environment[agent_alpha_id] = {
    "timestamp": time.time(),
    "signal_data": agent_alpha_signal
}




agent_beta_id = "agent_beta"
agent_beta_signal = {
    "vector": [0.9,0.3,-0.4], 
    "status": "ready_to_assist",
    "target_id": "agent_alpha" 
}

shared_environment[agent_beta_id] = {
    "timestamp": time.time(),
    "signal_data": agent_beta_signal
}


eval_agent_1_id = "agent_alpha"
eval_agent_2_id = "agent_beta"

signal_1_data = shared_environment[eval_agent_1_id]['signal_data']
signal_2_data = shared_environment[eval_agent_2_id]['signal_data']

vec1 = signal_1_data.get("vector", [])
vec2 = signal_2_data.get("vector", [])

coordination_score = 0.0
if len(vec1) == len(vec2) and len(vec1) > 0:
  coordination_score = sum(a * b for a, b in zip(vec1, vec2))

print(f"   Coordination Score {coordination_score:.4f}")
