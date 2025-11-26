"""
Dashboard Trendz Analytics para Análise de Padrões de Vento
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple
import requests

class WindDataProcessor:
    """Processador de dados de vento para Trendz Analytics"""
    
    def __init__(self, data_source: str = "/home/raf75/quinto-periodo/avd/avd_projeto/data/sample_wind_data.csv"):
        self.data_source = data_source
        self.df = None
        self.clusters = None
    
    def load_data(self) -> pd.DataFrame:
        """Carregar dados de vento"""
        try:
            self.df = pd.read_csv(self.data_source)
            self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
            self.df['hour'] = self.df['timestamp'].dt.hour
            self.df['day_of_week'] = self.df['timestamp'].dt.dayofweek
            self.df['month'] = self.df['timestamp'].dt.month
            
            print(f"✅ {len(self.df)} registros carregados")
            return self.df
            
        except Exception as e:
            print(f"❌ Erro ao carregar dados: {e}")
            return None
    
    def perform_clustering(self, n_clusters: int = 5) -> pd.DataFrame:
        """Realizar clustering dos padrões de vento"""
        from sklearn.cluster import KMeans
        from sklearn.preprocessing import StandardScaler
        
        if self.df is None:
            self.load_data()
        
        # Preparar features para clustering
        features = ['wind_velocity', 'wind_direction', 'hour', 'day_of_week']
        X = self.df[features].copy()
        
        # Tratar direção do vento (circular)
        X['wind_direction_sin'] = np.sin(np.radians(X['wind_direction']))
        X['wind_direction_cos'] = np.cos(np.radians(X['wind_direction']))
        X = X.drop('wind_direction', axis=1)
        
        # Normalizar features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Aplicar K-Means
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(X_scaled)
        
        # Adicionar clusters ao DataFrame
        self.df['cluster'] = clusters
        self.clusters = kmeans
        
        print(f"✅ Clustering realizado com {n_clusters} clusters")
        return self.df
    
    def get_cluster_statistics(self) -> Dict:
        """Obter estatísticas por cluster"""
        if 'cluster' not in self.df.columns:
            self.perform_clustering()
        
        stats = {}
        for cluster in sorted(self.df['cluster'].unique()):
            cluster_data = self.df[self.df['cluster'] == cluster]
            
            stats[f"Cluster {cluster}"] = {
                "count": len(cluster_data),
                "wind_velocity": {
                    "mean": cluster_data['wind_velocity'].mean(),
                    "std": cluster_data['wind_velocity'].std(),
                    "min": cluster_data['wind_velocity'].min(),
                    "max": cluster_data['wind_velocity'].max()
                },
                "wind_direction": {
                    "mean": cluster_data['wind_direction'].mean(),
                    "predominant_hours": cluster_data['hour'].mode().tolist(),
                    "predominant_days": cluster_data['day_of_week'].mode().tolist()
                },
                "temporal_patterns": {
                    "most_common_hour": cluster_data['hour'].mode().iloc[0] if len(cluster_data['hour'].mode()) > 0 else None,
                    "most_common_day": cluster_data['day_of_week'].mode().iloc[0] if len(cluster_data['day_of_week'].mode()) > 0 else None
                }
            }
        
        return stats

class TrendzDashboardCreator:
    """Criador de dashboards para Trendz Analytics"""
    
    def __init__(self, processor: WindDataProcessor):
        self.processor = processor
        self.trendz_url = "http://localhost:8888"
    
    def create_wind_rose_visualization(self) -> Dict:
        """Criar visualização Rosa dos Ventos"""
        if self.processor.df is None:
            self.processor.load_data()
        
        if 'cluster' not in self.processor.df.columns:
            self.processor.perform_clustering()
        
        # Configuração da Rosa dos Ventos para Trendz
        wind_rose_config = {
            "name": "Rosa dos Ventos - Clusters",
            "type": "polar_chart",
            "data_source": "wind_data",
            "configuration": {
                "angle_field": "wind_direction",
                "radius_field": "wind_velocity", 
                "color_field": "cluster",
                "aggregation": "mean",
                "bins": 16,  # 16 direções cardeais
                "color_scheme": "viridis"
            },
            "filters": {
                "time_range": "last_30_days",
                "min_velocity": 0,
                "max_velocity": 30
            }
        }
        
        return wind_rose_config
    
    def create_temporal_patterns_dashboard(self) -> Dict:
        """Criar dashboard de padrões temporais"""
        temporal_dashboard = {
            "name": "Padrões Temporais de Vento",
            "widgets": [
                {
                    "type": "heatmap",
                    "title": "Velocidade por Hora/Dia",
                    "x_axis": "hour",
                    "y_axis": "day_of_week",
                    "z_axis": "wind_velocity",
                    "aggregation": "mean"
                },
                {
                    "type": "line_chart",
                    "title": "Tendência Diária",
                    "x_axis": "hour", 
                    "y_axis": "wind_velocity",
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
                    "x_axis": "wind_direction",
                    "y_axis": "wind_velocity", 
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
                    "metric": "wind_velocity",
                    "aggregation": "mean",
                    "unit": "m/s",
                    "size": "medium"
                },
                {
                    "type": "kpi", 
                    "title": "Velocidade Máxima",
                    "metric": "wind_velocity",
                    "aggregation": "max",
                    "unit": "m/s",
                    "size": "medium"
                },
                {
                    "type": "gauge",
                    "title": "Direção Predominante",
                    "metric": "wind_direction",
                    "aggregation": "mode",
                    "min": 0,
                    "max": 360,
                    "unit": "graus"
                },
                {
                    "type": "histogram",
                    "title": "Distribuição de Velocidades",
                    "metric": "wind_velocity",
                    "bins": 20,
                    "color_by": "cluster"
                }
            ]
        }
        
        return stats_panel
    
    def export_dashboard_config(self, output_file: str = "/home/raf75/quinto-periodo/avd/avd_projeto/data/trendz_dashboard_config.json"):
        """Exportar configuração completa dos dashboards"""
        config = {
            "project_name": "Análise de Padrões de Vento",
            "dashboards": {
                "wind_rose": self.create_wind_rose_visualization(),
                "temporal_patterns": self.create_temporal_patterns_dashboard(),
                "statistics": self.create_statistics_panel()
            },
            "data_sources": {
                "primary": {
                    "type": "csv",
                    "path": "/home/raf75/quinto-periodo/avd/avd_projeto/data/sample_wind_data.csv",
                    "fields": {
                        "timestamp": "datetime",
                        "wind_velocity": "float", 
                        "wind_direction": "float",
                        "temperature": "float",
                        "humidity": "float",
                        "cluster": "int"
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
    print("🌪️ Configurando Dashboard Trendz para Análise de Vento")
    print("=" * 60)
    
    # 1. Processar dados
    processor = WindDataProcessor()
    processor.load_data()
    processor.perform_clustering(n_clusters=5)
    
    # 2. Exibir estatísticas
    stats = processor.get_cluster_statistics()
    print("\n📊 Estatísticas por Cluster:")
    for cluster, data in stats.items():
        print(f"\n{cluster}:")
        print(f"  - Registros: {data['count']}")
        print(f"  - Velocidade média: {data['wind_velocity']['mean']:.2f} m/s")
        print(f"  - Hora predominante: {data['temporal_patterns']['most_common_hour']}h")
    
    # 3. Criar dashboards
    dashboard_creator = TrendzDashboardCreator(processor)
    config = dashboard_creator.export_dashboard_config()
    
    # 4. Conectar com Trendz (se disponível)
    connector = TrendzAPIConnector()
    if connector.authenticate():
        connector.upload_data(processor.df)
    
    print("\n🎉 Configuração concluída!")
    print("\nArquivos criados:")
    print("  - data/sample_wind_data.csv")
    print("  - data/trendz_dashboard_config.json")
    print("\nPróximos passos:")
    print("  1. Acesse http://localhost:8888")
    print("  2. Importe a configuração dos dashboards")
    print("  3. Visualize os padrões de vento!")

if __name__ == "__main__":
    main()