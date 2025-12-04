"""
Configuração do Trendz Analytics para análise de dados de sensação térmica
"""

import os
from typing import Dict, List
import requests
from datetime import datetime, timedelta
import json

class TrendzConfig:
    """Classe para gerenciar configuração do Trendz Analytics"""
    
    def __init__(self):
        self.trendz_url = os.getenv('TRENDZ_URL', 'http://trendz:8888')
        self.thingsboard_url = os.getenv('THINGSBOARD_URL', 'http://thingsboard:9090')
        self.username = os.getenv('TRENDZ_USERNAME', 'tenant@thingsboard.org')
        self.password = os.getenv('TRENDZ_PASSWORD', 'tenant')
        self.api_token = None
    
    def get_auth_token(self) -> str:
        """Obter token de autenticação do Trendz"""
        try:
            auth_data = {
                "username": self.username,
                "password": self.password
            }
            
            response = requests.post(
                f"{self.thingsboard_url}/api/auth/login",
                json=auth_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                self.api_token = response.json().get('token')
                return self.api_token
            else:
                raise Exception(f"Falha na autenticação: {response.status_code}")
                
        except Exception as e:
            print(f"Erro ao obter token: {e}")
            return None
    
    def create_thermal_datasource(self) -> Dict:
        """Criar fonte de dados para análise de sensação térmica"""
        if not self.api_token:
            self.get_auth_token()
        
        datasource_config = {
            "name": "Thermal Comfort Data Source",
            "type": "THINGSBOARD",
            "configuration": {
                "url": self.thingsboard_url,
                "enableDeviceAttributes": True,
                "enableEntityAttributes": True,
                "telemetryKeys": [
                    "temperature",
                    "humidity", 
                    "wind_velocity",
                    "pressure",
                    "solar_radiation",
                    "thermal_sensation",
                    "comfort_zone"
                ],
                "attributeKeys": [
                    "location",
                    "sensor_type",
                    "installation_date"
                ]
            }
        }
        
        try:
            response = requests.post(
                f"{self.trendz_url}/api/datasources",
                json=datasource_config,
                headers={
                    "Authorization": f"Bearer {self.api_token}",
                    "Content-Type": "application/json"
                }
            )
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                raise Exception(f"Erro ao criar datasource: {response.status_code}")
                
        except Exception as e:
            print(f"Erro ao criar datasource: {e}")
            return None

class ThermalAnalyticsViews:
    """Configurar visualizações específicas para análise de sensação térmica"""
    
    @staticmethod
    def thermal_heatmap_config() -> Dict:
        """Configuração para Mapa de Calor de Sensação Térmica"""
        return {
            "name": "Thermal Sensation Heatmap",
            "type": "HEATMAP",
            "settings": {
                "xField": "hour_of_day",
                "yField": "day_of_week",
                "valueField": "thermal_sensation",
                "colorField": "comfort_zone",
                "aggregation": "AVG",
                "timeInterval": "1h",
                "comfort_zones": {
                    "enabled": True,
                    "zones": 5,
                    "clusters": 5
                }
            }
        }
    
    @staticmethod
    def comfort_zones_config() -> Dict:
        """Configuração para análise de zonas de conforto térmico"""
        return {
            "name": "Thermal Comfort Zones Analysis",
            "type": "SCATTER_CHART",
            "settings": {
                "xField": "temperature",
                "yField": "humidity",
                "colorField": "comfort_zone",
                "sizeField": "thermal_sensation",
                "aggregation": "AVG",
                "zones": {
                    "muito_frio": {"range": [0, 16], "color": "#0066cc"},
                    "frio": {"range": [16, 21], "color": "#66ccff"},
                    "confortavel": {"range": [21, 26], "color": "#00cc66"},
                    "quente": {"range": [26, 32], "color": "#ffcc00"},
                    "muito_quente": {"range": [32, 50], "color": "#ff6600"}
                }
            }
        }
    
    @staticmethod  
    def thermal_statistics_config() -> Dict:
        """Configuração para estatísticas de sensação térmica"""
        return {
            "name": "Thermal Comfort Statistics Dashboard",
            "type": "KPI_DASHBOARD",
            "widgets": [
                {
                    "type": "GAUGE",
                    "metric": "thermal_sensation",
                    "aggregation": "AVG",
                    "title": "Sensação Térmica Média"
                },
                {
                    "type": "PIE_CHART",
                    "metric": "comfort_zone",
                    "aggregation": "COUNT",
                    "title": "Distribuição Zonas de Conforto"
                },
                {
                    "type": "HISTOGRAM",
                    "metric": "thermal_sensation",
                    "bins": 20,
                    "title": "Distribuição de Sensação Térmica"
                }
            ]
        }

class TrendzIntegration:
    """Classe para integração completa com Trendz Analytics"""
    
    def __init__(self):
        self.config = TrendzConfig()
        self.views = ThermalAnalyticsViews()
    
    def setup_complete_analytics(self):
        """Configuração completa do ambiente de analytics térmicos"""
        print("🚀 Configurando Trendz Analytics para análise de sensação térmica...")
        
        # 1. Autenticar
        token = self.config.get_auth_token()
        if not token:
            print("❌ Falha na autenticação")
            return False
        
        print("✅ Autenticado com sucesso")
        
        # 2. Criar datasource
        datasource = self.config.create_thermal_datasource()
        if datasource:
            print("✅ Datasource criado com sucesso")
        else:
            print("❌ Falha ao criar datasource")
            return False
        
        # 3. Configurar visualizações (seria feito via API se disponível)
        views_config = {
            "thermal_heatmap": self.views.thermal_heatmap_config(),
            "comfort_zones": self.views.comfort_zones_config(),
            "thermal_statistics": self.views.thermal_statistics_config()
        }
        
        print("✅ Configurações de visualização preparadas:")
        for name, config in views_config.items():
            print(f"  - {config['name']}")
        
        return True
    
    def export_sample_data(self):
        """Gerar dados de exemplo térmicos para teste"""
        import numpy as np
        import pandas as pd
        import os
        
        np.random.seed(42)
        
        # Gerar dados sintéticos térmicos
        timestamps = pd.date_range(
            start=datetime.now() - timedelta(days=30),
            end=datetime.now(),
            freq='h'
        )
        
        data = []
        for ts in timestamps:
            # Padrões sazonais simulados
            hour = ts.hour
            day_factor = np.sin(2 * np.pi * hour / 24)
            
            # Dados térmicos realistas
            temperature = 22 + 8 * day_factor + np.random.normal(0, 3)
            temperature = max(10, min(45, temperature))  # Range realista
            
            humidity = 60 + 20 * np.sin(2 * np.pi * ts.day / 30) + np.random.normal(0, 10)
            humidity = max(20, min(95, humidity))
            
            wind_velocity = 2 + 3 * abs(day_factor) + np.random.normal(0, 1)
            wind_velocity = max(0, min(15, wind_velocity))
            
            pressure = 1013 + 10 * np.sin(2 * np.pi * ts.day / 365) + np.random.normal(0, 5)
            solar_radiation = max(0, 800 * max(0, np.sin(np.pi * hour / 12)) + np.random.normal(0, 100))
            
            # Calcular sensação térmica (simplificado)
            thermal_sensation = temperature + 0.1 * humidity - 0.5 * wind_velocity
            
            data.append({
                "timestamp": ts.isoformat(),
                "temperature": round(temperature, 1),
                "humidity": round(humidity, 1),
                "wind_velocity": round(wind_velocity, 2),
                "pressure": round(pressure, 1),
                "solar_radiation": round(solar_radiation, 1),
                "thermal_sensation": round(thermal_sensation, 1),
                "comfort_zone": "Confortável" if 21 <= thermal_sensation <= 26 else "Outro"
            })
        
        # Salvar arquivo para importação
        df = pd.DataFrame(data)
        output_path = '/app/data/sample_trendz_data.csv'
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        df.to_csv(output_path, index=False)
        
        print(f"✅ {len(data)} registros de dados térmicos de exemplo gerados")
        print(f"📁 Arquivo salvo: {output_path}")
        
        return df

if __name__ == "__main__":
    integration = TrendzIntegration()
    
    # Configurar analytics
    success = integration.setup_complete_analytics()
    
    if success:
        # Gerar dados de exemplo
        integration.export_sample_data()
        print("\n🎉 Configuração do Trendz Analytics para análise térmica concluída!")
        print("\nPróximos passos:")
        print("1. Acesse http://localhost:8888 para Trendz Analytics")
        print("2. Importe os dados térmicos de exemplo")
        print("3. Configure os dashboards de sensação térmica")
    else:
        print("\n❌ Falha na configuração. Verifique se os serviços estão rodando.")