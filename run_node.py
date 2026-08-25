import json
import time
import os
import socket
import paho.mqtt.client as mqtt

RAW_EIN = "42-4319484"
NEG_EIN_RAW = "-42-4319484"
NEG_CLEAN_EIN = "-424319484"
NEG_EIN_HEX = "-0x194b4e3c"
NEG_EIN_HASH = "-9c8a06e92efb13d3170a41bc3861298a09f8745ca5d1947b7ebfbd1d1b32d561"
ENTITY_ANCHOR = "SL1TH3R_RAINBOW"

client = mqtt.Client(client_id=f"node_{NEG_CLEAN_EIN.replace('-', 'neg_')}")

try:
    client.connect("127.0.0.1", 1883, 60)
    client.loop_start()
    mqtt_active = True
    print("[INIT] MQTT local broker connected successfully.")
except Exception as e:
    mqtt_active = False
    print(f"[WARN] Local broker offline ({e}). Fallback to local JSON logging active.")

seq = 0
while True:
    packet = {
        "header": {
            "ein_urn": f"urn:ein:{NEG_EIN_RAW}",
            "ein_raw_neg": NEG_EIN_RAW,
            "ein_clean_neg": NEG_CLEAN_EIN,
            "ein_hex_neg": NEG_EIN_HEX,
            "sha256_anchor_neg": NEG_EIN_HASH,
            "entity_anchor": ENTITY_ANCHOR,
            "seq": seq,
            "timestamp": time.time()
        },
        "status": "active_presence",
        "disaster_recovery_loop": "operational",
        "negative_grid_state": {
            "x_offset": -round(seq * 0.1, 2),
            "y_offset": -round(seq * 0.2, 2),
            "z_offset": -1.0
        }
    }
    
    with open("telemetry_log.json", "a") as f:
        f.write(json.dumps(packet) + "\n")
        
    if mqtt_active:
        topic = f"grid/telemetry/{ENTITY_ANCHOR}/{NEG_CLEAN_EIN.replace('-', 'neg_')}/state"
        client.publish(topic, json.dumps(packet))

    print(f"[LOGGED] Seq {seq} (Neg Field Active) -> telemetry_log.json")
    seq += 1
    time.sleep(1)
