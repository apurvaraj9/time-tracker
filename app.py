from flask import Flask, render_template, jsonify
from database import init_db, get_today_summary, get_today_detail
import datetime

app = Flask(__name__)
init_db()

@app.route("/")
def dashboard():
    """Serves the main dashboard page."""
    today = datetime.datetime.now().strftime("%A, %d %B %Y")
    return render_template("dashboard.html", today=today)

@app.route("/api/summary")
def api_summary():
    """Returns today's category summary as JSON for the chart."""
    df = get_today_summary()
    data = {
        "labels": df["category"].tolist(),
        "values": [round(v, 1) for v in df["total_minutes"].tolist()]
    }
    return jsonify(data)

@app.route("/api/detail")
def api_detail():
    """Returns today's detailed session log as JSON."""
    df = get_today_detail()
    # Convert to list of dicts for JSON
    records = df.head(50).to_dict(orient="records")
    return jsonify(records)

if __name__ == "__main__":
    app.run(debug=True)