#!/usr/bin/env python3
"""
Script para simular dados térmicos em tempo real no ThingsBoard
"""
import requests
import json
import time
import random
from datetime import datetime

# Token do dispositivo (obtido do script anterior)
DEVICE_ACCESS_TOKEN = "cthQ7KASyXYfyUHJ6g8Z"  # Substitua pelo seu token
THINGSBOARD_HOST = "http://localhost:8080"

def generate_realistic_thermal_data():
    """Gerar dados térmicos realistas baseados na hora do dia"""
    current_time = datetime.now()
    hour = current_time.hour
    
    # Simular variação de temperatura por hora
    base_temps = {
        0: 18, 1: 17, 2: 16, 3: 15, 4: 15, 5: 16,
        6: 18, 7: 20, 8: 22, 9: 25, 10: 27, 11: 29,
        12: 31, 13: 32, 14: 33, 15: 32, 16: 30, 17: 28,
        18: 26, 19: 24, 20: 22, 21: 21, 22: 20, 23: 19
    }
    
    # Temperatura base + variação aleatória
    temperature = base_temps.get(hour, 22) + random.uniform(-2, 3)
    
    # Umidade inversamente relacionada à temperatura
    humidity = max(30, min(90, 80 - (temperature - 20) * 2 + random.uniform(-10, 10)))
    
    # Vento com variação
    wind_velocity = random.uniform(5, 20)
    
    # Pressão atmosférica
    pressure = random.uniform(1010, 1025)
    
    # Radiação solar baseada na hora
    if 6 <= hour <= 18:
        solar_radiation = max(0, 900 * (1 - abs(hour - 12) / 6) + random.uniform(-100, 100))
    else:
        solar_radiation = 0
    
    # Calcular sensação térmica simplificada
    # Heat Index para temperaturas altas
    if temperature > 27 and humidity > 40:
        hi = -42.379 + 2.04901523 * temperature + 10.14333127 * humidity
        hi += -0.22475541 * temperature * humidity
        thermal_sensation = hi
    # Wind Chill para temperaturas baixas
    elif temperature < 10 and wind_velocity > 5:
        wc = 13.12 + 0.6215 * temperature - 11.37 * (wind_velocity ** 0.16)
        wc += 0.3965 * temperature * (wind_velocity ** 0.16)
        thermal_sensation = wc
    else:
        thermal_sensation = temperature + random.uniform(-2, 2)
    
    # Classificar zona de conforto
    if thermal_sensation < 16:
        comfort_zone = "Muito Frio"
    elif thermal_sensation < 20:
        comfort_zone = "Frio"
    elif thermal_sensation <= 26:
        comfort_zone = "Confortável"
    elif thermal_sensation <= 32:
        comfort_zone = "Quente"
    else:
        comfort_zone = "Muito Quente"
    
    return {
        "temperatura": round(temperature, 1),
        "umidade": round(humidity, 1),
        "velocidade_vento": round(wind_velocity, 1),
        "pressao": round(pressure, 1),
        "radiacao_solar": round(solar_radiation, 0),
        "sensacao_termica": round(thermal_sensation, 1),
        "zona_conforto": comfort_zone,
        "timestamp": current_time.isoformat(),
        "hora": hour
    }

def send_data_to_thingsboard(data):
    """Enviar dados para ThingsBoard"""
    telemetry_url = f"{THINGSBOARD_HOST}/api/v1/{DEVICE_ACCESS_TOKEN}/telemetry"
    
    try:
        response = requests.post(telemetry_url, json=data, timeout=5)
        if response.status_code == 200:
            return True
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    print("🌡️ Simulador de Dados Térmicos em Tempo Real")
    print("=" * 50)
    print("Pressione Ctrl+C para parar")
    print()
    
    interval = 5  # Enviar dados a cada 5 segundos
    count = 0
    
    try:
        while True:
            # Gerar dados
            thermal_data = generate_realistic_thermal_data()
            
            # Enviar para ThingsBoard
            if send_data_to_thingsboard(thermal_data):
                count += 1
                print(f"✅ [{count:3d}] {thermal_data['timestamp'][:19]} | "
                      f"Temp: {thermal_data['temperatura']:5.1f}°C | "
                      f"Sensação: {thermal_data['sensacao_termica']:5.1f}°C | "
                      f"Zona: {thermal_data['zona_conforto']}")
            else:
                print(f"❌ Falha no envio")
            
            # Aguardar próximo envio
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print(f"\n\n✅ Simulação finalizada. {count} registros enviados.")
        print("🌐 Acesse o ThingsBoard para ver os dados em tempo real!")

if __name__ == "__main__":
    main()