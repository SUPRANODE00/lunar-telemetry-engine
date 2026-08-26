# -----------------------------------------------------------------------------
# Copyright © 2026 Erik Ivan Rivera (D3M13N CAPSULECRAFT / SL1TH3R RAINBOW)
# SPDX-License-Identifier: LicenseRef-Proprietary
#
# Thermal Sweep Integration: Maps AC/DC polarity and thermal spectral metrics
# onto capsule mesh nodes for enhanced HUD visualization and telemetry fidelity.
# -----------------------------------------------------------------------------

import json

def process_thermal_sweep(input_file="parsed_nodes.json", output_file="thermal_nodes.json"):
    try:
        with open(input_file, 'r') as f:
            nodes = json.load(f)
    except FileNotFoundError:
        nodes = [
            {"node_id": 0, "spatial_vector": [5.0, 3.2, 1.1], "geofence_status": "SECURE_INSIDE_UMBRELLA"}
        ]

    for node in nodes:
        vector = node.get("spatial_vector", [0.0, 0.0, 0.0])
        # Compute magnitude and simulated AC/DC polarity variance
        magnitude = sum([v**2 for v in vector]) ** 0.5
        polarity = "AC_THERMAL_SURGE" if magnitude > 10.0 else "DC_STABLE_COLD"
        
        node["thermal_metrics"] = {
            "magnitude": round(magnitude, 2),
            "polarity": polarity,
            "spectral_overlay": "RED_HEAT" if polarity == "AC_THERMAL_SURGE" else "BLUE_CYAN_COLD"
        }

    with open(output_file, 'w') as f:
        json.dump(nodes, f, indent=4)
        
    print(f"[THERMAL SWEEP] Processed {len(nodes)} nodes with AC/DC polarity spectral mappings.")

if __name__ == "__main__":
    process_thermal_sweep()
