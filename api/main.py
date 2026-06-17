"""
Synaptica API - FastAPI Endpoints
Multi-agent workflow + multi-document RAG + persistent history + reports
"""

import os
import time
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.orchestrator import Orchestrator
from knowledge.ingest import extract_pdf_text, chunk_text
from knowledge.vector_store import add_chunks_to_chroma, list_collections
from knowledge.retriever import answer_from_docs
from knowledge.history import load_history, save_history_item, clear_history
from knowledge.reports import load_reports, save_report, clear_reports


app = FastAPI(
    title="Synaptica API",
    description="Multi-Agent AI Platform with Multi-Document RAG",
    version="2.3.0",
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
    collection_name: str


class ReportRequest(BaseModel):
    title: str
    content: str
    source_type: str = "rag"


@app.get("/")
async def root():
    return {
        "name": "Synaptica API",
        "version": "2.3.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "agents": 5,
        "rag": True,
        "multi_document_rag": True,
        "persistent_history": True,
        "reports": True,
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


@app.get("/knowledge-bases")
async def knowledge_bases():
    return {
        "collections": list_collections()
    }


@app.get("/rag-history")
async def rag_history():
    return {
        "history": load_history()
    }


@app.delete("/rag-history")
async def delete_rag_history():
    clear_history()
    return {
        "success": True,
        "message": "RAG history cleared",
    }


@app.get("/reports")
async def get_reports():
    return {
        "reports": load_reports()
    }


@app.post("/reports")
async def create_report(request: ReportRequest):
    report = save_report(
        title=request.title,
        content=request.content,
        source_type=request.source_type,
    )

    return {
        "success": True,
        "report": report,
    }


@app.delete("/reports")
async def delete_reports():
    clear_reports()
    return {
        "success": True,
        "message": "Reports cleared",
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

        result = add_chunks_to_chroma(
            chunks,
            source_name=file.filename,
        )

        return {
            "success": True,
            "filename": file.filename,
            "characters_extracted": len(text),
            "chunks_stored": result["chunks_stored"],
            "collection_name": result["collection_name"],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ask-docs")
async def ask_docs(request: AskDocsRequest):
    try:
        result = await answer_from_docs(
            question=request.question,
            collection_name=request.collection_name,
        )

        save_history_item(
            collection=request.collection_name,
            question=request.question,
            answer=result["answer"],
            sources=result["sources"],
        )

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