from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
import os
import sys

# Ensure imports work
sys.path.insert(0, os.path.dirname(__file__))

from env.environment import EmailEnv
from env.models import Action, TaskConfig
from tasks import ALL_CONFIGS

app = FastAPI(title="OpenEnv Triage API")

# Global environment instance (simplification for single-user validation)
current_env = EmailEnv(ALL_CONFIGS["easy"], seed=42)

class StepRequest(BaseModel):
    category: str
    priority: int
    reply: str

@app.post("/reset")
async def reset_env():
    try:
        obs = current_env.reset()
        return {
            "observation": {
                "timestep": obs.timestep,
                "email": obs.email.dict(),
                "emails_remaining": obs.emails_remaining
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/step")
async def step_env(req: StepRequest):
    try:
        action = Action(
            category=req.category,
            priority=req.priority,
            reply=req.reply
        )
        obs, reward, done, info = current_env.step(action)
        return {
            "observation": {
                "timestep": obs.timestep,
                "email": obs.email.dict(),
                "emails_remaining": obs.emails_remaining
            },
            "reward": reward,
            "done": done,
            "info": info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
