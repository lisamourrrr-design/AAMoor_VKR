from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class OptimizationRun(Base):
    __tablename__ = "optimization_runs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("optimization_tasks.id"))
    method: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    execution_time_ms: Mapped[float] = mapped_column(Float, nullable=False)

    task = relationship("OptimizationTask", back_populates="runs")
    results = relationship(
        "OptimizationResult", back_populates="run", cascade="all, delete-orphan"
    )


class OptimizationResult(Base):
    __tablename__ = "optimization_results"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("optimization_runs.id"))
    alternative_id: Mapped[int] = mapped_column(ForeignKey("alternatives.id"))
    score: Mapped[float] = mapped_column(Float, nullable=False)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    is_pareto_optimal: Mapped[bool] = mapped_column(Boolean, default=False)
    details_json: Mapped[dict] = mapped_column(JSON, default=dict)

    run = relationship("OptimizationRun", back_populates="results")
    alternative = relationship("Alternative", back_populates="results")
