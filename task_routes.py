from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Task, TaskDB

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

@router.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(TaskDB).all()
    return tasks

@router.post("/tasks")
def add_task(task: Task, db: Session = Depends(get_db)):
    new_task = TaskDB(title=task.title, completed=task.completed)
    db.add(new_task)
    db.commit()
    db.refresh(new_task) 
    return new_task

@router.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if task:
        task.title = updated_task.title
        task.completed = updated_task.completed
        db.commit()
        db.refresh(task)
        return task
    return {"error": "Task not found"}

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return {"message": f"Task with id {task_id} deleted"}
    return {"error": "Task not found"}