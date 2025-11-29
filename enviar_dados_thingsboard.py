#!/usr/bin/env python3
"""
Script para enviar dados térmicos da API FastAPI para o ThingsBoard
"""
import requests
import json
import time
from datetime import datetime

# Configurações ThingsBoard
THINGSBOARD_HOST = "http://localhost:8080"
USERNAME = "tenant@thingsboard.org"
PASSWORD = "tenant"

# Configurações API local
FASTAPI_HOST = "http://localhost:8060"

def get_thingsboard_token():
    """Obter token de autenticação do ThingsBoard"""
    login_url = f"{THINGSBOARD_HOST}/api/auth/login"
    login_data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    
    try:
        response = requests.post(login_url, json=login_data, timeout=10)
        if response.status_code == 200:
            token = response.json().get("token")
            print(f"✅ Token obtido com sucesso")
            return token
        else:
            print(f"❌ Erro ao fazer login: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return None

def create_device(token, device_name="Sensor Térmico AVD"):
    """Criar dispositivo no ThingsBoard"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    device_data = {
        "name": device_name,
        "type": "Sensor Térmico",
        "label": "Sensor de Sensação Térmica - AVD"
    }
    
    # Verificar se dispositivo já existe
    devices_url = f"{THINGSBOARD_HOST}/api/tenant/devices"
    try:
        response = requests.get(devices_url, headers=headers, timeout=10)
        if response.status_code == 200:
            devices = response.json().get("data", [])
            for device in devices:
                if device["name"] == device_name:
                    print(f"✅ Dispositivo '{device_name}' já existe")
                    return device["id"]["id"]
        else:
            print(f"❌ Erro ao listar dispositivos: {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️  Erro ao verificar dispositivos: {e}")
        return None
    
    # Criar novo dispositivo se não existir
    create_url = f"{THINGSBOARD_HOST}/api/device"
    try:
        response = requests.post(create_url, headers=headers, json=device_data, timeout=10)
        if response.status_code == 200:
            device_id = response.json()["id"]["id"]
            print(f"✅ Dispositivo criado: {device_id}")
            return device_id
        else:
            print(f"❌ Erro ao criar dispositivo: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return None

def get_device_access_token(token, device_id):
    """Obter token de acesso do dispositivo"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    credentials_url = f"{THINGSBOARD_HOST}/api/device/{device_id}/credentials"
    try:
        response = requests.get(credentials_url, headers=headers, timeout=10)
        if response.status_code == 200:
            credentials = response.json()
            access_token = credentials.get("credentialsId")
            print(f"✅ Token de acesso obtido: {access_token[:10]}...")
            return access_token
        else:
            print(f"❌ Erro ao obter credenciais: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return None

def get_thermal_data():
    """Obter dados térmicos da API local"""
    try:
        response = requests.get(f"{FASTAPI_HOST}/thermal/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            records = data.get("data", {}).get("records", [])
            print(f"✅ Obtidos {len(records)} registros térmicos")
            return records
        else:
            print(f"❌ Erro ao obter dados: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Erro de conexão com API: {e}")
        return []

def send_telemetry(access_token, thermal_data):
    """Enviar dados de telemetria para ThingsBoard"""
    telemetry_url = f"{THINGSBOARD_HOST}/api/v1/{access_token}/telemetry"
    
    for record in thermal_data:
        # Preparar dados para envio
        telemetry_data = {
            "temperatura": record["temperature"],
            "umidade": record["humidity"],
            "velocidade_vento": record["wind_velocity"],
            "pressao": record.get("pressure", 0),
            "radiacao_solar": record.get("solar_radiation", 0),
            "sensacao_termica": record["thermal_sensation"],
            "zona_conforto": record["comfort_zone"],
            "timestamp": record["timestamp"]
        }
        
        try:
            response = requests.post(telemetry_url, json=telemetry_data, timeout=10)
            if response.status_code == 200:
                print(f"✅ Dados enviados: {record['comfort_zone']} ({record['thermal_sensation']:.1f}°C)")
            else:
                print(f"❌ Erro ao enviar: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erro de conexão: {e}")
        
        # Aguardar um pouco entre envios
        time.sleep(0.5)

def main():
    print("🌡️ Enviando Dados Térmicos para ThingsBoard")
    print("=" * 50)
    
    # 1. Fazer login
    token = get_thingsboard_token()
    if not token:
        return
    
    # 2. Criar dispositivo
    device_id = create_device(token)
    if not device_id:
        return
    
    # 3. Obter token de acesso do dispositivo
    access_token = get_device_access_token(token, device_id)
    if not access_token:
        return
    
    # 4. Obter dados térmicos
    thermal_data = get_thermal_data()
    if not thermal_data:
        return
    
    # 5. Enviar telemetria
    print("\n📊 Enviando dados...")
    send_telemetry(access_token, thermal_data)
    
    print("\n✅ Processo concluído!")
    print(f"🌐 Acesse: {THINGSBOARD_HOST}/dashboards")
    print("📊 Vá em 'Dispositivos' > 'Sensor Térmico AVD' > 'Últimos Dados'")

if __name__ == "__main__":
    main()