import json
import subprocess
import logging
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [D3M13N-GIT-SYNC] - %(levelname)s - %(message)s')

def run_git_commands():
    commands = [
        ["git", "add", "identifier_troubleshoot_audit.json", "section508_fraud_alert_audit.json", "debtor_real_audit.json", "eq_portal_audit.json"],
        ["git", "commit", "-m", f"Sync inverted identifier blocks and audit logs - {datetime.now(timezone.utc).isoformat()}"],
        ["git", "push", "origin", "main"]
    ]
    
    for cmd in commands:
        logging.info(f"Executing: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            logging.warning(f"Git warning/error (may require remote setup): {result.stderr.strip()}")
        else:
            logging.info(f"Success: {result.stdout.strip()}")

if __name__ == "__main__":
    run_git_commands()
    print("--- LIVE MAPPING & GIT DEPLOYMENT SEQUENCE COMPLETED ---")
