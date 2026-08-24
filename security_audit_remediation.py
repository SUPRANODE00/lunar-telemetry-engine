import json
import subprocess
from datetime import datetime, timezone

def run_audit():
    print("--- INITIATING CAPSULECRAFT SECURITY AUDIT ---")
    audit_results = {
        "entity": "Erik Ivan Rivera",
        "module": "Security Audit & Remediation",
        "status": "SEC_AUDIT_IN_PROGRESS",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "actions_taken": []
    }

    # Run pip-audit if requirements.txt exists
    try:
        pip_audit_res = subprocess.run(["pip-audit", "--format=json"], capture_output=True, text=True)
        if pip_audit_res.returncode == 0:
            audit_results["pip_audit"] = "No vulnerabilities found."
        else:
            audit_results["pip_audit"] = json.loads(pip_audit_res.stdout) if pip_audit_res.stdout else "Vulnerabilities detected and logged."
        audit_results["actions_taken"].append("Executed Python pip-audit scan.")
    except Exception as e:
        audit_results["pip_audit_error"] = str(e)

    # Run npm audit fix if package.json exists
    try:
        npm_res = subprocess.run(["npm", "audit", "fix", "--json"], capture_output=True, text=True)
        audit_results["npm_audit_fix"] = json.loads(npm_res.stdout) if npm_res.stdout else "Node audit completed."
        audit_results["actions_taken"].append("Executed npm audit fix.")
    except Exception as e:
        audit_results["npm_audit_error"] = str(e)

    # Write report
    with open("security_audit_report.json", "w") as f:
        json.dump(audit_results, f, indent=2)

    print("--- SECURITY AUDIT REPORT GENERATED: security_audit_report.json ---")

if __name__ == "__main__":
    run_audit()
