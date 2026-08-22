from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from database import get_connection

app = FastAPI(
    title="Task CRUD API",
    description="Simple CRUD API using FastAPI and PostgreSQL",
    version="1.0.0"
)


# --------------------
# Data Models
# --------------------

class TaskCreate(BaseModel):
    title: str
    completed: bool = False


class Task(BaseModel):
    id: int
    title: str
    completed: bool = False


# --------------------
# Home Route
# --------------------

@app.get("/")
def home():
    return {"message": "Welcome to the Task CRUD API"}


# --------------------
# CREATE
# --------------------

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO tasks (title, done)
        VALUES (%s, %s)
        RETURNING id, title, done
        """,
        (task.title, task.completed)
    )

    row = cursor.fetchone()

    connection.commit()
    connection.close()

    return Task(
        id=row[0],
        title=row[1],
        completed=row[2]
    )


# --------------------
# READ ALL
# --------------------

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    connection = get_connection()

    rows = connection.execute(
        "SELECT id, title, done FROM tasks ORDER BY id"
    ).fetchall()

    connection.close()

    return [
        Task(
            id=row[0],
            title=row[1],
            completed=row[2]
        )
        for row in rows
    ]


# --------------------
# READ ONE
# --------------------

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    connection = get_connection()

    row = connection.execute(
        """
        SELECT id, title, done
        FROM tasks
        WHERE id = %s
        """,
        (task_id,)
    ).fetchone()

    connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return Task(
        id=row[0],
        title=row[1],
        completed=row[2]
    )


# --------------------
# UPDATE
# --------------------

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: TaskCreate):
    connection = get_connection()

    row = connection.execute(
        """
        UPDATE tasks
        SET title = %s, done = %s
        WHERE id = %s
        RETURNING id, title, done
        """,
        (
            updated_task.title,
            updated_task.completed,
            task_id
        )
    ).fetchone()

    connection.commit()
    connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return Task(
        id=row[0],
        title=row[1],
        completed=row[2]
    )


# --------------------
# DELETE
# --------------------

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    connection = get_connection()

    row = connection.execute(
        """
        DELETE FROM tasks
        WHERE id = %s
        RETURNING id
        """,
        (task_id,)
    ).fetchone()

    connection.commit()
    connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {"message": "Task deleted successfully"}