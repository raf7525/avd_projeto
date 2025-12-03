"""
Dashboard Trendz Analytics para Sistema de Predição de Sensação Térmica
"""

import pandas as pd
import json
from typing import Dict
import requests

class ThermalDataProcessor:
    """Processador de dados de sensação térmica para Trendz Analytics"""
    
    def __init__(self, data_source: str = "/home/raf75/quinto-periodo/avd/avd_projeto/data/sample_thermal_data.csv"):
        self.data_source = data_source
        self.df = None
        self.comfort_zones = None
    
    def load_data(self) -> pd.DataFrame:
        """Carregar dados de sensação térmica"""
        try:
            self.df = pd.read_csv(self.data_source)
            self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
            self.df['hour'] = self.df['timestamp'].dt.hour
            self.df['day_of_week'] = self.df['timestamp'].dt.dayofweek
            self.df['month'] = self.df['timestamp'].dt.month
            
            print(f"✅ {len(self.df)} registros térmicos carregados")
            return self.df
            
        except Exception as e:
            print(f"❌ Erro ao carregar dados térmicos: {e}")
            return None
    
    def classify_comfort_zones(self, n_zones: int = 5) -> pd.DataFrame:
        """Classificar zonas de conforto térmico"""
        
        if self.df is None:
            self.load_data()
        
        # Classificar zonas de conforto baseado na sensação térmica
        def get_comfort_zone(thermal_sensation):
            if thermal_sensation < 16:
                return "Muito Frio"
            elif thermal_sensation < 21:
                return "Frio"  
            elif thermal_sensation < 26:
                return "Confortável"
            elif thermal_sensation < 32:
                return "Quente"
            else:
                return "Muito Quente"
        
        self.df['comfort_zone_calculated'] = self.df['thermal_sensation'].apply(get_comfort_zone)
        
        # Estatísticas por zona de conforto
        comfort_stats = {}
        for zone in self.df['comfort_zone_calculated'].unique():
            zone_data = self.df[self.df['comfort_zone_calculated'] == zone]
            comfort_stats[zone] = {
                "count": len(zone_data),
                "avg_thermal_sensation": zone_data['thermal_sensation'].mean(),
                "avg_temperature": zone_data['temperature'].mean(),
                "avg_humidity": zone_data['humidity'].mean()
            }
        
        self.comfort_zones = comfort_stats
        print("✅ Classificação de zonas de conforto realizada")
        return self.df
    
    def get_comfort_statistics(self) -> Dict:
        """Obter estatísticas por zona de conforto"""
        if 'comfort_zone_calculated' not in self.df.columns:
            self.classify_comfort_zones()
        
        stats = {}
        for zone in sorted(self.df['comfort_zone_calculated'].unique()):
            zone_data = self.df[self.df['comfort_zone_calculated'] == zone]
            
            stats[f"Zona {zone}"] = {
                "count": len(zone_data),
                "thermal_sensation": {
                    "mean": zone_data['thermal_sensation'].mean(),
                    "std": zone_data['thermal_sensation'].std(),
                    "min": zone_data['thermal_sensation'].min(),
                    "max": zone_data['thermal_sensation'].max()
                },
                "environmental": {
                    "avg_temperature": zone_data['temperature'].mean(),
                    "avg_humidity": zone_data['humidity'].mean(),
                    "avg_wind": zone_data['wind_velocity'].mean(),
                    "avg_pressure": zone_data['pressure'].mean() if 'pressure' in zone_data.columns else None
                },
                "temporal_patterns": {
                    "most_common_hour": zone_data['hour'].mode().iloc[0] if len(zone_data['hour'].mode()) > 0 else None,
                    "most_common_day": zone_data['day_of_week'].mode().iloc[0] if len(zone_data['day_of_week'].mode()) > 0 else None
                }
            }
        
        return stats

class TrendzDashboardCreator:
    """Criador de dashboards para Trendz Analytics - Sensação Térmica"""
    
    def __init__(self, processor: ThermalDataProcessor):
        self.processor = processor
        self.trendz_url = "http://localhost:8888"
    
    def create_thermal_heatmap_visualization(self) -> Dict:
        """Criar visualização de Mapa de Calor de Sensação Térmica"""
        if self.processor.df is None:
            self.processor.load_data()
        
        if 'comfort_zone_calculated' not in self.processor.df.columns:
            self.processor.classify_comfort_zones()
        
        # Configuração do Mapa de Calor Térmico para Trendz
        thermal_heatmap_config = {
            "name": "Mapa de Calor - Sensação Térmica",
            "type": "heatmap",
            "data_source": "thermal_data",
            "configuration": {
                "x_field": "hour",
                "y_field": "day_of_week", 
                "value_field": "thermal_sensation",
                "color_field": "comfort_zone_calculated",
                "aggregation": "mean",
                "color_scheme": "RdYlBu_r"
            },
            "filters": {
                "time_range": "last_30_days",
                "comfort_zone": "all",
                "min_thermal_sensation": -10,
                "max_thermal_sensation": 50
            }
        }
        
        return thermal_heatmap_config
    
    def create_comfort_zones_dashboard(self) -> Dict:
        """Criar dashboard de zonas de conforto térmico"""
        comfort_dashboard = {
            "name": "Análise de Zonas de Conforto Térmico",
            "widgets": [
                {
                    "type": "scatter",
                    "title": "Temperatura vs Umidade por Zona",
                    "x_axis": "temperature",
                    "y_axis": "humidity",
                    "color": "comfort_zone_calculated",
                    "aggregation": "mean"
                },
                {
                    "type": "line_chart",
                    "title": "Tendência Diária",
                    "x_axis": "hour", 
                    "y_axis": "thermal_velocity",
                    "group_by": "cluster",
                    "aggregation": "mean"
                },
                {
                    "type": "bar_chart",
                    "title": "Distribuição por Cluster",
                    "x_axis": "cluster",
                    "y_axis": "count",
                    "color_by": "cluster"
                },
                {
                    "type": "scatter_plot",
                    "title": "Velocidade vs Direção",
                    "x_axis": "thermal_direction",
                    "y_axis": "thermal_velocity", 
                    "color_by": "cluster",
                    "size_by": "hour"
                }
            ]
        }
        
        return temporal_dashboard
    
    def create_statistics_panel(self) -> Dict:
        """Criar painel de estatísticas"""
        stats_panel = {
            "name": "Estatísticas de Vento",
            "layout": "grid",
            "widgets": [
                {
                    "type": "kpi",
                    "title": "Velocidade Média",
                    "metric": "thermal_velocity",
                    "aggregation": "mean",
                    "unit": "m/s",
                    "size": "medium"
                },
                {
                    "type": "kpi", 
                    "title": "Velocidade Máxima",
                    "metric": "thermal_velocity",
                    "aggregation": "max",
                    "unit": "m/s",
                    "size": "medium"
                },
                {
                    "type": "gauge",
                    "title": "Direção Predominante",
                    "metric": "thermal_direction",
                    "aggregation": "mode",
                    "min": 0,
                    "max": 360,
                    "unit": "graus"
                },
                {
                    "type": "histogram",
                    "title": "Distribuição de Velocidades",
                    "metric": "thermal_velocity",
                    "bins": 20,
                    "color_by": "cluster"
                }
            ]
        }
        
        return stats_panel
    
    def export_dashboard_config(self, output_file: str = "/home/raf75/quinto-periodo/avd/avd_projeto/data/trendz_dashboard_config.json"):
        """Exportar configuração completa dos dashboards"""
        config = {
            "project_name": "Sistema de Predição de Sensação Térmica",
            "dashboards": {
                "thermal_heatmap": self.create_thermal_heatmap_visualization(),
                "comfort_zones": self.create_comfort_zones_dashboard(),
                "statistics": self.create_statistics_panel()
            },
            "data_sources": {
                "primary": {
                    "type": "csv",
                    "path": "/home/raf75/quinto-periodo/avd/avd_projeto/data/sample_thermal_data.csv",
                    "fields": {
                        "timestamp": "datetime",
                        "temperature": "float", 
                        "humidity": "float",
                        "wind_velocity": "float",
                        "pressure": "float",
                        "solar_radiation": "float",
                        "thermal_sensation": "float",
                        "comfort_zone": "string",
                        "comfort_zone_calculated": "string"
                    }
                }
            },
            "filters": {
                "global": {
                    "time_range": ["last_30_days", "last_7_days", "last_24_hours"],
                    "velocity_range": [0, 30],
                    "direction_range": [0, 360]
                }
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(config, f, indent=2, default=str)
        
        print(f"✅ Configuração exportada para: {output_file}")
        return config

class TrendzAPIConnector:
    """Conector para API do Trendz Analytics"""
    
    def __init__(self, base_url: str = "http://localhost:8888"):
        self.base_url = base_url
        self.token = None
    
    def authenticate(self, username: str = "tenant@thingsboard.org", password: str = "tenant"):
        """Autenticar na API do Trendz"""
        auth_data = {
            "username": username,
            "password": password
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json=auth_data
            )
            
            if response.status_code == 200:
                self.token = response.json().get('token')
                print("✅ Autenticado no Trendz Analytics")
                return True
            else:
                print(f"❌ Falha na autenticação: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro de conexão: {e}")
            return False
    
    def upload_data(self, data: pd.DataFrame) -> bool:
        """Upload de dados para Trendz"""
        if not self.token:
            print("❌ Não autenticado")
            return False
        
        # Converter DataFrame para formato aceito pelo Trendz
        data_json = data.to_dict('records')
        
        try:
            response = requests.post(
                f"{self.base_url}/api/data/upload",
                json=data_json,
                headers={"Authorization": f"Bearer {self.token}"}
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ {len(data_json)} registros enviados")
                return True
            else:
                print(f"❌ Erro no upload: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro no upload: {e}")
            return False

def main():
    """Função principal para configuração completa"""
    print("🌡️ Configurando Dashboard Trendz para Análise de Sensação Térmica")
    print("=" * 60)
    
    # 1. Processar dados
    processor = ThermalDataProcessor()
    processor.load_data()
    processor.classify_comfort_zones()
    
    # 2. Exibir estatísticas
    stats = processor.get_comfort_statistics()
    print("\n📊 Estatísticas por Zona de Conforto:")
    for zone, data in stats.items():
        print(f"\n{zone}:")
        print(f"  - Registros: {data['count']}")
        print(f"  - Sensação térmica média: {data['thermal_sensation']['mean']:.1f}°C")
        print(f"  - Temperatura média: {data['environmental']['avg_temperature']:.1f}°C")
        print(f"  - Hora predominante: {data['temporal_patterns']['most_common_hour']}h")
    
    # 3. Criar dashboards
    dashboard_creator = TrendzDashboardCreator(processor)
    dashboard_creator.export_dashboard_config()
    
    # 4. Conectar com Trendz (se disponível)
    connector = TrendzAPIConnector()
    if connector.authenticate():
        if processor.df is not None:
            connector.upload_data(processor.df)
    
    print("\n🎉 Configuração concluída!")
    print("\nArquivos criados:")
    print("  - data/sample_thermal_data.csv")
    print("  - data/trendz_dashboard_config.json")
    print("\nPróximos passos:")
    print("  1. Acesse http://localhost:8888")
    print("  2. Importe a configuração dos dashboards térmicos")
    print("  3. Visualize as zonas de conforto térmico!")

if __name__ == "__main__":
    main()