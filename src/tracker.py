import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

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

        if active_window is not None and active_window.title.strip():
            window_title = active_window.title
            category = categorize(window_title)
            current_time = datetime.datetime.now().strftime("%H:%M:%S")

            save_session(window_title, category, INTERVAL)
            print(f"[{current_time}]  {category:<18}  {window_title}")

    except Exception as e:
        print(f"Error: {e}")

    # Single sleep at the end — always runs, no exceptions
    time.sleep(INTERVAL)