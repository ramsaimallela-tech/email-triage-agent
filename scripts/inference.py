"""Inference script for the Email Triage Agent.

Follows the specified professional checklist for deployment.
"""

import os
import sys
import json
from openai import OpenAI

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(__file__))

from env.environment import EmailEnv
from agents.llm_agent import LLMAgent
from tasks import ALL_CONFIGS

# -- Environment Variables (from checklist) ---------------------------------
API_BASE_URL = os.getenv("API_BASE_URL", "<your-active-endpoint>")
MODEL_NAME = os.getenv("MODEL_NAME", "<your-active-model>")
HF_TOKEN = os.getenv("HF_TOKEN")
# Optional - if you use from_docker_image()
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")

# -- Initialize OpenAI Client -----------------------------------------------
client = OpenAI(
    api_key=HF_TOKEN or "dummy-token",
    base_url=API_BASE_URL
)

def main():
    print("START")
    
    # Select environment config (defaulting to easy for demonstration)
    task_name = "easy"
    config = ALL_CONFIGS[task_name]
    env = EmailEnv(config, seed=42)
    agent = LLMAgent(client, MODEL_NAME)
    
    obs = env.reset()
    done = False
    step_id = 0
    
    while not done:
        print(f"STEP {step_id}")
        
        # Agent selects an action
        action = agent.select_action(obs)
        
        # Step through the environment
        obs, reward, done, info = env.step(action)
        
        # Optional logging for debugging (not strictly required by STEP format)
        # print(f"  Category: {action.category}, Reward: {reward}")
        
        step_id += 1
        
    print("END")

if __name__ == "__main__":
    main()
