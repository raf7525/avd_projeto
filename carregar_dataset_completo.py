#!/usr/bin/env python3
"""
Script para carregar e enviar TODOS os dados térmicos do CSV para ThingsBoard
"""
import csv
import requests
import json
import time
from datetime import datetime
import sys

# Configurações
THINGSBOARD_HOST = "http://localhost:8080"
USERNAME = "tenant@thingsboard.org"
PASSWORD = "tenant"
CSV_FILE = "data/sample_thermal_data.csv"
BATCH_SIZE = 50  # Enviar 50 registros por vez
DELAY_BETWEEN_BATCHES = 0.1  # Pausa entre lotes (segundos)

def get_device_token():
    """Obter token de acesso do dispositivo"""
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
    print(f"✅ Dispositivo: {device['name']}")
    
    # 3. Obter credenciais do dispositivo
    creds_url = f"{THINGSBOARD_HOST}/api/device/{device_id}/credentials"
    response = requests.get(creds_url, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Erro ao obter credenciais: {response.status_code}")
        return None
    
    credentials = response.json()
    access_token = credentials.get("credentialsId")
    print(f"✅ Token obtido: {access_token[:10]}...")
    
    return access_token

def load_csv_data():
    """Carregar dados do arquivo CSV"""
    data = []
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Converter tipos
                thermal_data = {
                    'timestamp': row['timestamp'],
                    'temperatura': float(row['temperature']),
                    'umidade': float(row['humidity']),
                    'velocidade_vento': float(row['wind_velocity']),
                    'pressao': float(row['pressure']),
                    'radiacao_solar': float(row['solar_radiation']),
                    'sensacao_termica': float(row['thermal_sensation']),
                    'zona_conforto': row['comfort_zone']
                }
                data.append(thermal_data)
        
        print(f"✅ Carregados {len(data)} registros do CSV")
        return data
    
    except Exception as e:
        print(f"❌ Erro ao ler CSV: {e}")
        return []

def send_batch_data(access_token, batch_data, batch_num):
    """Enviar um lote de dados"""
    telemetry_url = f"{THINGSBOARD_HOST}/api/v1/{access_token}/telemetry"
    
    success_count = 0
    
    for data in batch_data:
        try:
            # Converter timestamp para Unix timestamp (milissegundos)
            dt = datetime.fromisoformat(data['timestamp'].replace('T', ' '))
            timestamp_ms = int(dt.timestamp() * 1000)
            
            # Preparar payload com timestamp
            payload = {
                'ts': timestamp_ms,
                'values': {
                    'temperatura': data['temperatura'],
                    'umidade': data['umidade'],
                    'velocidade_vento': data['velocidade_vento'],
                    'pressao': data['pressao'],
                    'radiacao_solar': data['radiacao_solar'],
                    'sensacao_termica': data['sensacao_termica'],
                    'zona_conforto': data['zona_conforto']
                }
            }
            
            response = requests.post(telemetry_url, json=payload, timeout=5)
            
            if response.status_code == 200:
                success_count += 1
            else:
                print(f"⚠️  Erro no registro: {response.status_code}")
                
        except Exception as e:
            print(f"⚠️  Erro ao processar registro: {e}")
            continue
    
    return success_count

def main():
    print("🌡️ CARREGANDO DATASET COMPLETO PARA THINGSBOARD")
    print("=" * 55)
    
    # 1. Obter token de acesso
    access_token = get_device_token()
    if not access_token:
        return
    
    # 2. Carregar dados do CSV
    print(f"\n📂 Carregando dados de {CSV_FILE}...")
    csv_data = load_csv_data()
    if not csv_data:
        return
    
    total_records = len(csv_data)
    total_batches = (total_records + BATCH_SIZE - 1) // BATCH_SIZE
    
    print(f"📊 Total de registros: {total_records}")
    print(f"📦 Total de lotes: {total_batches}")
    print(f"⚡ Tamanho do lote: {BATCH_SIZE}")
    
    # 3. Enviar dados em lotes
    print(f"\n🚀 Iniciando envio...")
    total_success = 0
    
    try:
        for i in range(0, total_records, BATCH_SIZE):
            batch_num = (i // BATCH_SIZE) + 1
            batch_data = csv_data[i:i + BATCH_SIZE]
            
            print(f"📤 Lote {batch_num}/{total_batches} ({len(batch_data)} registros)...", end=" ")
            
            success = send_batch_data(access_token, batch_data, batch_num)
            total_success += success
            
            print(f"✅ {success}/{len(batch_data)} enviados")
            
            # Progress bar
            progress = (batch_num / total_batches) * 100
            bar_length = 30
            filled_length = int(bar_length * progress // 100)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            print(f"[{bar}] {progress:.1f}%")
            
            # Pausa entre lotes para não sobrecarregar
            if batch_num < total_batches:
                time.sleep(DELAY_BETWEEN_BATCHES)
                
    except KeyboardInterrupt:
        print(f"\n⚠️  Interrompido pelo usuário")
    
    # 4. Resultado final
    print(f"\n🎉 CONCLUÍDO!")
    print(f"✅ Registros enviados: {total_success}/{total_records}")
    print(f"📊 Taxa de sucesso: {(total_success/total_records)*100:.1f}%")
    
    if total_success > 0:
        print(f"\n🌐 Acesse o ThingsBoard:")
        print(f"   • Dispositivos > Sensor Térmico AVD > Última telemetria")
        print(f"   • Crie dashboards com {total_success} registros históricos!")

if __name__ == "__main__":
    main()