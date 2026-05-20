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
SENDER_EMAIL  = "jhonlegarda1.2@gmail.com"       # Tu correo remitente
SENDER_PASS   = "fley miwp lvth eqfw"        # Contraseña de aplicación (no tu pass real)
TARGET_EMAIL  = "jhonlegarda1.2@gmail.com"   # Tu correo destino (el tuyo)
PHISHING_URL  = "http://127.0.0.1:5000"      # URL de tu servidor local

# --- CUERPO HTML del correo ---
HTML_BODY = f"""
<html>
<body style="font-family:Arial,sans-serif;background:#f1f3f4;padding:20px;">
  <div style="max-width:500px;margin:auto;background:#fff;border-radius:8px;padding:32px;border:1px solid #dadce0;">
    <div style="text-align:center;margin-bottom:24px;">
      <img src="https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png" height="30" alt="Google">
    </div>
    <h2 style="font-weight:400;color:#202124;">Actividad inusual en tu cuenta</h2>
    <p style="color:#5f6368;font-size:14px;line-height:1.6;">
      Hemos detectado un intento de acceso desde un dispositivo nuevo.<br>
      Verifica tu identidad para proteger tu cuenta.
    </p>
    <div style="text-align:center;margin:32px 0;">
      <a href="{PHISHING_URL}"
         style="background:#1a73e8;color:#fff;padding:12px 28px;border-radius:4px;
                text-decoration:none;font-size:14px;font-weight:500;">
        Revisar actividad
      </a>
    </div>
    <p style="color:#80868b;font-size:12px;text-align:center;">
      Si no reconoces esta actividad, ignora este correo.
    </p>
  </div>
</body>
</html>
"""

def send():
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Alerta de seguridad: actividad inusual en tu cuenta"
    msg["From"]    = f"Google Security <{SENDER_EMAIL}>"
    msg["To"]      = TARGET_EMAIL
    msg.attach(MIMEText(HTML_BODY, "html"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASS)
        server.sendmail(SENDER_EMAIL, TARGET_EMAIL, msg.as_string())
        print(f"[+] Correo enviado a {TARGET_EMAIL}")

if __name__ == "__main__":
    send()
