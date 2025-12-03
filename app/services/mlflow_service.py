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
    
    def load_model(self, model_name: str, stage: str = "Production"):
        """
        Carregar um modelo do registro do MLflow.
        
        Args:
            model_name: O nome do modelo registrado.
            stage: O estágio do modelo a ser carregado (ex: 'Staging', 'Production').
        
        Returns:
            O modelo PyFunc carregado ou None se ocorrer um erro.
        """
        model_uri = f"models:/{model_name}/{stage}"
        try:
            print(f"Loading model '{model_name}' from stage '{stage}' at {self.tracking_uri}")
            model = mlflow.pyfunc.load_model(model_uri)
            print("Model loaded successfully.")
            return model
        except Exception as e:
            print(f"Erro ao carregar modelo '{model_name}' do MLflow: {e}")
            return None

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