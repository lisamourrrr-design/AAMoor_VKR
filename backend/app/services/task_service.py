from sqlalchemy.orm import Session, selectinload

from app.models import (
    Alternative,
    AlternativeValue,
    Criterion,
    OptimizationRun,
    OptimizationTask,
)
from app.schemas.task_schema import AlternativeRead, AlternativeValueRead, TaskCreate


def _normalize_weights(criteria_payload: list) -> list[float]:
    total = sum(criterion.weight for criterion in criteria_payload)
    if total <= 0:
        raise ValueError("Сумма весов должна быть больше нуля")
    return [criterion.weight / total for criterion in criteria_payload]


def _validate_payload(payload: TaskCreate) -> None:
    if not payload.criteria:
        raise ValueError("Добавьте хотя бы один критерий")
    if not payload.alternatives:
        raise ValueError("Добавьте хотя бы одну альтернативу")

    criterion_names = [criterion.name for criterion in payload.criteria]
    if len(set(criterion_names)) != len(criterion_names):
        raise ValueError("Названия критериев должны быть уникальными")

    required = set(criterion_names)
    for alternative in payload.alternatives:
        provided = {value.criterion_name for value in alternative.values}
        if provided != required:
            raise ValueError(
                f"У альтернативы '{alternative.name}' должны быть значения по всем критериям"
            )


def _serialize_task(task: OptimizationTask) -> dict:
    criteria = sorted(task.criteria, key=lambda criterion: criterion.id)
    criteria_by_id = {criterion.id: criterion for criterion in criteria}
    alternatives: list[AlternativeRead] = []

    for alternative in sorted(task.alternatives, key=lambda item: item.id):
        values = [
            AlternativeValueRead(
                criterion_id=value.criterion_id,
                criterion_name=criteria_by_id[value.criterion_id].name,
                value=value.value,
            )
            for value in sorted(alternative.values, key=lambda item: item.criterion_id)
        ]
        alternatives.append(
            AlternativeRead(id=alternative.id, name=alternative.name, values=values)
        )

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "created_at": task.created_at,
        "updated_at": task.updated_at,
        "criteria": criteria,
        "alternatives": alternatives,
    }


def create_task(db: Session, payload: TaskCreate) -> OptimizationTask:
    _validate_payload(payload)
    normalized_weights = _normalize_weights(payload.criteria)

    task = OptimizationTask(title=payload.title, description=payload.description)
    db.add(task)
    db.flush()

    criteria_by_name: dict[str, Criterion] = {}
    for criterion_payload, weight in zip(payload.criteria, normalized_weights):
        criterion = Criterion(
            task_id=task.id,
            name=criterion_payload.name,
            type=criterion_payload.type,
            weight=weight,
        )
        db.add(criterion)
        criteria_by_name[criterion.name] = criterion
    db.flush()

    for alternative_payload in payload.alternatives:
        alternative = Alternative(task_id=task.id, name=alternative_payload.name)
        db.add(alternative)
        db.flush()
        for value_payload in alternative_payload.values:
            db.add(
                AlternativeValue(
                    alternative_id=alternative.id,
                    criterion_id=criteria_by_name[value_payload.criterion_name].id,
                    value=value_payload.value,
                )
            )

    db.commit()
    db.refresh(task)
    return get_task_or_none(db, task.id)


def list_tasks(db: Session) -> list[OptimizationTask]:
    return db.query(OptimizationTask).order_by(OptimizationTask.updated_at.desc()).all()


def get_task_or_none(db: Session, task_id: int) -> OptimizationTask | None:
    return (
        db.query(OptimizationTask)
        .options(
            selectinload(OptimizationTask.criteria),
            selectinload(OptimizationTask.alternatives).selectinload(Alternative.values),
        )
        .filter(OptimizationTask.id == task_id)
        .first()
    )


def get_task_dict(db: Session, task_id: int) -> dict | None:
    task = get_task_or_none(db, task_id)
    return _serialize_task(task) if task else None


def replace_task(db: Session, task_id: int, payload: TaskCreate) -> OptimizationTask | None:
    task = get_task_or_none(db, task_id)
    if task is None:
        return None
    _validate_payload(payload)
    normalized_weights = _normalize_weights(payload.criteria)

    task.title = payload.title
    task.description = payload.description
    for run in db.query(OptimizationRun).filter(OptimizationRun.task_id == task_id).all():
        db.delete(run)
    db.flush()
    task.criteria.clear()
    task.alternatives.clear()
    db.flush()

    criteria_by_name: dict[str, Criterion] = {}
    for criterion_payload, weight in zip(payload.criteria, normalized_weights):
        criterion = Criterion(
            task=task,
            name=criterion_payload.name,
            type=criterion_payload.type,
            weight=weight,
        )
        db.add(criterion)
        criteria_by_name[criterion.name] = criterion
    db.flush()

    for alternative_payload in payload.alternatives:
        alternative = Alternative(task=task, name=alternative_payload.name)
        db.add(alternative)
        db.flush()
        for value_payload in alternative_payload.values:
            db.add(
                AlternativeValue(
                    alternative=alternative,
                    criterion=criteria_by_name[value_payload.criterion_name],
                    value=value_payload.value,
                )
            )

    db.commit()
    return get_task_or_none(db, task_id)


def delete_task(db: Session, task_id: int) -> bool:
    task = get_task_or_none(db, task_id)
    if task is None:
        return False
    db.delete(task)
    db.commit()
    return True
