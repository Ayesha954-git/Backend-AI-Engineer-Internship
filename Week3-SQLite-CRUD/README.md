Week 3 – SQLite CRUD API

A FastAPI CRUD API extended from the Week 2 in-memory CRUD API by adding
SQLite database persistence.

📌 Overview

In Week 2, the Task CRUD API stored tasks temporarily in a Python list.

In Week 3, the API was upgraded to use SQLite so that tasks are stored
persistently in a database and remain available even after restarting the
FastAPI server.

🚀 Features

- Create a new task
- Retrieve all tasks
- Retrieve a task by ID
- Update an existing task
- Delete a task
- SQLite database persistence
- Automatic database and table creation
- Seed data for initial tasks
- Input validation using Pydantic
- Proper HTTP status codes and exception handling
- Interactive API documentation with Swagger UI

🛠️ Technologies Used

- Python
- FastAPI
- SQLite
- Pydantic
- Uvicorn
- DB Browser for SQLite

📁 Project Structure
Week3-SQLite-CRUD/
│
├── main.py
├── database.py
├── requirements.txt
├── .gitignore
└── README.md

(Run these Commands)
python -m venv venv  
.\venv\Scripts\Activate.ps1  
pip install -r requirements.txt
python database.py  
uvicorn main:app --reload  
http://127.0.0.1:8000/docs
