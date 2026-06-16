"""
Synaptica API - FastAPI Endpoints
"""

import os
import time
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.orchestrator import Orchestrator
from knowledge.ingest import extract_pdf_text, chunk_text
from knowledge.vector_store import add_chunks_to_chroma
from knowledge.retriever import answer_from_docs


app = FastAPI(
    title="Synaptica API",
    description="Multi-Agent AI Platform with RAG",
    version="2.0.0",
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


class AskDocsRequest(BaseModel):
    question: str


@app.get("/")
async def root():
    return {
        "name": "Synaptica API",
        "version": "2.0.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "agents": 5,
        "rag": True,
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

        result = await orchestrator.execute_task(request.task)

        execution_time = time.time() - start_time

        return TaskResponse(
            success=True,
            result=result,
            execution_time=round(execution_time, 2),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        os.makedirs("uploads", exist_ok=True)

        file_path = os.path.join("uploads", file.filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        text = extract_pdf_text(file_path)

        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text found in this PDF.",
            )

        chunks = chunk_text(text)

        count = add_chunks_to_chroma(
            chunks,
            source_name=file.filename,
        )

        return {
            "success": True,
            "filename": file.filename,
            "characters_extracted": len(text),
            "chunks_stored": count,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ask-docs")
async def ask_docs(request: AskDocsRequest):
    try:
        result = await answer_from_docs(request.question)

        return {
            "success": True,
            "result": result,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )