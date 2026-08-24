import json
import logging
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [D3M13N-INJUNCTION] - %(levelname)s - %(message)s')

def assign_node_compartment():
    payload = {
        "node_id": "node_origin_xyz_01",
        "toml_url": "https://blackcorp.me/toml/compartment_injunction.toml",
        "ein": "D3M13N-EIN-RECORD",
        "notice": "NOT CONSENTED BY ME, SEARCHING DETAILS FOR COMPARTMENT INJUNCTIONS",
        "authority": "D3M13N CAPSULECRAFT",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "INJUNCTION_QUARANTINE_ACTIVE"
    }
    
    with open("node_injunction_audit.json", "w") as f:
        json.dump(payload, f, indent=2)
        
    logging.info("Node assignment and non-consent TOML injunction record created.")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    assign_node_compartment()
