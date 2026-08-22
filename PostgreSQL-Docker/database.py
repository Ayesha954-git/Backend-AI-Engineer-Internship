import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg.connect(DATABASE_URL)


def create_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL
        )
    """)

    connection.commit()
    connection.close()

def seed_tasks():
    connection = get_connection()

    cursor = connection.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:
        with connection.cursor() as cursor:
            cursor.executemany(
                "INSERT INTO tasks (title, done) VALUES (%s, %s)",
                [
                    ("Learn PostgreSQL", False),
                    ("Connect FastAPI to PostgreSQL", False),
                    ("Test CRUD API", False)
                ]
            )

        connection.commit()

    connection.close()

if __name__ == "__main__":
    create_table()
    seed_tasks()
    print("Database created successfully!")