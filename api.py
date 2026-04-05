import os
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import gradio as gr

# Ensure imports work from current directory
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from env.environment import EmailEnv
from env.models import Action
from tasks import ALL_CONFIGS
from app import app as demo

api_app = FastAPI(title="OpenEnv Triage API")

# Global environment instance
current_env = EmailEnv(ALL_CONFIGS["easy"], seed=42)

class StepRequest(BaseModel):
    category: str
    priority: int
    reply: str

@api_app.post("/reset")
async def reset_env():
    try:
        obs = current_env.reset()
        return {
            "observation": {
                "timestep": obs.timestep,
                "email": obs.email.model_dump(),
                "emails_remaining": obs.emails_remaining
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_app.post("/step")
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
                "email": obs.email.model_dump(),
                "emails_remaining": obs.emails_remaining
            },
            "reward": reward,
            "done": done,
            "info": info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_app.get("/health")
async def health():
    return {"status": "ok"}

# Mount Gradio UI
app = gr.mount_gradio_app(api_app, demo, path="/")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
