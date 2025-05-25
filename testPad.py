from gtfs_parser import get_schedule_for_stop
from gtfs_realtime import get_predictions
from datetime import datetime

# Step 1: Get static GTFS schedule
stop_code = "6104"  # or any valid stop_code
message, metadata = get_schedule_for_stop(stop_code)

print("📩 Static message:\n" + message)

# Step 2: Fetch live predictions
predictions = get_predictions()

print("\n🔍 Real-time vs Scheduled:")
for trip in metadata:
    trip_id = str(trip["trip_id"])
    stop_id = str(trip["stop_id"])
    route = trip["route_id"]
    scheduled = str(trip["departure_time"])[:5]

    key = (trip_id, stop_id)
    if key in predictions:
        live_unix = predictions[key]
        live_time = datetime.fromtimestamp(live_unix).strftime("%H:%M")
        print(f"🚌 {route} → {live_time} (live) vs {scheduled} (scheduled)")
    else:
        print(f"🚌 {route} → {scheduled} (no live data)")
