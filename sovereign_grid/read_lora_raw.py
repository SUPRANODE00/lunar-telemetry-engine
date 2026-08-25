#!/usr/bin/env python3
import serial
import sys
import time

port = sys.argv[1] if len(sys.argv) > 1 else '/dev/ttyACM0'
baud = 115200

print(f"[+] Opening Serial Port: {port} at {baud} baud...")

try:
    ser = serial.Serial(port, baud, timeout=1)
    while True:
        line = ser.readline()
        if line:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            try:
                decoded = line.decode('utf-8', errors='ignore').strip()
                if decoded:
                    print(f"[{timestamp}] [TXT] {decoded}")
            except Exception:
                print(f"[{timestamp}] [HEX] {line.hex(' ')}")
except KeyboardInterrupt:
    print("\n[*] Listener stopped.")
except Exception as e:
    print(f"[!] Error opening {port}: {e}")
