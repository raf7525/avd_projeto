import pandas as pd
import requests
import json
import time
import os
import sys
from datetime import datetime

# Add project root to path to import other modules if needed
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Configuration
THINGSBOARD_HOST = os.getenv("THINGSBOARD_HOST", "http://localhost:8080")
FASTAPI_HOST = os.getenv("FASTAPI_HOST", "http://localhost:8060")
USERNAME = os.getenv("TB_USER", "tenant@thingsboard.org")
PASSWORD = os.getenv("TB_PASSWORD", "tenant")
DEVICE_NAME = "Sensor Térmico 01"
DEVICE_TYPE = "Thermal Sensor"

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
    url = f"{FASTAPI_HOST}/thermal/"
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
    except Exception as e:
        # print(f"Error sending to API: {e}")
        pass

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
        print(f"Data file not found at {data_path}. Please run generate_thermal_data.py first.")
        # Optional: Run generation if missing
        # from generate_thermal_data import generate_thermal_data
        # df = generate_thermal_data()
        # df.to_csv(data_path, index=False)
        return

    print(f"Reading data from {data_path}...")
    df = pd.read_csv(data_path)
    
    print(f"Sending {len(df)} records to ThingsBoard...")
    
    # 5. Send Data
    # For demonstration, we'll send data with a small delay, or batch it.
    # Since it's historical data, we might want to send it all at once or simulate real-time.
    # For historical data in ThingsBoard, we need to include the 'ts' (timestamp) in milliseconds.
    
    for i, (index, row) in enumerate(df.iterrows()):
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
        
        # Send to ThingsBoard (only if needed - comment out if already populated)
        # send_telemetry(device_access_token, telemetry)
        
        # Send to FastAPI (for DB and S3 storage)
        send_to_api(row)
        
        if i % 100 == 0:
            print(f"Sent {i} records...")
            
    print("Ingestion complete!")

if __name__ == "__main__":
    main()
