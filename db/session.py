import sqlite3

DB_PATH = "data.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                description TEXT NOT NULL,
                data DATE,
                is_active INTEGER DEFAULT 1,
                notification TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER, 
                data_user DATE
            )
            """
        )

        conn.commit()

