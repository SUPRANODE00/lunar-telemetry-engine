import json
import time
import tomllib
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import paho.mqtt.client as mqtt

# Load TOML Capsule Identity
with open("capsule_identity.toml", "rb") as f:
    config = tomllib.load(f)

pos_ein = config["identity"]["positive_anchor"]["ein_clean"]
neg_ein = config["identity"]["electronegative_equilibrium"]["ein_clean"]
anchor = config["capsule"]["entity_anchor"]
ingress_url = config["network"]["ingress"]["live_url"]

BROKER_HOST = "127.0.0.1"
WS_PORT = 9001
WS_PATH = "/mqtt"
HTTP_PORT = 8080

# Global state tracking for status endpoint
node_state = {
    "capsule_id": config["capsule"]["id"],
    "status": "initializing",
    "mqtt_connected": False,
    "seq": 0,
    "last_timestamp": 0,
    "ingress_url": ingress_url
}

# Embedded HTTP Health Check Handler
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ["/status", "/health", "/"]:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(node_state, indent=2).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Suppress standard HTTP access logging from cluttering stdin/stdout
        return

def start_http_server():
    server = HTTPServer(("0.0.0.0", HTTP_PORT), HealthCheckHandler)
    server.serve_forever()

# Start HTTP server in a non-blocking daemon thread
http_thread = threading.Thread(target=start_http_server, daemon=True)
http_thread.start()
print(f"[INIT] Health check endpoint active at http://0.0.0.0:{HTTP_PORT}/status")

# Initialize MQTT Client with API v2 over WebSockets
client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2, 
    client_id=f"capsule_node_{pos_ein}",
    transport="websockets"
)

client.ws_set_options(path=WS_PATH)

try:
    client.connect(BROKER_HOST, WS_PORT, 60)
    client.loop_start()
    mqtt_active = True
    node_state["mqtt_connected"] = True
    print(f"[INIT] WebSocket MQTT connected at ws://{BROKER_HOST}:{WS_PORT}{WS_PATH}")
except Exception as e:
    mqtt_active = False
    node_state["mqtt_connected"] = False
    print(f"[WARN] WebSocket broker offline ({e}). Local file logging active.")

seq = 0
while True:
    timestamp = time.time()
    packet = {
        "capsule_id": config["capsule"]["id"],
        "header": {
            "seq": seq,
            "timestamp": timestamp,
            "live_ingress_url": ingress_url
        },
        "positive_identity": {
            "urn": config["identity"]["positive_anchor"]["ein_urn"],
            "url": config["identity"]["positive_anchor"]["ingress_endpoint"],
            "grid_state": {"x": round(seq * 0.1, 2), "y": round(seq * 0.2, 2), "z": 1.0}
        },
        "electronegative_equilibrium": {
            "urn": config["identity"]["electronegative_equilibrium"]["ein_urn"],
            "url": config["identity"]["electronegative_equilibrium"]["ingress_endpoint"],
            "grid_state": {"x": -round(seq * 0.1, 2), "y": -round(seq * 0.2, 2), "z": -1.0}
        }
    }

    # Update global thread state
    node_state["status"] = "operational"
    node_state["seq"] = seq
    node_state["last_timestamp"] = timestamp

    with open("telemetry_log.json", "a") as f:
        f.write(json.dumps(packet) + "\n")

    if mqtt_active:
        client.publish(f"grid/telemetry/{anchor}/dual_state", json.dumps(packet))

    print(f"[STREAM] Seq {seq} | Dual Equilibrium over WebSockets -> telemetry_log.json")
    seq += 1
    time.sleep(1)

# Injected Satellite Airspace Broadcast Hook
import json

def get_satellite_broadcast_payload():
    try:
        with open('capsule_solar_vector.json', 'r') as f:
            vector_data = json.load(f)
        return {
            "node": "CAPSULE-SL1TH3R-RAINBOW-01",
            "sector": "SATELLITE-AIRSPACE-MESH",
            "uplink_target": "ORBITAL-GATEWAY-DEEP",
            "telemetry_matrix": vector_data
        }
    except Exception as e:
        return {"error": str(e)}
