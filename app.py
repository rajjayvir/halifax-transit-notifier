from flask import Flask, request
from sms_sender import send_sms
from gtfs_parser import get_schedule_for_stop
from gtfs_realtime import get_predictions
from datetime import datetime
from gtfs_updater import update_gtfs

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def sms_handler():
    print("🔔 /sms endpoint hit")

    phone = request.form.get('From')
    stop_code = request.form.get('Body')

    if not phone or not stop_code:
        return "Missing phone or stop code", 400

    print(f"📥 Received request: phone={phone}, stop={stop_code}")

    # Step 1: Static GTFS response
    message, trips = get_schedule_for_stop(stop_code)

    # Step 2: Try to inject live predictions
    predictions = get_predictions()
    live_messages = []

    for trip in trips:
        trip_id = str(trip["trip_id"])
        stop_id = str(trip["stop_id"])
        route = trip["route_id"]
        scheduled = str(trip["departure_time"])[:5]

        key = (trip_id, stop_id)
        if key in predictions:
            rt = datetime.fromtimestamp(predictions[key]).strftime("%H:%M")
            time = f"{rt} (live)"
        else:
            time = scheduled

        live_messages.append(f"🚌 {route} @ {time}")

    # Step 3: Combine message
    final_message = "\n".join(live_messages) if live_messages else message

    # Step 4: Send reply
    send_sms(phone, final_message)
    return "OK", 200

@app.route('/ping', methods=['GET'])
def ping():
    print(f"Ping received at {datetime.now()}")
    return "pong", 200

@app.route('/update-gtfs', methods=['GET'])
def update_gtfs_webhook():
    try:
        update_gtfs()
        return "✅ GTFS update completed", 200
    except Exception as e:
        print(f"❌ GTFS update failed: {e}")
        return f"GTFS update failed: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
