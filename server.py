import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()


# Define Pydantic models for request bodies
class SimulationAgentRequest(BaseModel):
    data: dict  # Replace with your expected structure

class ProductionAgentRequest(BaseModel):
    data: dict  # Replace with your expected structure

class FeedbackRequest(BaseModel):
    feedback: str


    

@app.get("/")
async def root():
    return {"message": "Agent API"}

@app.post("/simulation-agent")
async def simulation_agent(request: SimulationAgentRequest):
    # Process the simulation agent request
    # (Insert your simulation logic here)
    return {"message": "Simulation agent endpoint", "received": request.data}

@app.post("/production-agent")
async def production_agent(request: ProductionAgentRequest):
    # Process the production agent request
    # (Insert your production logic here)
    return {"message": "Production agent endpoint", "received": request.data}

@app.post("/feedback")
async def feedback(request: FeedbackRequest):
    # Process the feedback. For example, if feedback is positive, the agent may call an email tool.
    # Here, we simply return an acknowledgment.
    # (Insert your feedback logic here)
    return {"message": "Feedback endpoint", "feedback": request.feedback, "acknowledgment": "Noted, thanks for the feedback"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
