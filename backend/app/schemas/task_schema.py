from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


CriterionType = Literal["min", "max"]


class CriterionBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    type: CriterionType
    weight: float = Field(ge=0)


class CriterionCreate(CriterionBase):
    pass


class CriterionRead(CriterionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class AlternativeValueCreate(BaseModel):
    criterion_name: str | None = None
    criterion_id: int | None = None
    value: float


class AlternativeBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class AlternativeCreate(AlternativeBase):
    values: list[AlternativeValueCreate]


class AlternativeValueRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    criterion_id: int
    criterion_name: str
    value: float


class AlternativeRead(AlternativeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    values: list[AlternativeValueRead]


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    criteria: list[CriterionCreate]
    alternatives: list[AlternativeCreate]


class TaskUpdate(TaskCreate):
    pass


class TaskListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    created_at: datetime
    updated_at: datetime


class TaskRead(TaskListItem):
    criteria: list[CriterionRead]
    alternatives: list[AlternativeRead]
