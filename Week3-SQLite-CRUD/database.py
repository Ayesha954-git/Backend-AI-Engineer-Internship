import sqlite3

DATABASE_NAME = "tasks.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


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
        connection.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Learn SQLite", 0),
                ("Connect FastAPI to SQLite", 0),
                ("Test CRUD API", 0)
            ]
        )

        connection.commit()

    connection.close()


if __name__ == "__main__":
    create_table()
    seed_tasks()
    print("Database created successfully!")