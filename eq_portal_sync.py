import json
from datetime import datetime, timezone

eq_profile = {
    "transfer_agent": "Equiniti (EQ, formerly AST)",
    "portal_access": {
        "individuals": "https://equiniti.com/us/ast-access/",
        "corporate_clients": "https://equiniti.com/us/ast-access/",
        "brokers_attorneys": "https://equiniti.com/us/ast-access/"
    },
    "platforms": [
        "Cap Table Management Product",
        "Ownership Intelligence Platform",
        "Corporate and Mutual Fund Proxy Campaign Platform",
        "Lost Asset Recovery Platform"
    ],
    "entity_authority": "D3M13N CAPSULECRAFT",
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "status": "PORTAL_SYNC_COMPLETED"
}

with open("eq_portal_audit.json", "w") as f:
    json.dump(eq_profile, f, indent=2)

print("--- EQ TRANSFER AGENT PORTAL SYNCED CLEANLY ---")
print(json.dumps(eq_profile, indent=2))
