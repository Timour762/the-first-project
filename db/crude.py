import sqlite3
from db.session import DB_PATH
import logging
logger = logging.getLogger(__name__)

def save_reminder(tg_id: int, description: str, data: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO recipes
            (tg_id, description, data, is_active)
            VALUES (?, ?, ?, 1)
            """,
            (tg_id, description, data)
        )
        conn.commit()
        logger.info(f"✅ Сохранено напоминание: {data} для пользователя {tg_id}")

def get_reminders(tg_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, description, data
            FROM recipes
            WHERE user_id = ? AND is_active = 1
            ORDER BY data
            """,
            (tg_id,)
        )
        return cursor.fetchall()


def delete_reminder(reminder_id: int, tg_id: int = None):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        if tg_id:
            cursor.execute(
                """
                UPDATE recipes
                SET is_active = 0
                WHERE id = ? AND tg_id = ?
                """,
                (reminder_id, tg_id)
            )
        else:
            cursor.execute(
                """
                UPDATE recipes
                SET is_active = 0
                WHERE id = ?
                """,
                (reminder_id,)
            )
        conn.commit()
        return cursor.rowcount > 0


def active_reminders():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, tg_id, description, data
            FROM recipes
            WHERE is_active = 1
            """
        )
        return cursor.fetchall()


def save_date_to_db(user_id: int, date_str: str, description: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO recipes (user_id, data, description, is_active, notification)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, date_str, description, True, "уведомление")
        )
        conn.commit()

def del_remind(id_reminder: int, user_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            DELETE FROM recipes
            WHERE id = ? AND user_id = ?
            """,
            (id_reminder, user_id))
        conn.commit()

def get_reminder_by_id(tg_id: int, reminder_id: int):  # ← Переименуйте функцию!
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, description, data
            FROM recipes
            WHERE id = ? AND user_id = ? 
            """,
            (reminder_id, tg_id)
        )
        return cursor.fetchone()

def get_reminder_by(tg_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, description
            FROM recipes
            WHERE user_id = ? 
            """,
            (tg_id,)
        )
        return cursor.fetchall()