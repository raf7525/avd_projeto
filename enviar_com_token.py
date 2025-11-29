#!/usr/bin/env python3
"""
Script para obter credenciais e enviar dados via HTTP simples
"""
import requests
import json
import time

# Configurações
THINGSBOARD_HOST = "http://localhost:8080"
USERNAME = "tenant@thingsboard.org"
PASSWORD = "tenant"

def get_device_token():
    # 1. Login
    login_url = f"{THINGSBOARD_HOST}/api/auth/login"
    login_data = {"username": USERNAME, "password": PASSWORD}
    
    response = requests.post(login_url, json=login_data)
    if response.status_code != 200:
        print(f"❌ Erro no login: {response.status_code}")
        return None
    
    token = response.json().get("token")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Buscar dispositivo
    devices_url = f"{THINGSBOARD_HOST}/api/tenant/devices?pageSize=50&page=0"
    response = requests.get(devices_url, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Erro ao buscar dispositivos: {response.status_code}")
        return None
    
    devices = response.json().get("data", [])
    device = None
    
    for d in devices:
        if "Térmico" in d.get("name", ""):
            device = d
            break
    
    if not device:
        print("❌ Dispositivo não encontrado")
        return None
    
    device_id = device["id"]["id"]
    print(f"✅ Dispositivo: {device['name']} ({device_id})")
    
    # 3. Obter credenciais do dispositivo
    creds_url = f"{THINGSBOARD_HOST}/api/device/{device_id}/credentials"
    response = requests.get(creds_url, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Erro ao obter credenciais: {response.status_code}")
        return None
    
    credentials = response.json()
    access_token = credentials.get("credentialsId")
    print(f"✅ Token de acesso: {access_token}")
    
    return access_token

def send_data_with_token(access_token):
    """Enviar dados usando token de acesso HTTP"""
    # URL para envio de telemetria via HTTP
    telemetry_url = f"{THINGSBOARD_HOST}/api/v1/{access_token}/telemetry"
    
    # Dados térmicos
    data = {
        "temperatura": 27.5,
        "umidade": 55.0,
        "velocidade_vento": 8.5,
        "pressao": 1018.0,
        "radiacao_solar": 680.0,
        "sensacao_termica": 28.2,
        "zona_conforto": "Quente"
    }
    
    print(f"📤 Enviando dados para: {telemetry_url}")
    
    response = requests.post(telemetry_url, json=data, timeout=10)
    
    if response.status_code == 200:
        print("✅ Dados enviados com sucesso!")
        for key, value in data.items():
            print(f"   {key}: {value}")
        return True
    else:
        print(f"❌ Erro: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def main():
    print("🔑 Obtendo Token e Enviando Dados")
    print("=" * 40)
    
    # Obter token
    access_token = get_device_token()
    if not access_token:
        return
    
    # Enviar dados
    print("\n📊 Enviando dados térmicos...")
    if send_data_with_token(access_token):
        print("\n🎉 Sucesso! Dados enviados para ThingsBoard")
        print("🔄 Atualize a página 'Última telemetria' do dispositivo")
    else:
        print("\n❌ Falha no envio")

if __name__ == "__main__":
    main()