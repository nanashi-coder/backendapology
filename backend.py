from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib, ssl, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # allow all

EMAIL_USER = os.environ.get("EMAIL_USER", "toqitamimprotik@gmail.com")
EMAIL_PASS = os.environ.get("EMAIL_PASS", "vjakoxonkqweqqqt")

@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.get_json()
    print("DEBUG Received:", data, flush=True)

    to = data.get("to")
    subject = data.get("subject")
    message = data.get("message")

    try:
        # Build MIME email
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        # Send with Gmail SMTP
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, to, msg.as_string())

        return jsonify({"success": True}), 200

    except Exception as e:
        print("EMAIL ERROR:", e, flush=True)
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
