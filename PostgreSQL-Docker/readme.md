PostgreSQL Docker CRUD API

A simple **Task CRUD API** built with **FastAPI, PostgreSQL, Docker, and Psycopg 3**.

This project demonstrates how to connect a FastAPI backend to a PostgreSQL database running inside a Docker container and perform Create, Read, Update, and Delete operations.

🚀 Technologies

* Python
* FastAPI
* PostgreSQL 17
* Docker
* Psycopg 3
* Pydantic
* python-dotenv
* Swagger UI

📁 Project Structure

```text
PostgreSQL-Docker/
│
├── main.py              # FastAPI application and CRUD endpoints
├── database.py          # PostgreSQL connection and database setup
├── requirements.txt     # Python dependencies
├── .env.example         # Example database configuration
├── .gitignore
└── README.md
```

🔗 How It Works

Client / Swagger
       ↓
    FastAPI
       ↓
    main.py
       ↓
   Psycopg 3
       ↓
PostgreSQL (Docker)
       ↓
    tasks table

FastAPI handles the API requests, while PostgreSQL stores the task data permanently.

🗄️ Database

The PostgreSQL database is:

Database: tasks
Host: localhost
Port: 5432


The `tasks` table contains:

| Column  | Type    | Description            |
| ------- | ------- | ---------------------- |
| `id`    | integer | Auto-generated task ID |
| `title` | text    | Task title             |
| `done`  | boolean | Completion status      |

⚙️ Setup

1. Create and activate virtual environment

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Configure `.env`

Create a `.env` file:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/tasks
```

Replace `YOUR_PASSWORD` with your PostgreSQL password.

**Do not commit `.env` to GitHub.**

4. Start PostgreSQL

Make sure Docker Desktop is running and check:

```powershell
docker ps
```

The PostgreSQL container used in this project is:

```text
taskdb
```

5. Initialize the database

```powershell
python database.py
```

This creates the `tasks` table and adds sample tasks.

6. Start FastAPI

```powershell
uvicorn main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

📌 API Endpoints

| Method | Endpoint      | Purpose         |
| ------ | ------------- | --------------- |
| GET    | `/`           | Welcome message |
| POST   | `/tasks`      | Create a task   |
| GET    | `/tasks`      | Get all tasks   |
| GET    | `/tasks/{id}` | Get one task    |
| PUT    | `/tasks/{id}` | Update a task   |
| DELETE | `/tasks/{id}` | Delete a task   |

 Example: Create a Task

```json
{
  "title": "Learn Docker",
  "completed": false
}
```

The task ID is generated automatically by PostgreSQL.

🧪 Testing

The API can be tested directly through **Swagger UI**:

```text
http://127.0.0.1:8000/docs
```

You can test all CRUD operations from there.

You can also verify the database directly:

```powershell
docker exec -it taskdb psql -U postgres -d tasks
```

Then:

```sql
SELECT * FROM tasks;
```

🔐 Security

Database credentials are stored in `.env` and are not committed to GitHub.

Only `.env.example` is included in the repository.

🎯 Learning Outcomes

This project demonstrates:

* Building REST APIs with FastAPI
* Implementing CRUD operations
* Connecting Python to PostgreSQL
* Running PostgreSQL with Docker
* Using Psycopg 3
* Managing environment variables
* Testing APIs with Swagger UI
* Using Git and GitHub
