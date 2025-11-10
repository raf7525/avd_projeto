"""
MLflow Service
=============

Serviços para integração com MLflow.
"""

import mlflow
import os
from typing import Dict, Any

class MLflowService:
    """Serviço para interação com MLflow."""
    
    def __init__(self):
        """Inicializar serviço MLflow."""
        self.tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
        mlflow.set_tracking_uri(self.tracking_uri)
    
    def get_experiments(self):
        """Listar experimentos."""
        try:
            return mlflow.search_experiments()
        except Exception as e:
            print(f"Erro ao buscar experimentos: {e}")
            return []
    
    def log_metrics(self, metrics: Dict[str, Any]):
        """Log de métricas."""
        try:
            for key, value in metrics.items():
                mlflow.log_metric(key, value)
            return True
        except Exception as e:
            print(f"Erro ao fazer log de métricas: {e}")
            return False