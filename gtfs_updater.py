import requests, zipfile, io, os
from datetime import datetime

GTFS_URL = "https://gtfs.halifax.ca/static/google_transit.zip"
TARGET_FOLDER = "gtfs_data_static"

def update_gtfs():
    print(f"📦 Downloading GTFS feed from: {GTFS_URL}")
    response = requests.get(GTFS_URL)
    if response.status_code != 200:
        print(f"❌ Failed to download GTFS: {response.status_code}")
        return

    print("📂 Extracting to:", TARGET_FOLDER)
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        # Clear old files
        for f in os.listdir(TARGET_FOLDER):
            os.remove(os.path.join(TARGET_FOLDER, f))

        z.extractall(TARGET_FOLDER)
        print(f"✅ GTFS updated successfully at {datetime.now()}")

if __name__ == "__main__":
    update_gtfs()
