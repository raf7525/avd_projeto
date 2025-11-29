#!/usr/bin/env python3
"""
Script para carregar AMOSTRA dos dados térmicos (primeiros 1000 registros)
"""
import csv
import requests
import time
from datetime import datetime

# Configurações
THINGSBOARD_HOST = "http://localhost:8080"
ACCESS_TOKEN = "cthQ7KASyXTqyL3AiAod"  # Token que já sabemos que funciona
CSV_FILE = "data/sample_thermal_data.csv"
MAX_RECORDS = 1000  # Carregar apenas os primeiros 1000 registros
BATCH_SIZE = 20  # Lotes menores

def load_sample_data():
    """Carregar amostra dos dados"""
    data = []
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader):
                if i >= MAX_RECORDS:
                    break
                    
                thermal_data = {
                    'temperatura': float(row['temperature']),
                    'umidade': float(row['humidity']),
                    'velocidade_vento': float(row['wind_velocity']),
                    'pressao': float(row['pressure']),
                    'radiacao_solar': float(row['solar_radiation']),
                    'sensacao_termica': float(row['thermal_sensation']),
                    'zona_conforto': row['comfort_zone'],
                    'timestamp': row['timestamp']
                }
                data.append(thermal_data)
        
        print(f"✅ Carregados {len(data)} registros (amostra)")
        return data
    
    except Exception as e:
        print(f"❌ Erro ao ler CSV: {e}")
        return []

def send_data_batch(batch_data, batch_num):
    """Enviar lote de dados"""
    telemetry_url = f"{THINGSBOARD_HOST}/api/v1/{ACCESS_TOKEN}/telemetry"
    success = 0
    
    for data in batch_data:
        try:
            response = requests.post(telemetry_url, json=data, timeout=3)
            if response.status_code == 200:
                success += 1
        except:
            pass  # Continuar mesmo com erros
    
    return success

def main():
    print("🌡️ CARREGANDO AMOSTRA DO DATASET (1000 registros)")
    print("=" * 50)
    
    # Carregar dados
    data = load_sample_data()
    if not data:
        return
    
    print(f"📊 Enviando {len(data)} registros em lotes de {BATCH_SIZE}...")
    
    total_success = 0
    total_batches = (len(data) + BATCH_SIZE - 1) // BATCH_SIZE
    
    for i in range(0, len(data), BATCH_SIZE):
        batch_num = (i // BATCH_SIZE) + 1
        batch = data[i:i + BATCH_SIZE]
        
        print(f"📤 Lote {batch_num}/{total_batches}...", end=" ")
        
        success = send_data_batch(batch, batch_num)
        total_success += success
        
        print(f"✅ {success}/{len(batch)}")
        
        # Progress
        progress = (i + len(batch)) / len(data) * 100
        print(f"   Progresso: {progress:.1f}%")
        
        time.sleep(0.05)  # Pequena pausa
    
    print(f"\n🎉 CONCLUÍDO!")
    print(f"✅ {total_success}/{len(data)} registros enviados")
    print(f"📊 Taxa de sucesso: {(total_success/len(data))*100:.1f}%")
    print(f"\n🔄 Atualize o ThingsBoard para ver os dados históricos!")

if __name__ == "__main__":
    main()