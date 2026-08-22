import math
import scipy.io
import socket
import json

def load_telemetry(file_path):
    """Loads the stabilized matrix from the Octave environment."""
    try:
        mat_data = scipy.io.load_mat(file_path)
        return mat_data['enhanced_matrix']
    except Exception as e:
        print(f"[-] Inventory error mapping matrix: {e}")
        return None

def interpret_intent(matrix):
    """Processes phase variance and spatial drift from the cross-inventory matrix."""
    insights = []
    for idx, row in enumerate(matrix):
        lat, lon, alt, phase_variance = row
        insights.append({
            "node_vector": idx,
            "coordinates": [lat, lon],
            "altitude_m": alt,
            "variance": phase_variance,
            "stabilized": phase_variance < 0.15
        })
    return insights

def broadcast_beacon(payload, host='127.0.0.1', port=5555):
    """Broadcasts intent insights to local sovereign grid loopback compartments."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(json.dumps(payload).encode('utf-8'))
            print("[SUCCESS] Intent beacon successfully attached and transmitted.")
    except ConnectionRefusedError:
        print("[-] Loopback beacon offline. Verify local endpoint listener is running.")

if __name__ == "__main__":
    MAT_PATH = '/home/d3m13n/sovereign_grid/enhanced_telemetry.mat'
    print("=== GNSS Compute-Node Bridge Initializing ===")
    
    matrix = load_telemetry(MAT_PATH)
    if matrix is not None:
        insights = interpret_intent(matrix)
        print(f"[LOAD] Interpreted {len(insights)} node vectors.")
        broadcast_beacon({"status": "ACTIVE", "insights": insights})
