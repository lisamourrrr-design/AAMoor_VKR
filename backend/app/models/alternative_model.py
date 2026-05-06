from sqlalchemy import Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Alternative(Base):
    __tablename__ = "alternatives"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("optimization_tasks.id"))
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    task = relationship("OptimizationTask", back_populates="alternatives")
    values = relationship(
        "AlternativeValue", back_populates="alternative", cascade="all, delete-orphan"
    )
    results = relationship("OptimizationResult", back_populates="alternative")


class AlternativeValue(Base):
    __tablename__ = "alternative_values"
    __table_args__ = (
        UniqueConstraint(
            "alternative_id", "criterion_id", name="uq_alternative_criterion_value"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    alternative_id: Mapped[int] = mapped_column(ForeignKey("alternatives.id"))
    criterion_id: Mapped[int] = mapped_column(ForeignKey("criteria.id"))
    value: Mapped[float] = mapped_column(Float, nullable=False)

    alternative = relationship("Alternative", back_populates="values")
    criterion = relationship("Criterion", back_populates="values")
