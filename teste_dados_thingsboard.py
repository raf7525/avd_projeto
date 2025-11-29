#!/usr/bin/env python3
"""
Script simplificado para enviar dados diretamente com timestamp Unix
"""
import requests
import json
import time
from datetime import datetime

# Configurações
THINGSBOARD_HOST = "http://localhost:8080"
USERNAME = "tenant@thingsboard.org"
PASSWORD = "tenant"
FASTAPI_HOST = "http://localhost:8060"

def get_token():
    login_url = f"{THINGSBOARD_HOST}/api/auth/login"
    login_data = {"username": USERNAME, "password": PASSWORD}
    
    response = requests.post(login_url, json=login_data, timeout=10)
    if response.status_code == 200:
        return response.json().get("token")
    return None

def send_test_data():
    """Enviar dados de teste diretamente via REST API"""
    token = get_token()
    if not token:
        print("❌ Erro no login")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Buscar dispositivos
    devices_url = f"{THINGSBOARD_HOST}/api/tenant/devices?pageSize=50&page=0"
    response = requests.get(devices_url, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Erro ao buscar dispositivos: {response.status_code}")
        return
    
    devices = response.json().get("data", [])
    thermal_device = None
    
    for device in devices:
        if "Térmico" in device.get("name", "") or "Sensor" in device.get("name", ""):
            thermal_device = device
            break
    
    if not thermal_device:
        print("❌ Dispositivo térmico não encontrado")
        return
    
    device_id = thermal_device["id"]["id"]
    print(f"✅ Dispositivo encontrado: {thermal_device['name']} ({device_id})")
    
    # Enviar telemetria via REST API
    telemetry_url = f"{THINGSBOARD_HOST}/api/v1/{device_id}/telemetry"
    
    # Dados de teste com timestamp atual
    now_ms = int(time.time() * 1000)
    
    test_data = {
        "ts": now_ms,
        "values": {
            "temperatura": 25.5,
            "umidade": 60.0,
            "velocidade_vento": 10.0,
            "pressao": 1013.25,
            "radiacao_solar": 750.0,
            "sensacao_termica": 26.8,
            "zona_conforto": "Confortável"
        }
    }
    
    response = requests.post(telemetry_url, headers=headers, json=test_data, timeout=10)
    
    if response.status_code == 200:
        print("✅ Dados enviados com sucesso!")
        print(f"📊 Temp: {test_data['values']['temperatura']}°C")
        print(f"🌡️  Sensação: {test_data['values']['sensacao_termica']}°C")
        print(f"🎯 Zona: {test_data['values']['zona_conforto']}")
    else:
        print(f"❌ Erro ao enviar dados: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    print("🌡️ Enviando Dados de Teste para ThingsBoard")
    print("=" * 45)
    send_test_data()
    print("\n🔄 Atualize a página do ThingsBoard para ver os dados!")