import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [D3M13N-BROKER] - %(levelname)s - %(message)s')

class CellularCompartment:
    """Represents an isolated data cell within the cellular grid architecture."""
    def __init__(self, cell_id: str, payload_type: str, data: dict):
        self.cell_id = cell_id
        self.payload_type = payload_type
        self.data = data
        self.created_at = datetime.utcnow().isoformat()
        
    def extract_parameters(self) -> dict:
        """Returns localized telemetry fields for processing."""
        return {
            "cell_id": self.cell_id,
            "type": self.payload_type,
            "metrics": self.data
        }

class BrokerInferenceEngine:
    """Coordinates, routes, and processes inferences across isolated cells under D3M13N EIN."""
    def __init__(self):
        self.compartments = {}
        logging.info("Broker Cellular Inference Engine online under D3M13N CAPSULECRAFT authority.")

    def register_compartment(self, cell: CellularCompartment):
        """Secures a new cellular node into the broker registry."""
        self.compartments[cell.cell_id] = cell
        logging.info(f"Registered isolated cellular compartment: {cell.cell_id} ({cell.payload_type})")

    def run_cellular_inference(self, cell_id: str) -> dict:
        """Invokes isolated parameter inference on a specific cell target."""
        if cell_id not in self.compartments:
            raise KeyError(f"Target cell compartment {cell_id} not initialized in active grid.")
            
        cell = self.compartments[cell_id]
        params = cell.extract_parameters()
        
        logging.info(f"Initiating inference loop on isolated parameters for {cell_id}...")
        
        metrics = params["metrics"]
        inference_result = {"status": "UNKNOWN", "confidence": 0.0, "flagged_actions": []}
        
        if params["type"] == "FINANCIAL_LEDGER":
            balance = metrics.get("balance", 0.0)
            if balance == 0.0:
                inference_result = {"status": "CLOSED_DEBT_ZERO_BALANCE", "confidence": 0.99}
            else:
                inference_result = {"status": "ACTIVE_LIABILITY", "confidence": 0.95}
                
        elif params["type"] == "NETWORK_GRID":
            isp = metrics.get("isp", "")
            if "DoD" in isp or "nic.mil" in metrics.get("domain", ""):
                inference_result = {"status": "SECURE_SOVEREIGN_NODE", "confidence": 0.98, "flagged_actions": ["ATTACH_WITNESS"]}
                
        return {
            "target_cell": cell_id,
            "entity": "D3M13N CAPSULECRAFT",
            "timestamp": datetime.utcnow().isoformat(),
            "inference": inference_result
        }

if __name__ == "__main__":
    engine = BrokerInferenceEngine()
    
    financial_cell = CellularCompartment(
        cell_id="cell_fin_01",
        payload_type="FINANCIAL_LEDGER",
        data={"account_mask": "*1919", "balance": 0.0, "creditor": "T-Mobile"}
    )
    
    network_cell = CellularCompartment(
        cell_id="cell_net_01",
        payload_type="NETWORK_GRID",
        data={"ip_address": "7.26.16.11", "isp": "DoD Network Information Center", "domain": "nic.mil"}
    )
    
    engine.register_compartment(financial_cell)
    engine.register_compartment(network_cell)
    
    fin_output = engine.run_cellular_inference("cell_fin_01")
    net_output = engine.run_cellular_inference("cell_net_01")
    
    print("\n--- D3M13N INFERENCE STREAM OUTPUTS ---")
    print(json.dumps(fin_output, indent=2))
    print(json.dumps(net_output, indent=2))
