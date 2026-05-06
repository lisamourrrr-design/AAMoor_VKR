import time
from collections.abc import Callable

from sqlalchemy.orm import Session

from app.algorithms import calculate_pareto, calculate_topsis, calculate_weighted_sum
from app.models import OptimizationResult, OptimizationRun
from app.models.alternative_model import Alternative
from app.models.task_model import OptimizationTask
from app.services.task_service import get_task_or_none

Algorithm = Callable[
    [list[str], list[str], list[list[float]], list[float], list[str]], list[dict]
]

ALGORITHMS: dict[str, Algorithm] = {
    "weighted_sum": calculate_weighted_sum,
    "pareto": calculate_pareto,
    "topsis": calculate_topsis,
}


def _build_input(task: OptimizationTask) -> tuple[
    list[Alternative], list[str], list[list[float]], list[float], list[str]
]:
    criteria = sorted(task.criteria, key=lambda criterion: criterion.id)
    alternatives = sorted(task.alternatives, key=lambda alternative: alternative.id)
    criterion_ids = [criterion.id for criterion in criteria]

    matrix: list[list[float]] = []
    for alternative in alternatives:
        values_by_criterion = {
            value.criterion_id: value.value for value in alternative.values
        }
        if set(values_by_criterion) != set(criterion_ids):
            raise ValueError(
                f"У альтернативы '{alternative.name}' должны быть значения по всем критериям"
            )
        matrix.append([values_by_criterion[criterion_id] for criterion_id in criterion_ids])

    return (
        alternatives,
        [criterion.name for criterion in criteria],
        matrix,
        [criterion.weight for criterion in criteria],
        [criterion.type for criterion in criteria],
    )


def _pareto_flags(
    alternatives: list[str],
    criteria: list[str],
    matrix: list[list[float]],
    weights: list[float],
    criterion_types: list[str],
) -> dict[str, bool]:
    pareto_results = calculate_pareto(
        alternatives, criteria, matrix, weights, criterion_types
    )
    return {
        item["alternative_name"]: item["is_pareto_optimal"] for item in pareto_results
    }


def _chart_data(
    criteria: list[str],
    alternatives: list[Alternative],
    matrix: list[list[float]],
    ranking: list[dict],
) -> dict:
    pareto_points = [
        {
            "alternative_name": item["alternative_name"],
            "x": matrix[item["alternative_index"]][0],
            "y": matrix[item["alternative_index"]][1],
        }
        for item in ranking
        if item["is_pareto_optimal"] and len(criteria) == 2
    ]
    return {
        "criteria": criteria,
        "alternatives": [alternative.name for alternative in alternatives],
        "values": matrix,
        "pareto_points": pareto_points,
    }


def optimize_task(db: Session, task_id: int, method: str) -> dict | None:
    if method not in ALGORITHMS:
        raise ValueError("Неизвестный метод оптимизации")

    task = get_task_or_none(db, task_id)
    if task is None:
        return None

    alternatives, criteria, matrix, weights, criterion_types = _build_input(task)
    alternative_names = [alternative.name for alternative in alternatives]
    start = time.perf_counter()
    raw_ranking = ALGORITHMS[method](
        alternative_names, criteria, matrix, weights, criterion_types
    )
    pareto_by_name = _pareto_flags(
        alternative_names, criteria, matrix, weights, criterion_types
    )

    for item in raw_ranking:
        item["is_pareto_optimal"] = pareto_by_name[item["alternative_name"]]

    execution_time_ms = (time.perf_counter() - start) * 1000
    run = OptimizationRun(
        task_id=task.id, method=method, execution_time_ms=execution_time_ms
    )
    db.add(run)
    db.flush()

    ranking = []
    for item in raw_ranking:
        alternative = alternatives[item["alternative_index"]]
        db.add(
            OptimizationResult(
                run_id=run.id,
                alternative_id=alternative.id,
                score=item["score"],
                rank=item["rank"],
                is_pareto_optimal=item["is_pareto_optimal"],
                details_json=item["details"],
            )
        )
        ranking.append(
            {
                "alternative_id": alternative.id,
                "alternative_name": alternative.name,
                "score": item["score"],
                "rank": item["rank"],
                "is_pareto_optimal": item["is_pareto_optimal"],
                "details": item["details"],
            }
        )

    db.commit()
    return {
        "task_id": task.id,
        "run_id": run.id,
        "method": method,
        "execution_time_ms": execution_time_ms,
        "ranking": ranking,
        "chart_data": _chart_data(criteria, alternatives, matrix, raw_ranking),
    }
