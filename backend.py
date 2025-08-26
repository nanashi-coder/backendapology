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
        subject = data['subject']       # ✅ contains YES / NOT YET
        message = data['message']       # ✅ contains Forgiven / Not forgiven

        # Build full email body
        email_text = f"Subject: {subject}\n\n{message}"

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_addr, email_text)

        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
