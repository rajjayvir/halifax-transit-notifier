from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os
from sms_sender import send_sms
from gtfs_parser import get_bus_info

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# db = SQLAlchemy(app)

# # User model
# class User(db.Model):
#     phone = db.Column(db.String, primary_key=True)
#     carrier = db.Column(db.String)

# with app.app_context():
#     db.create_all()
# Send SMS via Twilio
@app.route('/sms', methods=['POST'])
def sms_handler():
    print("🔔 /sms endpoint hit")

    phone = request.form.get('From')
    message = request.form.get('Body')

    if not phone or not message:
        return "Missing phone or message", 400

    print(f"📥 Received from {phone}: {message}")

    bus_info = get_bus_info(message) or "No buses found at that stop."
    send_sms(phone, bus_info)

    return "OK", 200

if __name__ == "__main__":
    app.run()
