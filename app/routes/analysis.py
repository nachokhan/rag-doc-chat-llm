"""
API endpoints for market analysis.
"""
import asyncio
from fastapi import APIRouter, BackgroundTasks, Depends
from sse_starlette.sse import EventSourceResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db import get_db
from app.models import MarketAnalysis, TaskStatus
from app.services.market_analysis.orchestrator import run_analysis

router = APIRouter()

class AnalysisRequest(BaseModel):
    query: str

@router.post("/analysis/market", status_code=202)
async def start_market_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Starts a market analysis background task.
    """
    new_analysis = MarketAnalysis(query=request.query, status=TaskStatus.PENDING)
    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)

    task_id = new_analysis.id

    background_tasks.add_task(run_analysis, task_id, request.query)

    return {"message": "Analysis started", "task_id": task_id}

@router.get("/analysis/stream/{task_id}")
async def stream_market_analysis(task_id: int, db: Session = Depends(get_db)):
    """
    Streams progress and results for a market analysis task.
    """
    async def event_generator():
        last_update = ""
        while True:
            task = db.query(MarketAnalysis).filter(MarketAnalysis.id == task_id).first()
            if task:
                db.refresh(task)  # Force a refresh to see committed changes
                if task.progress_updates and task.progress_updates != last_update:
                    yield {"event": "progress", "data": task.progress_updates}
                    last_update = task.progress_updates

                if task.status == TaskStatus.COMPLETED:
                    yield {"event": "complete", "data": task.report}
                    break

                if task.status == TaskStatus.FAILED:
                    yield {"event": "error", "data": "Analysis failed."}
                    break

            await asyncio.sleep(2)  # Poll the DB every 2 seconds

    return EventSourceResponse(event_generator())
