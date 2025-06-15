import requests
import urllib.parse
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
MAPBOX_TOKEN = os.environ.get("MAPBOX_TOKEN")
STYLES = os.environ.get("STYLES")
start_point_str = os.environ.get("START_POINT")
end_point_str = os.environ.get("END_POINT")

if not start_point_str or not end_point_str:
    raise RuntimeError("Please set START_POINT and END_POINT in your .env file.")
if not MAPBOX_TOKEN:
    raise RuntimeError("Please set MAPBOX_TOKEN in your .env file.")
if not STYLES:
    raise RuntimeError("Please set STYLES in your .env file.")

# Parse styles from env (just style IDs)
style_ids = [s.strip() for s in STYLES.split(",") if s.strip()]

# Coordinates
start_point = tuple(map(float, start_point_str.split(",")))
end_point = tuple(map(float, end_point_str.split(",")))

# Get route from Directions API
directions_url = (
    f"https://api.mapbox.com/directions/v5/mapbox/walking/"
    f"{start_point[0]},{start_point[1]};{end_point[0]},{end_point[1]}"
    f"?geometries=geojson&access_token={MAPBOX_TOKEN}"
)
directions_response = requests.get(directions_url)
directions = directions_response.json()
route_coords = directions["routes"][0]["geometry"]["coordinates"]

# GeoJSON for the route (red, with white outline for visibility)
geojson = {
    "type": "FeatureCollection",
    "features": [
        # White outline (thicker)
        {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": route_coords
            },
            "properties": {
                "stroke": "#ffffff",
                "stroke-width": 12,
                "stroke-opacity": 0.8
            }
        },
        # Main route (red)
        {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": route_coords
            },
            "properties": {
                "stroke": "#ff0000",
                "stroke-width": 6
            }
        }
    ]
}

geojson_str = urllib.parse.quote(json.dumps(geojson))

# Custom markers
start_marker = f"pin-l-circle+ff0000({start_point[0]},{start_point[1]})"
finish_marker = f"pin-l-star+ff0000({end_point[0]},{end_point[1]})"

# Map center and style
lons = [c[0] for c in route_coords]
lats = [c[1] for c in route_coords]
center = (sum(lons) / len(lons), sum(lats) / len(lats))
zoom = 16
size = (1280, 800)
center_str = f"{center[0]},{center[1]},{zoom}"
size_str = f"{size[0]}x{size[1]}"

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

for style_id in style_ids:
    # Use the last part of the style_id as the name
    style_name = style_id.split("/")[-1]
    output_file = f"banner-map_{style_name}_{timestamp}.png"
    url = (
        f"https://api.mapbox.com/styles/v1/{style_id}/static/"
        f"{start_marker},{finish_marker},geojson({geojson_str})/"
        f"{center_str}/{size_str}"
        f"?access_token={MAPBOX_TOKEN}"
    )
    print(f"Requesting styled map '{style_name}' from Mapbox...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"Styled map image saved as {output_file}")
    else:
        print(f"Error for style '{style_name}':", response.status_code, response.text)