from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os
from sms_sender import send_sms
from gtfs_parser import get_bus_info

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

# User model
class User(db.Model):
    phone = db.Column(db.String, primary_key=True)
    carrier = db.Column(db.String)

with app.app_context():
    db.create_all()

# List of valid carrier gateways
KNOWN_CARRIERS = ["bell", "rogers", "telus", "vmobile.ca"]

@app.route('/sms', methods=['POST'])
def sms_handler():
    print("🔔 /sms endpoint hit")

    phone = request.form.get('phone')
    message = request.form.get('stop')  # message from SMS form field

    if not phone or not message:
        return "Missing phone or message", 400

    user = User.query.filter_by(phone=phone).first()

    if user:
        # Registered user → treat message as stop code
        carrier_gateway = user.carrier
        bus_info = get_bus_info(message) or "No buses found."
        send_sms(phone, carrier_gateway, bus_info)
        return "Sent!"
    else:
        # Unregistered user → treat message as potential carrier
        carrier_guess = message.strip().lower()
        if carrier_guess in KNOWN_CARRIERS:
            new_user = User(phone=phone, carrier=carrier_guess)
            db.session.add(new_user)
            db.session.commit()
            send_sms(phone, carrier_guess, "✅ Carrier registered! Now send a stop code to get bus info.")
            return "Carrier registered!"
        else:
            return "Please reply with your carrier: Bell, Rogers, Telus, etc."

@app.route('/register', methods=['POST'])
def register_user():
    phone = request.form.get('phone')
    carrier = request.form.get('carrier')

    if not phone or not carrier:
        return "Missing phone or carrier", 400

    existing_user = User.query.filter_by(phone=phone).first()
    if existing_user:
        return "Phone already registered", 400

    new_user = User(phone=phone, carrier=carrier.lower())
    db.session.add(new_user)
    db.session.commit()

    return "User registered successfully"

@app.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return {
        "users": [{"phone": u.phone, "carrier": u.carrier} for u in users]
    }

@app.route('/delete', methods=['POST'])
def delete_user():
    phone = request.form.get('phone')
    user = User.query.filter_by(phone=phone).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return "User deleted"
    return "User not found", 404
