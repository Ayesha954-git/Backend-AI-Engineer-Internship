PostgreSQL Docker CRUD API

A Task CRUD API built with **FastAPI, PostgreSQL 17, Docker Compose, Psycopg 3, and Pydantic**.

This project demonstrates how to run both the FastAPI backend and PostgreSQL database in Docker and connect them through Docker Compose.

🚀 Technologies

* Python
* FastAPI
* PostgreSQL 17
* Docker & Docker Compose
* Psycopg 3
* Pydantic
* python-dotenv
* Swagger UI

📁 Project Structure

```text
PostgreSQL-Docker/
├── main.py
├── database.py
├── Dockerfile
├── compose.yaml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

🔗 How It Works

```text
Swagger / Client
       ↓
    FastAPI
       ↓
    Psycopg 3
       ↓
 PostgreSQL
   (Docker)
       ↓
  tasks table
```

Docker Compose runs the API and PostgreSQL as separate containers and connects them through the Compose network.

🗄️ Database

* **Database:** `tasks`
* **User:** `postgres`
* **PostgreSQL:** 17
* **Container:** `taskdb`
* **Port:** `5432`

The `tasks` table stores:

| Column | Type    | Description            |
| ------ | ------- | ---------------------- |
| id     | integer | Auto-generated task ID |
| title  | text    | Task title             |
| done   | boolean | Completion status      |

⚙️ Setup

Create a `.env` file:

```env
POSTGRES_PASSWORD=YOUR_PASSWORD
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/tasks
```

Do **not** commit `.env` to GitHub.

### Start the application

Make sure Docker Desktop is running, then:

```powershell
docker compose up -d
```

Check the containers:

```powershell
docker ps
```

You should see:

```text
taskdb
taskapi
```

API

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
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

🧪 Testing

CRUD operations can be tested through Swagger UI:

```text
http://localhost:8000/docs
```

The PostgreSQL database can also be checked directly:

```powershell
docker exec -it taskdb psql -U postgres -d tasks
```

Then:

```sql
SELECT * FROM tasks;
```

🔐 Security

Database credentials are stored in `.env`.

The `.env` file is excluded from GitHub, while `.env.example` is provided as a template.

🎯 Learning Outcomes

* Built a REST API with FastAPI
* Implemented CRUD operations
* Connected FastAPI to PostgreSQL using Psycopg 3
* Containerized FastAPI and PostgreSQL with Docker
* Used Docker Compose for multi-container setup
* Managed environment variables
* Tested APIs using Swagger UI
* Used Git and GitHub
