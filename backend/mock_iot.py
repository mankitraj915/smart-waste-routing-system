import requests
import random
import time

API_URL = "http://127.0.0.1:8000/api/telemetry"

def send_mock_telemetry(num_bins=20):
    print("🚀 Starting IoT Simulation...")
    for i in range(1, num_bins + 1):
        payload = {
            "bin_id": i,
            "fill_percentage": round(random.uniform(10.0, 95.0), 2)
        }
        try:
            res = requests.post(API_URL, json=payload)
            print(f"✅ Bin {i} -> {payload['fill_percentage']}% | [{res.status_code}]")
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error - Ensure FastAPI is running on port 8000")
            return
        time.sleep(0.5)
        
if __name__ == "__main__":
    send_mock_telemetry()
