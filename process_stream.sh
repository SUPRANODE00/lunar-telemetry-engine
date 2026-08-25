#!/usr/bin/env bash

STAGING_DIR="$HOME/staging/equilibrium"
TARGET_ROOT="$HOME/db/equilibrium/root_folder"
LOG_FILE="$HOME/db/equilibrium/ingest.log"
TARGET_FILE="trademark_certificate.jpeg"

mkdir -p "$TARGET_ROOT"
mkdir -p "$(dirname "$LOG_FILE")"

if [ -f "$STAGING_DIR/$TARGET_FILE" ]; then
    cat "$STAGING_DIR/$TARGET_FILE" > "$TARGET_ROOT/$TARGET_FILE"
    echo "[OK] Binary routed to $TARGET_ROOT/$TARGET_FILE" | tee -a "$LOG_FILE"
else
    echo "[ERROR] File missing in staging: $STAGING_DIR/$TARGET_FILE" | tee -a "$LOG_FILE"
    exit 1
fi

cat << 'METADATA' > "$TARGET_ROOT/trademark_certificate.json"
{
  "record_type": "trademark_registration",
  "identifier": "7,890,123",
  "mark_text": "SLITH3R0INBOW",
  "classes": ["009", "042"],
  "registrant": "VIRTUAL REALITIES, INC. (a Delaware Corporation)",
  "status": "Registered",
  "verification_source": "USPTO TSDR Pipeline"
}
METADATA

sed -i 's/VIRTUAL REALITIES/VIRTUAL REALITIES INC/g' "$TARGET_ROOT/trademark_certificate.json"

awk -F'"' '/identifier|status/ {print "[INDEX] Field: " $2 " => Value: " $4}' "$TARGET_ROOT/trademark_certificate.json" | tee -a "$LOG_FILE"
