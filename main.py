from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI(title="Capsule Telemetry Geofence Broadcast Engine")

class TelemetryPayload(BaseModel):
    entity: str
    phone: str
    geofence_targets: list[str]
    incident_data: dict

@app.post("/api/v1/transmit-geofence")
async def transmit_geofence(payload: TelemetryPayload):
    results = {}
    async with httpx.AsyncClient() as client:
        for target in payload.geofence_targets:
            try:
                response = await client.post(f"https://{target}/ingest", json=payload.dict(), timeout=5.0)
                results[target] = {"status": response.status_code, "response": response.text}
            except Exception as e:
                results[target] = {"status": "failed", "error": str(e)}
                
    return {"broadcast_status": "dispatched", "nodes": results}
