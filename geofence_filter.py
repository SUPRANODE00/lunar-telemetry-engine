# -----------------------------------------------------------------------------
# Copyright © 2026 Erik Ivan Rivera (D3M13N CAPSULECRAFT / SL1TH3R RAINBOW)
# SPDX-License-Identifier: LicenseRef-Proprietary
#
# Geofence Capsule Stream Filter: Restricts telemetry rendering to active
# sovereign spatial radius coordinates (Houston / Pasadena anchor grid).
# -----------------------------------------------------------------------------

import json
import math

# Sovereign Anchor Coordinates (Houston, TX Vector Base)
ANCHOR_LAT = 29.7604
ANCHOR_LON = -95.3698
MAX_GEOFENCE_RADIUS_KM = 50.0

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0 # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def filter_telemetry_stream(input_file="decoded_telemetry.json", output_file="parsed_nodes.json"):
    try:
        with open(input_file, 'r') as f:
            nodes = json.load(f)
    except FileNotFoundError:
        nodes = [
            {"node_id": 0, "lat": 29.7604, "lon": -95.3698, "spatial_vector": [5.0, 3.2, 1.1]},
            {"node_id": 1, "lat": 32.7767, "lon": -96.7970, "spatial_vector": [12.5, 8.1, 4.0]} # Out of bounds (Dallas)
        ]

    secured_nodes = []
    for node in nodes:
        dist = haversine_distance(ANCHOR_LAT, ANCHOR_LON, node.get("lat", ANCHOR_LAT), node.get("lon", ANCHOR_LON))
        if dist <= MAX_GEOFENCE_RADIUS_KM:
            node["geofence_status"] = "SECURE_INSIDE_UMBRELLA"
            secured_nodes.append(node)
        else:
            node["geofence_status"] = "OUTSIDE_JURISDICTION_FILTERED"

    with open(output_file, 'w') as f:
        json.dump(secured_nodes, f, indent=4)
    print(f"[GEOFENCE] Filtered {len(secured_nodes)} nodes within {MAX_GEOFENCE_RADIUS_KM}km sovereign radius.")

if __name__ == "__main__":
    filter_telemetry_stream()
