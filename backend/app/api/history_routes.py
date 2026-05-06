from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.result_schema import OptimizationResultResponse, RunHistoryItem
from app.services.history_service import get_run_result, list_runs

router = APIRouter(tags=["history"])


@router.get("/api/tasks/{task_id}/runs", response_model=list[RunHistoryItem])
def task_runs(task_id: int, db: Session = Depends(get_db)):
    runs = list_runs(db, task_id)
    if runs is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return runs


@router.get("/api/runs/{run_id}", response_model=OptimizationResultResponse)
def run_result(run_id: int, db: Session = Depends(get_db)):
    result = get_run_result(db, run_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Запуск не найден")
    return result
