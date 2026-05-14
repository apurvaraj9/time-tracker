import sqlite3
import datetime
import pandas as pd

# The database file will be created automatically in your project folder
DATABASE_FILE = "time_data.db"

def init_db():
    """
    Creates the database and the sessions table if they don't exist yet.
    Safe to call every time the tracker starts.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp       TEXT NOT NULL,
            window_title    TEXT NOT NULL,
            category        TEXT NOT NULL,
            duration_seconds INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def save_session(window_title, category, duration_seconds):
    """
    Saves one tracking entry to the database.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO sessions (timestamp, window_title, category, duration_seconds)
        VALUES (?, ?, ?, ?)
    """, (timestamp, window_title, category, duration_seconds))

    conn.commit()
    conn.close()

def get_today_summary():
    """
    Returns a summary of today's usage grouped by category.
    Result is a pandas DataFrame with columns: category, total_minutes.
    """
    conn = sqlite3.connect(DATABASE_FILE)

    today = datetime.datetime.now().strftime("%Y-%m-%d")

    query = """
        SELECT
            category,
            SUM(duration_seconds) / 60.0 AS total_minutes
        FROM sessions
        WHERE timestamp LIKE ?
        GROUP BY category
        ORDER BY total_minutes DESC
    """

    df = pd.read_sql_query(query, conn, params=(f"{today}%",))
    conn.close()
    return df

def get_today_detail():
    """
    Returns every individual session from today.
    Useful for showing a detailed log.
    """
    conn = sqlite3.connect(DATABASE_FILE)

    today = datetime.datetime.now().strftime("%Y-%m-%d")

    query = """
        SELECT timestamp, category, window_title, duration_seconds
        FROM sessions
        WHERE timestamp LIKE ?
        ORDER BY timestamp DESC
    """

    df = pd.read_sql_query(query, conn, params=(f"{today}%",))
    conn.close()
    return df