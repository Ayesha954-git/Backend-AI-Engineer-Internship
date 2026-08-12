from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from database import get_connection

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
    connection = get_connection()

    existing_task = connection.execute(
        "SELECT id FROM tasks WHERE id = ?",
        (task.id,)
    ).fetchone()

    if existing_task is not None:
        connection.close()
        raise HTTPException(
            status_code=400,
            detail="Task ID already exists"
        )

    connection.execute(
        "INSERT INTO tasks (id, title, done) VALUES (?, ?, ?)",
        (task.id, task.title, int(task.completed))
    )

    connection.commit()
    connection.close()

    return {
        "message": "Task created successfully",
        "task": task
    }

# --------------------
# READ ALL
# --------------------
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    connection = get_connection()

    rows = connection.execute(
        "SELECT id, title, done FROM tasks"
    ).fetchall()

    connection.close()

    return [
        Task(
            id=row[0],
            title=row[1],
            completed=bool(row[2])
        )
        for row in rows
    ]

# --------------------
# READ ONE
# --------------------
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    connection = get_connection()

    row = connection.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    connection.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return Task(
        id=row[0],
        title=row[1],
        completed=bool(row[2])
    )

# --------------------
# UPDATE
# --------------------
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    connection = get_connection()

    existing_task = connection.execute(
        "SELECT id FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if existing_task is None:
        connection.close()
        raise HTTPException(status_code=404, detail="Task not found")

    connection.execute(
        """
        UPDATE tasks
        SET title = ?, done = ?
        WHERE id = ?
        """,
        (
            updated_task.title,
            int(updated_task.completed),
            task_id
        )
    )

    connection.commit()
    connection.close()

    updated_task.id = task_id

    return {
        "message": "Task updated successfully",
        "task": updated_task
    }
# --------------------
# DELETE
# --------------------
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    connection = get_connection()

    existing_task = connection.execute(
        "SELECT id FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if existing_task is None:
        connection.close()
        raise HTTPException(status_code=404, detail="Task not found")

    connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()