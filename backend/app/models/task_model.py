from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class OptimizationTask(Base):
    __tablename__ = "optimization_tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    criteria = relationship(
        "Criterion", back_populates="task", cascade="all, delete-orphan"
    )
    alternatives = relationship(
        "Alternative", back_populates="task", cascade="all, delete-orphan"
    )
    runs = relationship(
        "OptimizationRun", back_populates="task", cascade="all, delete-orphan"
    )
