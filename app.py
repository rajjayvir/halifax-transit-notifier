from flask import Flask, request
from sms_sender import send_sms
from gtfs_parser import get_schedule_for_stop

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return "pong", 200

@app.route('/sms', methods=['POST'])
def sms_handler():
    print("🔔 /sms endpoint hit")

    phone = request.form.get('From')
    stop_code = request.form.get('Body')

    if not phone or not stop_code:
        return "Missing phone or stop code", 400

    print(f"📥 Received request: phone={phone}, stop={stop_code}")

    # Call GTFS static function (will add real-time later)
    message, _ = get_schedule_for_stop(stop_code)

    # Send SMS reply
    send_sms(phone, message)

    return "OK", 200

if __name__ == "__main__":
    app.run(debug=True)
