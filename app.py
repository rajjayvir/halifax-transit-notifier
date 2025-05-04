from flask import Flask, request
import sqlite3
from sms_sender import send_sms
from gtfs_parser import get_bus_info

app = Flask(__name__)

# DB setup (runs once)
def init_db():
    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                phone TEXT PRIMARY KEY,
                carrier TEXT
            )
        ''')
init_db()

@app.route('/sms', methods=['POST'])
def sms_handler():
    print("🔔 /sms endpoint hit")

    phone = request.form.get('phone')
    stop = request.form.get('stop')
    print(f"Received request: phone={phone}, stop={stop}")
    phone = request.form.get('phone')
    stop = request.form.get('stop')

    if not phone or not stop:
        return "Missing phone or stop", 400

    # Look up carrier
    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()
        c.execute('SELECT carrier FROM users WHERE phone = ?', (phone,))
        row = c.fetchone()

    if not row:
        return "Please reply with your carrier: Bell, Rogers, Telus, etc."

    carrier_gateway = row[0]

    # Get bus info
    bus_info = get_bus_info(stop)
    if not bus_info:
        bus_info = "No buses found."

    # Send SMS
    send_sms(phone, carrier_gateway, bus_info)
    return "Sent!"
    
if __name__ == "__main__":
    app.run(debug=True)
