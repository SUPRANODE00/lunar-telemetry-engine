# lunar-telemetry-engine

# Lunar Telemetry Matrix Engine (`lunar-telemetry-engine`)

A lightweight POSIX shell and Python orchestration repository designed to ingest spatial coordinates, compute celestial zenith/elevation vectors, and filter log streams for real-time mesh node positioning.

## Architecture & System Flow

This repository calculates real-time lunar tracking metrics (Hour Angle, Elevation, Zenith Angle, and Azimuth) and processes raw telemetry outputs using standard command-line stream manipulation tools.

1. **Ingest Phase**: `telemetry_calc.py` calculates local sidereal time (LST) and directional vectors from geographic and astronomical inputs.
2. **Pipeline Stream Phase**: System outputs are redirected to log files for offline parsing or piped directly through Unix streams.
3. **Filter & Transform Phase**: Native POSIX utilities (`cat`, `sed`, `awk`) extract required field metrics without third-party binary dependencies.

---

## File Structure

```text
.
├── README.md
├── scripts/
│   ├── telemetry_calc.py
│   └── process_logs.sh
└── data/
    └── telemetry.log
