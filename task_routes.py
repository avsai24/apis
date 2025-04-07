from fastapi import APIRouter
from models import Task

router = APIRouter()

tasks = [
    {"id": 1, "title": "Buy milk", "completed": False},
    {"id": 2, "title": "Do laundry", "completed": True}
]

@router.get("/tasks")
def get_tasks():
    return tasks

@router.post("/tasks")
def add_task(task: Task):
    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "completed": task.completed
    }
    tasks.append(new_task)
    return new_task

@router.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["completed"] = updated_task.completed
            return task
    return {"error": "Task not found"}

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": f"Task with id {task_id} deleted"}
    return {"error": "Task not found"}