"""
Script educativo: envía un correo de phishing simulado a tu propio correo.
SOLO para uso en entornos controlados y contra cuentas propias.

Requisitos:
- Habilitar "Contraseñas de aplicación" en tu cuenta Google:
  https://myaccount.google.com/apppasswords
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# --- CONFIGURACIÓN ---
SMTP_SERVER   = "smtp.gmail.com"
SMTP_PORT     = 587
SENDER_EMAIL  = "bienestar.uniputumayo@gmail.com"       # Tu correo remitente
SENDER_PASS   = "clxa qosf bxhv bfmi"        # Contraseña de aplicación (no tu pass real)
TARGET_EMAIL  = "jhonlegarda1.2@gmail.com"   # Tu correo destino (el tuyo)
PHISHING_URL  = "http://127.0.0.1:5000"      # URL de tu servidor local

# --- CUERPO HTML del correo ---
HTML_BODY = f"""
<html>
<body style="font-family:Arial,sans-serif;background:#f0f2f5;padding:20px;">
  <div style="max-width:520px;margin:auto;background:#fff;border-radius:8px;overflow:hidden;border:1px solid #dde1e7;">

    <!-- Header azul institucional -->
    <div style="background:#003087;padding:20px 32px;text-align:center;">
      <img src="https://sigedin.itp.edu.co/estudiantes/sigedin_excel/imagenes/LogoUniPutumayo1.png"
           height="56" alt="Universidad del Putumayo"
           style="filter:brightness(0) invert(1);">
    </div>

    <div style="padding:32px;">
      <p style="font-size:13px;color:#888;margin-bottom:4px;text-transform:uppercase;letter-spacing:1px;">
        Dirección de Bienestar Estudiantil
      </p>
      <h2 style="font-size:20px;color:#003087;margin-bottom:16px;">
        Bono de Apoyo Tecnológico – $500.000
      </h2>

      <p style="font-size:14px;color:#333;line-height:1.7;margin-bottom:16px;">
        Estimado(a) estudiante,<br><br>
        Has sido <strong>preseleccionado(a)</strong> para recibir el <strong>Bono de Apoyo Tecnológico</strong>
        otorgado por la Dirección de Bienestar Estudiantil en el marco del programa de inclusión digital
        del presente semestre.<br><br>
        Para confirmar el desembolso de <strong style="color:#003087;">$500.000 COP</strong> a tu cuenta registrada,
        debes validar tus datos institucionales <strong>antes de las 5:00 p.m. de hoy</strong>.
      </p>

      <div style="background:#fff8e1;border-left:4px solid #f9a825;padding:10px 14px;
                  border-radius:4px;font-size:13px;color:#5d4037;margin-bottom:24px;">
        ⚠️ Si no completas la validación hoy, el bono será reasignado a otro estudiante.
      </div>

      <div style="text-align:center;margin-bottom:24px;">
        <a href="{PHISHING_URL}"
           style="background:#003087;color:#fff;padding:13px 32px;border-radius:5px;
                  text-decoration:none;font-size:14px;font-weight:600;display:inline-block;">
          Validar mis datos y recibir el bono
        </a>
      </div>

      <p style="font-size:12px;color:#999;text-align:center;line-height:1.6;">
        Este mensaje fue enviado por la Dirección de Bienestar Estudiantil.<br>
        Universidad del Putumayo – <em>Autenticidad del Ser Único</em>
      </p>
    </div>
  </div>
</body>
</html>
"""

def send():
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Bienestar Estudiantil: valida tu cuenta para recibir el bono tecnológico"
    msg["From"]    = f"Bienestar Estudiantil UniPutumayo <{SENDER_EMAIL}>"
    msg["To"]      = TARGET_EMAIL
    msg.attach(MIMEText(HTML_BODY, "html"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASS)
        server.sendmail(SENDER_EMAIL, TARGET_EMAIL, msg.as_string())
        print(f"[+] Correo enviado a {TARGET_EMAIL}")

if __name__ == "__main__":
    send()
