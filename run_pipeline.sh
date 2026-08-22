#!/usr/bin/env bash

TARGET_ROOT="$HOME/db/equilibrium/root_folder"
MASTER_INDEX="$HOME/db/equilibrium/equilibrium_union_index.json"
LOG_FILE="$HOME/db/equilibrium/ingest.log"

# Ensure directories exist
mkdir -p "$TARGET_ROOT"
mkdir -p "$(dirname "$LOG_FILE")"

# Generate placeholder binary/certificate asset if missing
if [ ! -f "$TARGET_ROOT/trademark_certificate.jpeg" ]; then
    touch "$TARGET_ROOT/trademark_certificate.jpeg"
    echo "[OK] Initialized binary asset placeholder." | tee -a "$LOG_FILE"
fi

# Generate metadata JSON sidecar
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

# Stream processing using sed & awk
sed -i 's/VIRTUAL REALITIES/VIRTUAL REALITIES INC/g' "$TARGET_ROOT/trademark_certificate.json"
awk -F'"' '/identifier|status/ {print "[INDEX] Field: " $2 " => Value: " $4}' "$TARGET_ROOT/trademark_certificate.json" | tee -a "$LOG_FILE"

# Build master union index
echo "[" > "$MASTER_INDEX"
first=1
for f in "$TARGET_ROOT"/*.json; do
    if [ -f "$f" ]; then
        if [ $first -eq 0 ]; then
            echo "," >> "$MASTER_INDEX"
        fi
        cat "$f" | awk '1' >> "$MASTER_INDEX"
        first=0
    fi
done
echo "]" >> "$MASTER_INDEX"

echo "[SYNC] Equilibrium union index updated successfully via stream pipeline." | tee -a "$LOG_FILE"
