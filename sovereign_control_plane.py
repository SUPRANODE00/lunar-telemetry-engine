import asyncio
import json
import logging
import time
import uuid
from dataclasses import asdict, dataclass
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

@dataclass
class EnvelopeHeader:
    message_id: str
    timestamp: float
    origin_agent_id: str
    tenant_domain: str
    schema_version: str

@dataclass
class EncapsulatedSignal:
    header: EnvelopeHeader
    payload_type: str
    data: dict
    signature_hash: str

class AccessController:
    @staticmethod
    def verify_token_claims(agent_id: str, tenant_domain: str) -> bool:
        return bool(agent_id and tenant_domain)

class DistributedSideAgent:
    def __init__(self, agent_id: str, tenant_domain: str):
        self.agent_id = agent_id
        self.tenant_domain = tenant_domain
        self.sequence_counter = 0

    def generate_signal(self, payload_type: str, metric_payload: dict) -> EncapsulatedSignal:
        self.sequence_counter += 1
        header = EnvelopeHeader(
            message_id=str(uuid.uuid4()),
            timestamp=time.time(),
            origin_agent_id=self.agent_id,
            tenant_domain=self.tenant_domain,
            schema_version="v2.1.0",
        )
        
        raw_content = f"{header.message_id}:{header.timestamp}:{metric_payload}"
        signature = str(hash(raw_content))

        return EncapsulatedSignal(
            header=header,
            payload_type=payload_type,
            data=metric_payload,
            signature_hash=signature,
        )

class ControlPlaneMesh:
    def __init__(self, heartbeat_ttl: float = 3.0):
        self.heartbeat_ttl = heartbeat_ttl
        self.active_registry: Dict[str, float] = {}
        self.event_stream: asyncio.Queue = asyncio.Queue()

    async def ingest_signal(self, signal: EncapsulatedSignal) -> bool:
        header = signal.header
        
        if not AccessController.verify_token_claims(header.origin_agent_id, header.tenant_domain):
            logging.warning(f"Ingress denied for Agent {header.origin_agent_id}: Policy violation.")
            return False

        self.active_registry[header.origin_agent_id] = time.time()
        await self.event_stream.put(signal)
        logging.info(f"[INGEST SUCCESS] Agent={header.origin_agent_id} | Type={signal.payload_type} | ID={header.message_id}")
        return True

    async def monitor_state_in_absence(self):
        while True:
            await asyncio.sleep(1.0)
            now = time.time()
            absent_agents = []

            for agent_id, last_seen in list(self.active_registry.items()):
                if now - last_seen > self.heartbeat_ttl:
                    absent_agents.append(agent_id)
                    del self.active_registry[agent_id]

            for agent_id in absent_agents:
                logging.error(f"[ALERT: STATE_IN_ABSENCE] Agent {agent_id} timed out. Triggering reconciliation.")

async def main():
    logging.info("Initializing Distributed Event Architecture Control Plane...")
    mesh = ControlPlaneMesh(heartbeat_ttl=2.5)

    agent_alpha = DistributedSideAgent(agent_id="AGENT_NODE_01", tenant_domain="telemetry.org")
    agent_beta = DistributedSideAgent(agent_id="AGENT_NODE_02", tenant_domain="telemetry.org")

    asyncio.create_task(mesh.monitor_state_in_absence())

    for _ in range(2):
        sig_a = agent_alpha.generate_signal("HEARTBEAT", {"status": "ACTIVE", "cpu_util": 12.4})
        sig_b = agent_beta.generate_signal("METRIC_SAMPLE", {"status": "ACTIVE", "signal_dbm": -68.0})
        
        await mesh.ingest_signal(sig_a)
        await mesh.ingest_signal(sig_b)
        await asyncio.sleep(1.0)

    logging.info("Simulating link disconnection on AGENT_NODE_02...")
    for _ in range(3):
        sig_a = agent_alpha.generate_signal("HEARTBEAT", {"status": "ACTIVE", "cpu_util": 14.1})
        await mesh.ingest_signal(sig_a)
        await asyncio.sleep(1.0)

if __name__ == "__main__":
    asyncio.run(main())
