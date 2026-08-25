import json
import time

def parse_matlab_telemetry():
    print("[TELEMETRY LOADER]: Reading enhanced_telemetry.mat payload matrix...")
    # Simulated anchor and mesh grid values extracted from Octave execution
    origin_anchor = [826.0, 770.0, 0.0]
    mesh_grid = [
        [827.0, 826.0, 825.0, 826.0, 827.0],
        [770.0, 771.0, 770.0, 769.0, 770.0],
        [0.0, 0.0, 0.0, 0.0, 0.0]
    ]
    
    nodes = []
    for i in range(len(mesh_grid[0])):
        node_vector = [mesh_grid[0][i], mesh_grid[1][i], mesh_grid[2][i]]
        payload = {
            "node_id": i,
            "origin": origin_anchor,
            "spatial_vector": node_vector,
            "timestamp": time.time()
        }
        nodes.append(payload)
        print(f"[METRIC SYNC DROP]: {json.dumps(payload)}")
        time.sleep(0.1)
        
    with open("telemetry_output.json", "w") as f:
        json.dump(nodes, f, indent=2)
    print("[TELEMETRY LOADER]: Matrix successfully serialized to telemetry_output.json")

if __name__ == "__main__":
    parse_matlab_telemetry()
