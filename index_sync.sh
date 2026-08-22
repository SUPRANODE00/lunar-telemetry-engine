#!/usr/bin/env bash

TARGET_ROOT="$HOME/db/equilibrium/root_folder"
MASTER_INDEX="$HOME/db/equilibrium/equilibrium_union_index.json"

mkdir -p "$(dirname "$MASTER_INDEX")"

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

echo "[SYNC] Equilibrium union index updated successfully via stream pipeline."
