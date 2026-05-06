from sqlalchemy import CheckConstraint, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Criterion(Base):
    __tablename__ = "criteria"
    __table_args__ = (
        CheckConstraint("type in ('min', 'max')", name="ck_criteria_type"),
        CheckConstraint("weight >= 0", name="ck_criteria_weight_non_negative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("optimization_tasks.id"))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(3), nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)

    task = relationship("OptimizationTask", back_populates="criteria")
    values = relationship(
        "AlternativeValue", back_populates="criterion", cascade="all, delete-orphan"
    )
