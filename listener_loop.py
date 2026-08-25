import time
import telemetry_sync   # chained module with carrier alignment

def continuous_listener_loop(interval=60):
    print("--- STARTING CONTINUOUS TELEMETRY LISTENER LOOP ---")
    while True:
        try:
            telemetry_sync.confirm_telemetry_sync()
            print(">>> Telemetry sync cycle completed.")
        except Exception as e:
            print(f"!!! Error during telemetry sync cycle: {e}")
        time.sleep(interval)  # wait before next cycle

if __name__ == "__main__":
    continuous_listener_loop(interval=300)  # run every 5 minutes
