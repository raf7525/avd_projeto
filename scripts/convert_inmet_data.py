import pandas as pd
import numpy as np
import os
import sys

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

def convert_inmet_to_system_format(input_path, output_path):
    print(f"🔄 Convertendo '{input_path}' para formato do sistema...")
    
    try:
        # 1. Ler CSV do INMET
        # - skiprows=8: Pula metadados
        # - delimiter=';': Separador do INMET
        # - decimal=',': Decimal brasileiro
        # - encoding='latin1' ou 'utf-8': INMET costuma usar latin1 (ISO-8859-1)
        df = pd.read_csv(input_path, skiprows=8, delimiter=';', decimal=',', encoding='latin1')
        
        # 2. Selecionar e Renomear Colunas
        # Mapeamento: Nome no CSV INMET -> Nome no Sistema
        column_mapping = {
            'Data': 'date',
            'Hora UTC': 'time',
            'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)': 'temperature',
            'UMIDADE RELATIVA DO AR, HORARIA (%)': 'humidity',
            'VENTO, VELOCIDADE HORARIA (m/s)': 'wind_velocity',
            'PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)': 'pressure',
            'RADIACAO GLOBAL (Kj/m²)': 'solar_radiation'
        }
        
        # Tentar encontrar as colunas (os nomes as vezes variam ligeiramente no INMET)
        # Vamos normalizar os nomes das colunas do DF para facilitar
        df.columns = [c.strip() for c in df.columns]
        
        # Ajuste fino nos nomes se necessário (INMET as vezes muda acentos)
        # Procurar coluna que contem "TEMPERATURA DO AR"
        for col in df.columns:
            if "TEMPERATURA DO AR" in col and "BULBO SECO" in col:
                column_mapping[col] = 'temperature'
            elif "UMIDADE RELATIVA" in col:
                column_mapping[col] = 'humidity'
            elif "VENTO" in col and "VELOCIDADE" in col:
                column_mapping[col] = 'wind_velocity'
            elif "PRESSAO ATMOSFERICA" in col and "ESTACAO" in col:
                column_mapping[col] = 'pressure'
            elif "RADIACAO GLOBAL" in col:
                column_mapping[col] = 'solar_radiation'

        # Filtrar apenas colunas mapeadas
        mapped_cols = {k: v for k, v in column_mapping.items() if k in df.columns}
        df = df[list(mapped_cols.keys())].rename(columns=mapped_cols)
        
        # 3. Tratamento de Dados
        
        # Converter Data e Hora para Timestamp
        # Hora UTC vem como "0000 UTC", precisamos remover " UTC" e formatar
        df['time'] = df['time'].astype(str).str.replace(' UTC', '').str.zfill(4)
        df['time'] = df['time'].str[:2] + ':' + df['time'].str[2:]
        
        df['timestamp'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%Y/%m/%d %H:%M')
        
        # Converter Radiação: INMET usa Kj/m², sistema usa W/m² (aprox) ou manter escala
        # Mas cuidado: INMET poe nulos como vazio ou -9999
        numeric_cols = ['temperature', 'humidity', 'wind_velocity', 'pressure', 'solar_radiation']
        
        for col in numeric_cols:
            if col in df.columns:
                # Forçar numérico, transformar erros em NaN
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # Preencher NaN com interpolação linear (bom para séries temporais)
                df[col] = df[col].interpolate(method='linear', limit_direction='both')
        
        # Radiação no INMET as vezes vem vazia à noite, preencher com 0
        df['solar_radiation'] = df['solar_radiation'].fillna(0)
        # Converter Kj/m² (acumulado hora) para W/m² (intensidade média)
        # 1 Kj/m² = 1000 J/m². Dividido por 3600s = ~0.277 W/m²
        df['solar_radiation'] = df['solar_radiation'] * 1000 / 3600
        
        # 4. Calcular Colunas Derivadas (Sensação e Conforto)
        print("🧮 Calculando sensação térmica e zonas de conforto...")
        
        sensations = []
        zones = []
        
        for _, row in df.iterrows():
            sensation = calculate_thermal_sensation(
                row['temperature'],
                row['humidity'],
                row['wind_velocity'],
                row['pressure'],
                row['solar_radiation']
            )
            sensations.append(round(sensation, 2))
            zones.append(get_comfort_zone(sensation))
            
        df['thermal_sensation'] = sensations
        df['comfort_zone'] = zones
        
        # 5. Selecionar Colunas Finais
        final_cols = ['timestamp', 'temperature', 'humidity', 'wind_velocity', 
                      'pressure', 'solar_radiation', 'thermal_sensation', 'comfort_zone']
        
        df_final = df[final_cols]
        
        # 6. Salvar
        df_final.to_csv(output_path, index=False)
        
        print("\n✅ Conversão Concluída com Sucesso!")
        print(f"📄 Origem: {input_path}")
        print(f"💾 Destino: {output_path}")
        print(f"📊 Registros processados: {len(df_final)}")
        print(f"📅 Período: {df_final['timestamp'].min()} até {df_final['timestamp'].max()}")
        print("\nAgora você pode rodar: python scripts/ingest_data.py")
        
    except Exception as e:
        print(f"\n❌ Erro na conversão: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    INMET_FILE = "data/inmet.csv"
    OUTPUT_FILE = "data/sample_thermal_data.csv"
    
    if not os.path.exists(INMET_FILE):
        print(f"Arquivo {INMET_FILE} não encontrado na raiz.")
    else:
        convert_inmet_to_system_format(INMET_FILE, OUTPUT_FILE)
