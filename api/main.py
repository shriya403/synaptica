"""
Synaptica API - FastAPI Endpoints
"""

import time
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.orchestrator import Orchestrator


app = FastAPI(
    title="Synaptica API",
    description="Self-Evolving Multi-Agent Intelligence Platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


orchestrator = Orchestrator()


class TaskRequest(BaseModel):
    task: str
    context: Dict[str, Any] = {}


class TaskResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
    execution_time: float


@app.get("/")
async def root():
    return {
        "name": "Synaptica API",
        "version": "1.0.0",
        "description": "Self-Evolving Multi-Agent Intelligence Platform",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "agents": 5,
    }


@app.get("/agents")
async def list_agents():
    return {
        "agents": [
            {"name": "MarketResearcher", "role": "Market Research Analyst"},
            {"name": "ContentCreator", "role": "Content Creator & Copywriter"},
            {"name": "TimelinePlanner", "role": "Project Manager"},
            {"name": "RiskAnalyst", "role": "Risk Analyst"},
            {"name": "BudgetOptimizer", "role": "Financial Analyst"},
        ]
    }


@app.post("/execute", response_model=TaskResponse)
async def execute_task(request: TaskRequest):
    try:
        start_time = time.time()

        result = await orchestrator.execute_task(
            request.task
        )

        execution_time = time.time() - start_time

        return TaskResponse(
            success=True,
            result=result,
            execution_time=round(execution_time, 2),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )