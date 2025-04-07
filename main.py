from fastapi import FastAPI
from pydantic import BaseModel

app =  FastAPI()

class Task(BaseModel):
    title: str
    completed: bool = False

tasks = [
    {"id": 1, "title": "Buy milk", "completed": False},
    {"id": 2, "title": "Do laundry", "completed": True}
]

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def add_task(task: Task):
    new_task = {
        "id":len(tasks)+1,
        "title": task.title,
        "completed": task.completed
    }
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id:int,updated_task : Task):
    print(tasks)
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["completed"] = updated_task.completed
            return task
    return {
        "error": "task not found"
    }