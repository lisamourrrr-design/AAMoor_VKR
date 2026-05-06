from sqlalchemy.orm import Session, selectinload

from app.models import OptimizationRun
from app.models.alternative_model import Alternative
from app.models.task_model import OptimizationTask
from app.services.optimization_service import _build_input, _chart_data
from app.services.task_service import get_task_or_none


def list_runs(db: Session, task_id: int) -> list[OptimizationRun] | None:
    task = get_task_or_none(db, task_id)
    if task is None:
        return None
    return (
        db.query(OptimizationRun)
        .filter(OptimizationRun.task_id == task_id)
        .order_by(OptimizationRun.created_at.desc())
        .all()
    )


def get_run_result(db: Session, run_id: int) -> dict | None:
    run = (
        db.query(OptimizationRun)
        .options(
            selectinload(OptimizationRun.results),
            selectinload(OptimizationRun.task)
            .selectinload(OptimizationTask.alternatives)
            .selectinload(Alternative.values),
            selectinload(OptimizationRun.task).selectinload(OptimizationTask.criteria),
        )
        .filter(OptimizationRun.id == run_id)
        .first()
    )
    if run is None:
        return None

    alternatives, criteria, matrix, _weights, _types = _build_input(run.task)
    ranking = [
        {
            "alternative_id": result.alternative_id,
            "alternative_name": result.alternative.name,
            "score": result.score,
            "rank": result.rank,
            "is_pareto_optimal": result.is_pareto_optimal,
            "details": result.details_json or {},
        }
        for result in sorted(run.results, key=lambda item: item.rank)
    ]
    raw_ranking = [
        {
            "alternative_name": item["alternative_name"],
            "alternative_index": next(
                index
                for index, alternative in enumerate(alternatives)
                if alternative.id == item["alternative_id"]
            ),
            "is_pareto_optimal": item["is_pareto_optimal"],
        }
        for item in ranking
    ]

    return {
        "task_id": run.task_id,
        "run_id": run.id,
        "method": run.method,
        "execution_time_ms": run.execution_time_ms,
        "ranking": ranking,
        "chart_data": _chart_data(criteria, alternatives, matrix, raw_ranking),
    }
