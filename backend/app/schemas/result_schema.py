from datetime import datetime

from pydantic import BaseModel


class RankingItem(BaseModel):
    alternative_id: int
    alternative_name: str
    score: float
    rank: int
    is_pareto_optimal: bool
    details: dict


class ChartData(BaseModel):
    criteria: list[str]
    alternatives: list[str]
    values: list[list[float]]
    pareto_points: list[dict]


class OptimizationResultResponse(BaseModel):
    task_id: int
    run_id: int
    method: str
    execution_time_ms: float
    ranking: list[RankingItem]
    chart_data: ChartData


class RunHistoryItem(BaseModel):
    id: int
    task_id: int
    method: str
    created_at: datetime
    execution_time_ms: float


class MethodComparisonResponse(BaseModel):
    task_id: int
    runs: list[OptimizationResultResponse]
    summary: list[dict]
