from typing import Literal

from pydantic import BaseModel


OptimizationMethod = Literal["weighted_sum", "pareto", "topsis"]


class OptimizeRequest(BaseModel):
    method: OptimizationMethod
