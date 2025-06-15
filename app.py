from flask import Flask, request, Response
import sqlite3
from datetime import datetime, timezone

app = Flask(__name__)

def insert_health_check():
    try:
        conn = sqlite3.connect("health.db")
        cursor = conn.cursor()
        utc_time = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
        cursor.execute("INSERT INTO health_check (datetime) VALUES (?)", (utc_time,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False

@app.route("/healthz", methods=["GET"])
def healthz():
    if request.data:
        return Response(status=400, headers={"Cache-Control": "no-cache", "Pragma": "no-cache", "X-Content-Type-Options": "nosniff"})

    success = insert_health_check()
    return Response(
        status=200 if success else 503,
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "X-Content-Type-Options": "nosniff"
        }
    )

@app.errorhandler(405)
def method_not_allowed(e):
    return Response(
        status=405,
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "X-Content-Type-Options": "nosniff"
        }
    )

if __name__ == "__main__":
    app.run(port=8080)
