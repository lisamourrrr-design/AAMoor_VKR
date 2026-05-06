from sqlalchemy.orm import Session

from app.services.optimization_service import optimize_task


METHODS = ["weighted_sum", "pareto", "topsis"]


def compare_all_methods(db: Session, task_id: int) -> dict | None:
    runs = []
    for method in METHODS:
        result = optimize_task(db, task_id, method)
        if result is None:
            return None
        runs.append(result)

    summary = []
    for result in runs:
        best = min(result["ranking"], key=lambda item: item["rank"])
        summary.append(
            {
                "method": result["method"],
                "best_alternative": best["alternative_name"],
                "best_score": best["score"],
                "run_id": result["run_id"],
            }
        )

    return {"task_id": task_id, "runs": runs, "summary": summary}
