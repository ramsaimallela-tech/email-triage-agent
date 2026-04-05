"""Formal inference script for the Email Triage Agent."""

import os
import sys
import json
from openai import OpenAI

# Ensure project root is in the path
sys.path.insert(0, os.path.dirname(__file__))

from env.environment import EmailEnv
from agents.llm_agent import LLMAgent
from tasks import ALL_CONFIGS

# Configuration from Environment
API_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL = os.getenv("MODEL_NAME", "gpt-4-turbo")
TOKEN = os.getenv("HF_TOKEN")

def main():
    print("START")
    
    # Setup infrastructure
    client = OpenAI(api_key=TOKEN or "no-token", base_url=API_URL)
    config = ALL_CONFIGS["easy"]
    
    env = EmailEnv(config, seed=42)
    agent = LLMAgent(client, MODEL)
    
    observation = env.reset()
    is_finished = False
    step_index = 0
    
    while not is_finished:
        print(f"STEP {step_index}")
        
        # Agent interaction
        agent_action = agent.select_action(observation)
        observation, step_reward, is_finished, step_metadata = env.step(agent_action)
        
        step_index += 1
        
    print("END")

if __name__ == "__main__":
    main()
