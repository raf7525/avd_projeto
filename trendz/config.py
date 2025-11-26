"""
Configuração do Trendz Analytics para análise de dados de vento
"""

import os
from typing import Dict, List
import requests
from datetime import datetime, timedelta
import json

class TrendzConfig:
    """Classe para gerenciar configuração do Trendz Analytics"""
    
    def __init__(self):
        self.trendz_url = os.getenv('TRENDZ_URL', 'http://localhost:8888')
        self.thingsboard_url = os.getenv('THINGSBOARD_URL', 'http://localhost:8080')
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
                f"{self.trendz_url}/api/auth/login",
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
    
    def create_wind_datasource(self) -> Dict:
        """Criar fonte de dados para análise de vento"""
        if not self.api_token:
            self.get_auth_token()
        
        datasource_config = {
            "name": "Wind Data Source",
            "type": "THINGSBOARD",
            "configuration": {
                "url": self.thingsboard_url,
                "enableDeviceAttributes": True,
                "enableEntityAttributes": True,
                "telemetryKeys": [
                    "wind_velocity",
                    "wind_direction", 
                    "temperature",
                    "humidity"
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

class WindAnalyticsViews:
    """Configurar visualizações específicas para análise de vento"""
    
    @staticmethod
    def wind_rose_config() -> Dict:
        """Configuração para Rosa dos Ventos"""
        return {
            "name": "Wind Rose Analysis",
            "type": "POLAR_CHART",
            "settings": {
                "angleField": "wind_direction",
                "radiusField": "wind_velocity",
                "colorField": "cluster_id",
                "aggregation": "AVG",
                "timeInterval": "1h",
                "clustering": {
                    "enabled": True,
                    "algorithm": "KMEANS",
                    "clusters": 5
                }
            }
        }
    
    @staticmethod
    def wind_patterns_config() -> Dict:
        """Configuração para análise de padrões temporais"""
        return {
            "name": "Wind Patterns Timeline",
            "type": "TIME_SERIES",
            "settings": {
                "metrics": ["wind_velocity", "wind_direction"],
                "groupBy": ["hour", "day_of_week"],
                "aggregation": "AVG",
                "clustering": {
                    "enabled": True,
                    "features": ["wind_velocity", "wind_direction", "hour"],
                    "algorithm": "DBSCAN"
                }
            }
        }
    
    @staticmethod
    def wind_statistics_config() -> Dict:
        """Configuração para estatísticas de vento"""
        return {
            "name": "Wind Statistics Dashboard",
            "type": "KPI_DASHBOARD",
            "widgets": [
                {
                    "type": "GAUGE",
                    "metric": "wind_velocity",
                    "aggregation": "AVG",
                    "title": "Velocidade Média"
                },
                {
                    "type": "COMPASS",
                    "metric": "wind_direction",
                    "aggregation": "MODE",
                    "title": "Direção Predominante"
                },
                {
                    "type": "HISTOGRAM",
                    "metric": "wind_velocity",
                    "bins": 20,
                    "title": "Distribuição de Velocidades"
                }
            ]
        }

class TrendzIntegration:
    """Classe para integração completa com Trendz Analytics"""
    
    def __init__(self):
        self.config = TrendzConfig()
        self.views = WindAnalyticsViews()
    
    def setup_complete_analytics(self):
        """Configuração completa do ambiente de analytics"""
        print("🚀 Configurando Trendz Analytics para análise de vento...")
        
        # 1. Autenticar
        token = self.config.get_auth_token()
        if not token:
            print("❌ Falha na autenticação")
            return False
        
        print("✅ Autenticado com sucesso")
        
        # 2. Criar datasource
        datasource = self.config.create_wind_datasource()
        if datasource:
            print("✅ Datasource criado com sucesso")
        else:
            print("❌ Falha ao criar datasource")
            return False
        
        # 3. Configurar visualizações (seria feito via API se disponível)
        views_config = {
            "wind_rose": self.views.wind_rose_config(),
            "patterns": self.views.wind_patterns_config(),
            "statistics": self.views.wind_statistics_config()
        }
        
        print("✅ Configurações de visualização preparadas:")
        for name, config in views_config.items():
            print(f"  - {config['name']}")
        
        return True
    
    def export_sample_data(self, num_records: int = 1000):
        """Gerar dados de exemplo para teste"""
        import numpy as np
        import pandas as pd
        
        np.random.seed(42)
        
        # Gerar dados sintéticos de vento
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
            
            velocity = 5 + 3 * day_factor + np.random.normal(0, 2)
            velocity = max(0, velocity)  # Velocidade não pode ser negativa
            
            direction = (180 + 60 * day_factor + np.random.normal(0, 30)) % 360
            
            data.append({
                "timestamp": ts.isoformat(),
                "wind_velocity": round(velocity, 2),
                "wind_direction": round(direction, 2),
                "temperature": round(20 + 5 * day_factor + np.random.normal(0, 3), 1),
                "humidity": round(50 + 20 * np.sin(2 * np.pi * ts.day / 30) + np.random.normal(0, 10), 1)
            })
        
        # Salvar arquivo para importação
        df = pd.DataFrame(data)
        output_path = '/home/raf75/quinto-periodo/avd/avd_projeto/data/sample_wind_data.csv'
        df.to_csv(output_path, index=False)
        
        print(f"✅ {len(data)} registros de dados de exemplo gerados")
        print(f"📁 Arquivo salvo: {output_path}")
        
        return df

if __name__ == "__main__":
    integration = TrendzIntegration()
    
    # Configurar analytics
    success = integration.setup_complete_analytics()
    
    if success:
        # Gerar dados de exemplo
        integration.export_sample_data()
        print("\n🎉 Configuração do Trendz Analytics concluída!")
        print("\nPróximos passos:")
        print("1. Acesse http://localhost:8888 para Trendz Analytics")
        print("2. Importe os dados de exemplo")
        print("3. Configure os dashboards de análise de vento")
    else:
        print("\n❌ Falha na configuração. Verifique se os serviços estão rodando.")