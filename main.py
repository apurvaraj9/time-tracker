"""
Time Tracker - Entry Point
--------------------------
Run this file to start the tracker and dashboard together.

Usage:
    python main.py            -> starts both tracker and dashboard
    python main.py --track    -> starts tracker only
    python main.py --dash     -> starts dashboard only
"""

import sys
import threading
import subprocess

def start_tracker():
    subprocess.run([sys.executable, "src/tracker.py"])

def start_dashboard():
    subprocess.run([sys.executable, "src/app.py"])

if __name__ == "__main__":
    args = sys.argv[1:]

    if "--track" in args:
        print("Starting tracker only...")
        start_tracker()

    elif "--dash" in args:
        print("Starting dashboard only...")
        start_dashboard()

    else:
        print("Starting Time Tracker...")
        print("Dashboard will be available at http://127.0.0.1:5000")
        print("Press Ctrl+C to stop.\n")

        # Run both tracker and dashboard in parallel
        tracker_thread = threading.Thread(target=start_tracker)
        dash_thread    = threading.Thread(target=start_dashboard)

        tracker_thread.daemon = True
        dash_thread.daemon    = True

        tracker_thread.start()
        dash_thread.start()

        # Keep main.py alive until Ctrl+C
        try:
            tracker_thread.join()
        except KeyboardInterrupt:
            print("\nTime Tracker stopped.")