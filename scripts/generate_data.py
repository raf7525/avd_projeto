"""
Gerador de dados de sensação térmica
Converte dados de vento para dados térmicos com pressão e radiação solar
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math

def calculate_thermal_sensation(temp, humidity, wind_speed, pressure=None, solar_radiation=None):
    """
    Calcula sensação térmica usando fórmula aproximada do índice de calor
    """
    # Fórmula simplificada do Heat Index
    if temp < 27:  # Para temperaturas baixas, usar wind chill
        if wind_speed > 1.79:  # > 6.5 km/h
            wind_chill = 13.12 + 0.6215 * temp - 11.37 * (wind_speed * 3.6)**0.16 + 0.3965 * temp * (wind_speed * 3.6)**0.16
            return wind_chill
        return temp
    
    # Para temperaturas altas, usar heat index
    c1 = -8.78469475556
    c2 = 1.61139411
    c3 = 2.33854883889
    c4 = -0.14611605
    c5 = -0.012308094
    c6 = -0.0164248277778
    c7 = 0.002211732
    c8 = 0.00072546
    c9 = -0.000003582
    
    heat_index = (c1 + (c2 * temp) + (c3 * humidity) + 
                 (c4 * temp * humidity) + (c5 * temp**2) + 
                 (c6 * humidity**2) + (c7 * temp**2 * humidity) + 
                 (c8 * temp * humidity**2) + (c9 * temp**2 * humidity**2))
    
    # Ajustar por vento (vento reduz sensação de calor)
    if wind_speed > 0:
        wind_factor = 1 - (wind_speed * 0.05)  # Cada m/s reduz 5% a sensação
        wind_factor = max(wind_factor, 0.7)  # Mínimo 70%
        heat_index *= wind_factor
    
    # Ajustar por radiação solar (se disponível)
    if solar_radiation is not None and solar_radiation > 200:
        solar_factor = 1 + (solar_radiation - 200) / 2000  # Radiação alta aumenta sensação
        heat_index *= solar_factor
    
    return heat_index

def get_comfort_zone(thermal_sensation):
    """Classifica zona de conforto baseada na sensação térmica"""
    if thermal_sensation < 16:
        return "Frio"
    elif thermal_sensation < 20:
        return "Fresco" 
    elif thermal_sensation < 26:
        return "Confortável"
    elif thermal_sensation < 30:
        return "Quente"
    else:
        return "Muito Quente"

def generate_thermal_data(years_range=(2023, 2025)):
    """
    Gera dados sintéticos de sensação térmica para o período especificado
    Simula dados realistas baseados em padrões climáticos brasileiros
    """
    
    start_year, end_year = years_range
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year + 1, 1, 1)
    
    # Gerar timestamps de hora em hora
    timestamps = pd.date_range(start=start_date, end=end_date, freq='h')[:-1]
    
    data = []
    np.random.seed(42)  # Para reprodutibilidade
    
    for i, ts in enumerate(timestamps):
        # Padrões sazonais
        day_of_year = ts.timetuple().tm_yday
        season_factor = np.sin(2 * np.pi * day_of_year / 365)  # -1 (inverno) a 1 (verão)
        
        # Padrões diários
        hour_factor = np.sin(2 * np.pi * (ts.hour - 6) / 24)  # Pico às 14h
        
        # Temperatura base (Brasil: 15-35°C)
        base_temp = 25 + 8 * season_factor + 5 * hour_factor
        temp_noise = np.random.normal(0, 2)
        temperature = max(10, min(45, base_temp + temp_noise))
        
        # Umidade (inversamente relacionada com temperatura no verão)
        base_humidity = 70 - 15 * season_factor - 10 * hour_factor
        humidity_noise = np.random.normal(0, 10)
        humidity = max(20, min(95, base_humidity + humidity_noise))
        
        # Velocidade do vento (mantem do dataset original, mas em m/s)
        wind_base = 2 + np.random.exponential(3)  # 2-8 m/s típico
        wind_velocity = max(0, min(15, wind_base))
        
        # Pressão atmosférica (Brasil: 1000-1025 hPa)
        base_pressure = 1013 + 5 * np.sin(2 * np.pi * day_of_year / 365)  # Variação sazonal
        pressure_noise = np.random.normal(0, 3)
        pressure = max(990, min(1030, base_pressure + pressure_noise))
        
        # Radiação solar (W/m²) - depende da hora e estação
        if 6 <= ts.hour <= 18:  # Apenas durante o dia
            max_radiation = 1000  # Pico ao meio-dia
            hour_radiation_factor = np.sin(np.pi * (ts.hour - 6) / 12)
            season_radiation_factor = 0.7 + 0.3 * season_factor  # Mais forte no verão
            cloud_factor = np.random.uniform(0.3, 1.0)  # Simulação de nuvens
            
            solar_radiation = max_radiation * hour_radiation_factor * season_radiation_factor * cloud_factor
            solar_radiation = max(0, min(1200, solar_radiation + np.random.normal(0, 50)))
        else:
            solar_radiation = 0
        
        # Calcular sensação térmica
        thermal_sensation = calculate_thermal_sensation(
            temperature, humidity, wind_velocity, pressure, solar_radiation
        )
        
        # Classificar zona de conforto
        comfort_zone = get_comfort_zone(thermal_sensation)
        
        data.append({
            "timestamp": ts.isoformat(),
            "temperature": round(temperature, 2),
            "humidity": round(humidity, 1),
            "wind_velocity": round(wind_velocity, 2),
            "pressure": round(pressure, 2),
            "solar_radiation": round(solar_radiation, 1),
            "thermal_sensation": round(thermal_sensation, 2),
            "comfort_zone": comfort_zone
        })
        
        # Progress indicator
        if i % 10000 == 0:
            print(f"Processando: {ts.year}-{ts.month:02d} ({i}/{len(timestamps)})")
    
    return pd.DataFrame(data)

def main():
    print("🌡️ Gerando dados de sensação térmica (2023-2025)...")
    print("📊 Colunas: timestamp, temperature, humidity, wind_velocity, pressure, solar_radiation, thermal_sensation, comfort_zone")
    
    # Gerar dados
    df = generate_thermal_data(years_range=(2023, 2025))
    
    # Salvar arquivo
    output_file = "data/sample_thermal_data.csv"
    df.to_csv(output_file, index=False)
    
    # Estatísticas
    print(f"\n✅ Dados gerados com sucesso!")
    print(f"📁 Arquivo: {output_file}")
    print(f"📊 Total de registros: {len(df):,}")
    print(f"📅 Período: {df['timestamp'].min()} a {df['timestamp'].max()}")
    
    print(f"\n📈 Estatísticas:")
    print(f"  Temperatura: {df['temperature'].min():.1f}°C - {df['temperature'].max():.1f}°C (média: {df['temperature'].mean():.1f}°C)")
    print(f"  Umidade: {df['humidity'].min():.1f}% - {df['humidity'].max():.1f}% (média: {df['humidity'].mean():.1f}%)")
    print(f"  Vento: {df['wind_velocity'].min():.1f} - {df['wind_velocity'].max():.1f} m/s (média: {df['wind_velocity'].mean():.1f} m/s)")
    print(f"  Pressão: {df['pressure'].min():.1f} - {df['pressure'].max():.1f} hPa (média: {df['pressure'].mean():.1f} hPa)")
    print(f"  Radiação Solar: {df['solar_radiation'].min():.1f} - {df['solar_radiation'].max():.1f} W/m² (média: {df['solar_radiation'].mean():.1f} W/m²)")
    print(f"  Sensação Térmica: {df['thermal_sensation'].min():.1f}°C - {df['thermal_sensation'].max():.1f}°C (média: {df['thermal_sensation'].mean():.1f}°C)")
    
    print(f"\n🏠 Zonas de Conforto:")
    comfort_counts = df['comfort_zone'].value_counts()
    for zone, count in comfort_counts.items():
        percentage = (count / len(df)) * 100
        print(f"  {zone}: {count:,} ({percentage:.1f}%)")

if __name__ == "__main__":
    main()