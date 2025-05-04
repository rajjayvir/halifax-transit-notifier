from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os
from sms_sender import send_sms
from gtfs_parser import get_bus_info

app = Flask(__name__)

# Load DB URL from environment
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

# User model
class User(db.Model):
    phone = db.Column(db.String, primary_key=True)
    carrier = db.Column(db.String)

# Create tables if not exist
with app.app_context():
    db.create_all()

@app.route('/sms', methods=['POST'])
def sms_handler():
    print("🔔 /sms endpoint hit")

    phone = request.form.get('phone')
    stop = request.form.get('stop')
    if not phone or not stop:
        return "Missing phone or stop", 400

    user = User.query.filter_by(phone=phone).first()
    if not user:
        return "Please reply with your carrier: Bell, Rogers, Telus, etc."

    carrier_gateway = user.carrier
    bus_info = get_bus_info(stop) or "No buses found."
    send_sms(phone, carrier_gateway, bus_info)

    return "Sent!"

@app.route('/register', methods=['POST'])
def register_user():
    phone = request.form.get('phone')
    carrier = request.form.get('carrier')

    if not phone or not carrier:
        return "Missing phone or carrier", 400

    existing_user = User.query.filter_by(phone=phone).first()
    if existing_user:
        return "Phone already registered", 400

    new_user = User(phone=phone, carrier=carrier)
    db.session.add(new_user)
    db.session.commit()

    return "User registered successfully"
