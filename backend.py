from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib, ssl, os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # <-- force allow all

EMAIL_USER = os.environ.get("EMAIL_USER", "toqitamimprotik@gmail.com")
EMAIL_PASS = os.environ.get("EMAIL_PASS", "vjakoxonkqweqqqt")

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.json
        to_addr = data['to']
        subject = data['subject']
        message = data['message']

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, to, f"Subject: {subject}\n\n{message}")

        return jsonify(success=True), 200   # ✅ always lowercase true
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

