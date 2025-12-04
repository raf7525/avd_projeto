import pandas as pd
import requests
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add project root to path to import other modules if needed
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Configuration
THINGSBOARD_HOST = os.getenv("THINGSBOARD_HOST", "http://localhost:8080")
FASTAPI_HOST = os.getenv("FASTAPI_HOST", "http://localhost:8060")
USERNAME = os.getenv("TB_USER", "tenant@thingsboard.org")
PASSWORD = os.getenv("TB_PASSWORD", "tenant")
DEVICE_NAME = "Sensor Térmico 01"
DEVICE_TYPE = "Thermal Sensor"

# Number of parallel workers
MAX_WORKERS = 10

def get_token():
    """Login to ThingsBoard and get JWT token"""
    url = f"{THINGSBOARD_HOST}/api/auth/login"
    try:
        response = requests.post(url, json={"username": USERNAME, "password": PASSWORD})
        response.raise_for_status()
        return response.json().get("token")
    except Exception as e:
        print(f"Error logging in: {e}")
        return None

def get_or_create_device(token):
    """Get device by name or create if it doesn't exist"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Check if device exists
    url = f"{THINGSBOARD_HOST}/api/tenant/devices?textSearch={DEVICE_NAME}&pageSize=10&page=0"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data['data']:
            device = data['data'][0]
            print(f"Found existing device: {device['name']} (ID: {device['id']['id']})")
            return device['id']['id']
    except Exception as e:
        print(f"Error searching for device: {e}")

    # Create device
    print(f"Creating new device: {DEVICE_NAME}")
    url = f"{THINGSBOARD_HOST}/api/device"
    device_data = {
        "name": DEVICE_NAME,
        "type": DEVICE_TYPE,
        "label": "Sensor de Temperatura e Umidade"
    }
    try:
        response = requests.post(url, headers=headers, json=device_data)
        response.raise_for_status()
        device = response.json()
        return device['id']['id']
    except Exception as e:
        print(f"Error creating device: {e}")
        return None

def get_device_token(token, device_id):
    """Get device credentials (access token)"""
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{THINGSBOARD_HOST}/api/device/{device_id}/credentials"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("credentialsId")
    except Exception as e:
        print(f"Error getting device credentials: {e}")
        return None

def send_telemetry(device_token, data):
    """Send telemetry data to ThingsBoard"""
    url = f"{THINGSBOARD_HOST}/api/v1/{device_token}/telemetry"
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        # print(f"Data sent: {data}")
    except Exception as e:
        print(f"Error sending telemetry: {e}")

def send_to_api(row):
    """Send data to FastAPI for storage"""
    url = f"{FASTAPI_HOST}/thermal_comfort/"
    try:
        payload = {
            "timestamp": row['timestamp'],
            "temperature": row['temperature'],
            "humidity": row['humidity'],
            "wind_velocity": row['wind_velocity'],
            "pressure": row['pressure'],
            "solar_radiation": row['solar_radiation']
        }
        requests.post(url, json=payload)
    except Exception:
        # print(f"Error sending to API: {e}")
        pass

def process_row(row, device_access_token):
    """Process a single row: send to ThingsBoard and API"""
    try:
        # Convert timestamp to milliseconds
        ts = int(pd.to_datetime(row['timestamp']).timestamp() * 1000)
        
        telemetry = {
            "ts": ts,
            "values": {
                "temperature": row['temperature'],
                "humidity": row['humidity'],
                "wind_velocity": row['wind_velocity'],
                "pressure": row['pressure'],
                "solar_radiation": row['solar_radiation'],
                "thermal_sensation": row['thermal_sensation'],
                "comfort_zone": row['comfort_zone']
            }
        }
        
        # Send to ThingsBoard
        send_telemetry(device_access_token, telemetry)
        
        # Send to FastAPI
        send_to_api(row)
        return True
    except Exception as e:
        print(f"Error processing row: {e}")
        return False

def main():
    print("Starting data ingestion to ThingsBoard...")
    
    # 1. Login
    token = get_token()
    if not token:
        return

    # 2. Get/Create Device
    device_id = get_or_create_device(token)
    if not device_id:
        return

    # 3. Get Device Access Token
    device_access_token = get_device_token(token, device_id)
    if not device_access_token:
        return

    # 4. Read Data
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_thermal_data.csv')
    if not os.path.exists(data_path):
        print(f"Data file not found at {data_path}. Please run convert_inmet_data.py to process data first.")
        return

    print(f"Reading data from {data_path}...")
    df = pd.read_csv(data_path)
    
    total_records = len(df)
    print(f"Sending {total_records} records to ThingsBoard with {MAX_WORKERS} workers...")
    
    # 5. Send Data in Parallel
    completed = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for index, row in df.iterrows():
            futures.append(executor.submit(process_row, row, device_access_token))
            
        for future in as_completed(futures):
            completed += 1
            if completed % 100 == 0:
                print(f"Processed {completed}/{total_records} records...")
            
    print("Ingestion complete!")

if __name__ == "__main__":
    main()
