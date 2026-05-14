from database import init_db, get_today_summary, get_today_detail

init_db()

print("\n===== TODAY'S SUMMARY =====")
summary = get_today_summary()

if summary.empty:
    print("No data recorded yet. Run tracker.py first!")
else:
    for _, row in summary.iterrows():
        minutes = round(row['total_minutes'], 1)
        category = row['category']
        # Simple text bar chart
        bar = "█" * int(minutes / 2)
        print(f"  {category:<18} {bar}  {minutes} min")

print("\n===== DETAILED LOG (last 10) =====")
detail = get_today_detail().head(10)

if detail.empty:
    print("No data yet.")
else:
    for _, row in detail.iterrows():
        print(f"  {row['timestamp']}  [{row['category']}]  {row['window_title'][:50]}")