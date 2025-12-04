
import os
import requests
import json
import time
from trendz.config import TrendzConfig

def create_view(config: TrendzConfig, view_config: dict):
    """
    Cria uma nova visualização (gráfico) no Trendz.
    """
    if not config.api_token:
        print("Erro: Token de API não encontrado. Autentique primeiro.")
        return None

    try:
        response = requests.post(
            f"{config.trendz_url}/api/views",
            headers={
                "Authorization": f"Bearer {config.api_token}",
                "Content-Type": "application/json"
            },
            json=view_config
        )

        if response.status_code == 200 or response.status_code == 201:
            print(f"✅ Visualização '{view_config.get('name')}' criada com sucesso!")
            return response.json()
        else:
            print(f"❌ Erro ao criar visualização. Status: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão ao tentar criar a visualização: {e}")
        return None

def main():
    """
    Script principal para criar um novo gráfico no Trendz.
    """
    print("🚀 Iniciando a criação de um novo gráfico no Trendz...")

    trendz_config = TrendzConfig()
    
    # 1. Configurar e autenticar com retentativas
    max_retries = 10
    retry_delay = 10
    auth_success = False
    for attempt in range(max_retries):
        print(f"🔑 Tentativa de autenticação {attempt + 1}/{max_retries}...")
        if trendz_config.get_auth_token():
            auth_success = True
            print("✅ Autenticação bem-sucedida.")
            break
        print(f"⏳ Falha na autenticação. Tentando novamente em {retry_delay} segundos...")
        time.sleep(retry_delay)

    if not auth_success:
        print("❌ Falha na autenticação após múltiplas tentativas. Abortando.")
        return

    # 2. Definir a configuração do novo gráfico
    # Gráfico de linha: Média de Temperatura por Hora
    new_chart_config = {
      "name": "Média de Temperatura por Hora",
      "type": "LINE_CHART",
      "settings": {
        "datasource": "Thermal Comfort Data Source", # Nome definido em trendz/config.py
        "xField": "hour_of_day",
        "yField": "temperature",
        "aggregation": "AVG",
        "timeInterval": "1h",
        "color": "#FF5733"
      }
    }
    
    print(f"📊 Configuração do gráfico '{new_chart_config['name']}' definida.")

    # 3. Criar a visualização (gráfico)
    create_view(trendz_config, new_chart_config)

if __name__ == "__main__":
    main()
