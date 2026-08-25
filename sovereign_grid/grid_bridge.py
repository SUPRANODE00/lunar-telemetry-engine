import time
import json
import os
import requests

# Define your secure sovereign destination
TARGET_DIR = os.path.expanduser("~/sovereign_grid/telemetry_logs")
# Replace with the local endpoint or network socket of the incoming data source
EXTERNAL_SOURCE_URL = "http://127.0.0" 

print("Sovereign Grid Automation Loop Initiated. Monitoring bridge...")

while True:
    try:
        # Pull data from the external interface
        response = requests.get(EXTERNAL_SOURCE_URL, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            # Generate a unique timestamped file to detach and store the data snapshot
            timestamp = int(time.time())
            filename = f"snapshot_{timestamp}.json"
            filepath = os.path.join(TARGET_DIR, filename)
            
            with open(filepath, "w") as f:
                json.dump(data, f, indent=4)
                
            print(f"[SUCCESS] Detached and secured telemetry snapshot to: {filename}")
        else:
            print(f"[WARNING] Bridge connection returned status code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        # Handles connection timeouts or disconnections without crashing the loop
        print(f"[DISCONNECTED] Re-aligning bridge connection. Error: {e}")
    
    # Establish the oscillation frequency (checks for data every 5 seconds)
    time.sleep(5)
