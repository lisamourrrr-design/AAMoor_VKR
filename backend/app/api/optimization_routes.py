from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.optimization_schema import OptimizeRequest
from app.schemas.result_schema import MethodComparisonResponse, OptimizationResultResponse
from app.services.comparison_service import compare_all_methods
from app.services.optimization_service import optimize_task

router = APIRouter(prefix="/api/tasks", tags=["optimization"])


@router.post("/{task_id}/optimize", response_model=OptimizationResultResponse)
def optimize(task_id: int, payload: OptimizeRequest, db: Session = Depends(get_db)):
    try:
        result = optimize_task(db, task_id, payload.method)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if result is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return result


@router.post("/{task_id}/compare", response_model=MethodComparisonResponse)
def compare(task_id: int, db: Session = Depends(get_db)):
    try:
        result = compare_all_methods(db, task_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if result is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return result
