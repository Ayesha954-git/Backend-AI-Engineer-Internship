from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Task CRUD API",
    description="Simple CRUD API using FastAPI",
    version="1.0.0"
)

# --------------------
# Data Model
# --------------------
class Task(BaseModel):
    id: int
    title: str
    completed: bool = False


tasks = []

# --------------------
# Home Route
# --------------------
@app.get("/")
def home():
    return {"message": "Welcome to the Task CRUD API"}

# --------------------
# CREATE
# --------------------
@app.post("/tasks")
def create_task(task: Task):
    for t in tasks:
        if t.id == task.id:
            raise HTTPException(status_code=400, detail="Task ID already exists")

    tasks.append(task)
    return {
        "message": "Task created successfully",
        "task": task
    }

# --------------------
# READ ALL
# --------------------
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

# --------------------
# READ ONE
# --------------------
@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    for task in tasks:
        if task.id == task_id:
            return task

    raise HTTPException(status_code=404, detail="Task not found")

# --------------------
# UPDATE
# --------------------
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):

    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks[index] = updated_task
            return {
                "message": "Task updated successfully",
                "task": updated_task
            }

    raise HTTPException(status_code=404, detail="Task not found")

# --------------------
# DELETE
# --------------------
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(index)
            return {
                "message": "Task deleted successfully"
            }

    raise HTTPException(status_code=404, detail="Task not found")