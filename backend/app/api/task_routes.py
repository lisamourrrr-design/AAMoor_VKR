from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.task_schema import TaskCreate, TaskListItem, TaskRead
from app.services import task_service

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    try:
        task = task_service.create_task(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return task_service.get_task_dict(db, task.id)


@router.get("", response_model=list[TaskListItem])
def list_tasks(db: Session = Depends(get_db)):
    return task_service.list_tasks(db)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = task_service.get_task_dict(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, payload: TaskCreate, db: Session = Depends(get_db)):
    try:
        task = task_service.replace_task(db, task_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task_service.get_task_dict(db, task_id)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    if not task_service.delete_task(db, task_id):
        raise HTTPException(status_code=404, detail="Задача не найдена")
