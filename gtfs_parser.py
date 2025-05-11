import pandas as pd
from datetime import datetime

# Load GTFS static data
GTFS_PATH = "gtfs_data_static/"

stops = pd.read_csv(GTFS_PATH + "stops.txt")
routes = pd.read_csv(GTFS_PATH + "routes.txt")
trips = pd.read_csv(GTFS_PATH + "trips.txt")
stop_times = pd.read_csv(GTFS_PATH + "stop_times.txt")
calendar = pd.read_csv(GTFS_PATH + "calendar.txt")
calendar_dates = pd.read_csv(GTFS_PATH + "calendar_dates.txt")

def get_active_service_ids():
    today = datetime.strptime("20250525", "%Y%m%d").date()
    weekday = today.strftime('%A').lower()
    today_str = today.strftime('%Y%m%d')

    calendar['day_active'] = calendar[weekday] == 1
    calendar['start'] = pd.to_datetime(calendar['start_date'], format="%Y%m%d")
    calendar['end'] = pd.to_datetime(calendar['end_date'], format="%Y%m%d")
    calendar_active = calendar[
        (calendar['day_active']) &
        (calendar['start'] <= pd.Timestamp(today)) &
        (calendar['end'] >= pd.Timestamp(today))
    ]['service_id'].tolist()

    calendar_dates['date'] = calendar_dates['date'].astype(str)
    additions_today = calendar_dates[
        (calendar_dates['date'] == today_str) & (calendar_dates['exception_type'] == 1)
    ]['service_id'].tolist()

    removals_today = calendar_dates[
        (calendar_dates['date'] == today_str) & (calendar_dates['exception_type'] == 2)
    ]['service_id'].tolist()

    active_service_ids = set(calendar_active + additions_today) - set(removals_today)
    print(f"🗓️ Active services for today ({today_str}): {sorted(active_service_ids)}")
    return list(active_service_ids)

def get_schedule_for_stop(stop_code, max_results=3):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    # Ensure stop_code is str for comparison
    stop_code_str = str(stop_code).strip()
    stops['stop_code'] = stops['stop_code'].astype(str).str.strip()
    stops['stop_id'] = stops['stop_id'].astype(str).str.strip()

    # Debug print first few stop codes
    print("🔍 Preview of stop_codes:", stops['stop_code'].dropna().unique()[:10])

    # Try match by stop_code first
    matched_stop = stops[stops['stop_code'] == stop_code_str]

    # Fallback: Try matching stop_id directly if no stop_code match
    if matched_stop.empty and stop_code_str in stops['stop_id'].values:
        print(f"⚠️ stop_code '{stop_code_str}' not found. Trying as stop_id...")
        matched_stop = stops[stops['stop_id'] == stop_code_str]

    if matched_stop.empty:
        return f"❌ Stop code or ID '{stop_code}' not found.", []

    stop_id = matched_stop.iloc[0]['stop_id']
    active_services = get_active_service_ids()

    stop_times_for_stop = stop_times[stop_times['stop_id'] == int(stop_id)]
    upcoming = stop_times_for_stop[stop_times_for_stop['departure_time'] > current_time]

    upcoming = upcoming.merge(trips, on='trip_id')
    upcoming = upcoming[upcoming['service_id'].isin(active_services)]
    upcoming = upcoming.merge(routes, on='route_id')
    upcoming = upcoming.sort_values('departure_time').head(max_results)

    if upcoming.empty:
        return f"⚠️ No upcoming buses at stop {stop_code} today.", []

    messages = []
    metadata = []

    for _, row in upcoming.iterrows():
        route = row['route_short_name']
        time = row['departure_time'][:5]
        destination = row['trip_headsign']
        messages.append(f"🚌 Route {route} – {time} to {destination}")

        metadata.append({
            "stop_id": stop_id,
            "trip_id": row['trip_id'],
            "route_id": row['route_id'],
            "departure_time": row['departure_time'],
        })

    return "\n".join(messages), metadata

# Terminal test block
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("❌ Please provide a stop code or stop ID (e.g., 8312 or 6103)")
        sys.exit(1)

    stop_code = sys.argv[1]
    message, meta = get_schedule_for_stop(stop_code)
    print("\n📩 Formatted SMS:\n", message)
    print("\n🧾 Raw Metadata:\n", meta)
