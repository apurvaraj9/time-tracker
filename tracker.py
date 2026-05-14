import pygetwindow as gw
import time
import datetime
from categorizer import categorize
from database import init_db, save_session

# How often we check (in seconds)
INTERVAL = 5

# Set up the database when the tracker starts
init_db()

print("Time Tracker started! Press Ctrl+C to stop.")
print("-" * 40)

while True:
    try:
        active_window = gw.getActiveWindow()

        if active_window is None:
            time.sleep(INTERVAL)
            continue

        window_title = active_window.title

        if not window_title.strip():
            time.sleep(INTERVAL)
            continue

        category = categorize(window_title)
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        # Save to database
        save_session(window_title, category, INTERVAL)

        print(f"[{current_time}]  {category:<18}  {window_title}")

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(INTERVAL)