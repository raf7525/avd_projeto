#!/usr/bin/env python3
"""
Script para carregar MAIS dados térmicos (próximos 5000 registros)
"""
import csv
import requests
import time
from datetime import datetime

# Configurações
THINGSBOARD_HOST = "http://localhost:8080"
ACCESS_TOKEN = "cthQ7KASyXTqyL3AiAod"
CSV_FILE = "data/sample_thermal_data.csv"
SKIP_RECORDS = 1000  # Pular os primeiros 1000 (já enviados)
MAX_RECORDS = 5000   # Carregar próximos 5000
BATCH_SIZE = 50      # Lotes maiores agora

def load_more_data():
    """Carregar mais dados do CSV"""
    data = []
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # Pular registros já enviados
            for i in range(SKIP_RECORDS):
                next(reader, None)
            
            # Carregar próximos registros
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
                    'zona_conforto': row['comfort_zone']
                }
                data.append(thermal_data)
        
        print(f"✅ Carregados {len(data)} novos registros")
        return data
    
    except Exception as e:
        print(f"❌ Erro ao ler CSV: {e}")
        return []

def send_batch(batch_data):
    """Enviar lote de dados"""
    telemetry_url = f"{THINGSBOARD_HOST}/api/v1/{ACCESS_TOKEN}/telemetry"
    success = 0
    
    for data in batch_data:
        try:
            response = requests.post(telemetry_url, json=data, timeout=2)
            if response.status_code == 200:
                success += 1
        except:
            pass
    
    return success

def main():
    print("🌡️ CARREGANDO MAIS 5000 REGISTROS DO DATASET")
    print("=" * 45)
    
    # Carregar dados
    data = load_more_data()
    if not data:
        return
    
    print(f"📊 Enviando {len(data)} registros em lotes de {BATCH_SIZE}...")
    
    total_success = 0
    total_batches = (len(data) + BATCH_SIZE - 1) // BATCH_SIZE
    start_time = time.time()
    
    for i in range(0, len(data), BATCH_SIZE):
        batch_num = (i // BATCH_SIZE) + 1
        batch = data[i:i + BATCH_SIZE]
        
        success = send_batch(batch)
        total_success += success
        
        # Progress a cada 10 lotes
        if batch_num % 10 == 0 or batch_num == total_batches:
            elapsed = time.time() - start_time
            progress = (i + len(batch)) / len(data) * 100
            rate = total_success / elapsed if elapsed > 0 else 0
            
            print(f"📤 Lote {batch_num}/{total_batches} | "
                  f"Progresso: {progress:.1f}% | "
                  f"Taxa: {rate:.1f} reg/s | "
                  f"Total enviado: {total_success}")
    
    print(f"\n🎉 SEGUNDA LEVA CONCLUÍDA!")
    print(f"✅ {total_success}/{len(data)} registros enviados")
    print(f"📊 Total acumulado: ~{total_success + 1000} registros no ThingsBoard")
    print(f"\n🌐 Agora você tem dados históricos robustos para análise!")

if __name__ == "__main__":
    main()