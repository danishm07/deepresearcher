#setting up the FastAPI application
#this allows us to run the FastAPI application with uvicorn
#fast api is a framework for building APIs, and Uvicorn is a lightweight ASGI server for running FastAPI applications
#fastapi builds apis by defining endpoints, which are the URLs that the API responds to
#each endpoint is associated with a function that handles the request and returns a response
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from backend.mcp.registry import load_yaml_workflow_by_agent_name, execute_workflow
import backend.mcp.agents 

app = FastAPI()

class AgentRequest(BaseModel):
    query: str
    agent_name: str
    context: dict = {}

STORAGE_PATH = "frontend/storage.json"

@app.post("/run-agent")
def run_agent(request: AgentRequest):
    try:
        agent_yaml = load_yaml_workflow_by_agent_name(request.agent_name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Agent YAML not found.")
    print("🧠 Loaded YAML:", agent_yaml)

    # For chat_single_paper, context is required
    results = execute_workflow(agent_yaml, {
        "query": request.query,
        "context": request.context
    })

    return {"results": results}

@app.get("/health")
def health_check():
    return {"status": "ok"}
    """
    Simple health check endpoint.
    Returns a 200 response with a JSON body containing `{"status": "ok"}`.
    """


#Usage
# -----------------------------
# Run the API server:
# uvicorn backend.api.main:app --reload

# Example request:
# POST http://localhost:8000/run-agent
# Body:
# {
#   "query": "self-supervised learning in medical imaging",
#   "agent_name": "example_agent"
# }
