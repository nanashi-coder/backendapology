from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib, ssl

app = Flask(__name__)
CORS(app)  # <-- Allow cross-origin requests

EMAIL_USER = "toqitamimprotik@gmail.com"
EMAIL_PASS = "vjakoxonkqweqqqt"

@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        data = request.json
        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        subject = f"New message from {name}"
        body = f"From: {email}\n\n{message}"

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, EMAIL_USER, f"Subject: {subject}\n\n{body}")

        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
