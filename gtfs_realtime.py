# gtfs_realtime.py
import requests
from google.transit import gtfs_realtime_pb2

GTFS_TRIP_UPDATES_URL = "http://gtfs.halifax.ca/realtime/TripUpdate/TripUpdates.pb"

def fetch_trip_updates():
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(GTFS_TRIP_UPDATES_URL)
    feed.ParseFromString(response.content)
    return feed.entity

def get_predictions():
    data = {}
    for entity in fetch_trip_updates():
        if not entity.HasField("trip_update"):
            continue
        trip_id = entity.trip_update.trip.trip_id
        for stop_time in entity.trip_update.stop_time_update:
            stop_id = stop_time.stop_id
            if stop_time.HasField("arrival"):
                data[(trip_id, stop_id)] = stop_time.arrival.time  # UNIX timestamp
    return data
