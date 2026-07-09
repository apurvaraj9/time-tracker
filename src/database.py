import os

import sqlite3
import datetime
import pandas as pd
from contextlib import contextmanager

DATABASE_FILE = os.path.join(os.path.dirname(__file__), "..", "time_data.db")

@contextmanager
def get_connection():
    """
    A single reusable context manager for database connections.
    Automatically commits and closes the connection when done.
    Usage: with get_connection() as conn:
    """
    conn = sqlite3.connect(DATABASE_FILE)
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def init_db():
    """
    Creates the database and the sessions table if they don't exist yet.
    Safe to call every time the tracker starts.
    """
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp        TEXT NOT NULL,
                window_title     TEXT NOT NULL,
                category         TEXT NOT NULL,
                duration_seconds INTEGER NOT NULL
            )
        """)

def save_session(window_title, category, duration_seconds):
    """
    Saves one tracking entry to the database.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO sessions (timestamp, window_title, category, duration_seconds)
            VALUES (?, ?, ?, ?)
        """, (timestamp, window_title, category, duration_seconds))

def get_today_summary():
    """
    Returns today's usage grouped by category as a pandas DataFrame.
    """
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    with get_connection() as conn:
        df = pd.read_sql_query("""
            SELECT
                category,
                SUM(duration_seconds) / 60.0 AS total_minutes
            FROM sessions
            WHERE timestamp LIKE ?
            GROUP BY category
            ORDER BY total_minutes DESC
        """, conn, params=(f"{today}%",))
    return df

def get_today_detail():
    """
    Returns every individual session from today.
    """
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    with get_connection() as conn:
        df = pd.read_sql_query("""
            SELECT timestamp, category, window_title, duration_seconds
            FROM sessions
            WHERE timestamp LIKE ?
            ORDER BY timestamp DESC
        """, conn, params=(f"{today}%",))
    return df


def clear_today():
    """
    Deletes all sessions recorded today.
    """
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    with get_connection() as conn:
        conn.execute("""
            DELETE FROM sessions
            WHERE timestamp LIKE ?
        """, (f"{today}%",))