import subprocess
import json
import sys
import time

def extract_mat_payload():
    print("[MAT DECODER]: Querying enhanced_telemetry.mat vector space...")
    try:
        # Stream Octave script output to decode matrix structure
        cmd = ["octave", "--eval", "load('enhanced_telemetry.mat'); disp(mesh_grid);"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        raw_lines = result.stdout.strip().split('\n')
        print(f"[MAT DECODER]: Extracted raw grid tensor:\n{result.stdout}")
        
        # Structure extraction payload
        payload = {
            "status": "ALIGNED",
            "raw_matrix": raw_lines,
            "timestamp": time.time()
        }
        
        with open("decoded_telemetry.json", "w") as f:
            json.dump(payload, f, indent=2)
            
        print("[MAT DECODER]: Spatial vector tensor stored in decoded_telemetry.json")
    except Exception as e:
        print(f"[MAT DECODER ERROR]: Failed to process matrix structure: {e}")
        sys.exit(1)

if __name__ == "__main__":
    extract_mat_payload()
