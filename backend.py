from flask import Flask, request, jsonify
import smtplib, ssl, os

app = Flask(__name__)

EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")

@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        data = request.get_json()
        receiver = data["to"]
        subject = data["subject"]
        message = data["message"]

        email_text = f"Subject: {subject}\n\n{message}"

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, receiver, email_text)

        return jsonify({"success": True, "msg": "Email sent"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
