"""
Thermal Sensation Predictor
===========================

Sistema de previsão de sensação térmica usando Machine Learning.
Suporta múltiplos modelos: Random Forest, Gradient Boosting, Neural Networks.
"""

import numpy as np
import pandas as pd
import pickle
import os
from typing import Dict, Tuple, Optional, List
from datetime import datetime
import joblib

# ML Libraries
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error


class ThermalSensationPredictor:
    """
    Preditor de sensação térmica usando Machine Learning.
    
    Suporta múltiplos algoritmos e treina automaticamente se necessário.
    """
    
    MODELS_DIR = "/app/models"
    
    def __init__(self, model_type: str = "random_forest"):
        """
        Inicializar preditor.
        
        Args:
            model_type: Tipo de modelo ('random_forest', 'gradient_boosting', 'neural_network')
        """
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.model_path = os.path.join(self.MODELS_DIR, f"{model_type}_model.pkl")
        self.scaler_path = os.path.join(self.MODELS_DIR, f"{model_type}_scaler.pkl")
        
        # Criar diretório de modelos se não existir
        os.makedirs(self.MODELS_DIR, exist_ok=True)
        
        # Tentar carregar modelo existente
        self._load_model()
    
    def _create_model(self):
        """Criar novo modelo baseado no tipo especificado."""
        if self.model_type == "random_forest":
            return RandomForestRegressor(
                n_estimators=100,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
        elif self.model_type == "gradient_boosting":
            return GradientBoostingRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            )
        elif self.model_type == "neural_network":
            return MLPRegressor(
                hidden_layer_sizes=(64, 32, 16),
                activation='relu',
                solver='adam',
                max_iter=1000,
                random_state=42
            )
        else:
            raise ValueError(f"Tipo de modelo não suportado: {self.model_type}")
    
    def _load_model(self) -> bool:
        """Carregar modelo e scaler salvos."""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                self.is_trained = True
                print(f"✅ Modelo {self.model_type} carregado com sucesso!")
                return True
        except Exception as e:
            print(f"⚠️  Erro ao carregar modelo: {e}")
        
        return False
    
    def _save_model(self):
        """Salvar modelo e scaler."""
        try:
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.scaler, self.scaler_path)
            print(f"✅ Modelo {self.model_type} salvo em {self.model_path}")
        except Exception as e:
            print(f"❌ Erro ao salvar modelo: {e}")
    
    def train(self, data_path: str = "/app/data/sample_thermal_data.csv"):
        """
        Treinar modelo com dados históricos.
        
        Args:
            data_path: Caminho para arquivo CSV com dados de treinamento
        """
        print(f"🔄 Treinando modelo {self.model_type}...")
        
        # Carregar dados
        df = pd.read_csv(data_path)
        print(f"📊 Dataset carregado: {len(df)} registros")
        
        # Features e target
        features = ['temperature', 'humidity', 'wind_velocity', 'pressure', 'solar_radiation']
        X = df[features].values
        y = df['thermal_sensation'].values
        
        # Split treino/teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Normalizar features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Criar e treinar modelo
        self.model = self._create_model()
        print(f"🤖 Treinando {self.model.__class__.__name__}...")
        
        self.model.fit(X_train_scaled, y_train)
        
        # Avaliar modelo
        y_pred_train = self.model.predict(X_train_scaled)
        y_pred_test = self.model.predict(X_test_scaled)
        
        # Métricas
        train_r2 = r2_score(y_train, y_pred_train)
        test_r2 = r2_score(y_test, y_pred_test)
        train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
        test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
        train_mae = mean_absolute_error(y_train, y_pred_train)
        test_mae = mean_absolute_error(y_test, y_pred_test)
        
        print(f"\n📈 Métricas de Treinamento:")
        print(f"   R² Score (treino): {train_r2:.4f}")
        print(f"   R² Score (teste):  {test_r2:.4f}")
        print(f"   RMSE (treino):     {train_rmse:.4f}°C")
        print(f"   RMSE (teste):      {test_rmse:.4f}°C")
        print(f"   MAE (treino):      {train_mae:.4f}°C")
        print(f"   MAE (teste):       {test_mae:.4f}°C")
        
        self.is_trained = True
        self._save_model()
        
        return {
            "model_type": self.model_type,
            "train_samples": len(X_train),
            "test_samples": len(X_test),
            "metrics": {
                "train_r2": float(train_r2),
                "test_r2": float(test_r2),
                "train_rmse": float(train_rmse),
                "test_rmse": float(test_rmse),
                "train_mae": float(train_mae),
                "test_mae": float(test_mae)
            }
        }
    
    def predict(
        self,
        temperature: float,
        humidity: float,
        wind_velocity: float,
        pressure: float,
        solar_radiation: float
    ) -> Tuple[float, str, float]:
        """
        Prever sensação térmica.
        
        Args:
            temperature: Temperatura do ar (°C)
            humidity: Umidade relativa (%)
            wind_velocity: Velocidade do vento (m/s)
            pressure: Pressão atmosférica (hPa)
            solar_radiation: Radiação solar (W/m²)
        
        Returns:
            Tupla (sensação_térmica, zona_conforto, confiança)
        """
        if not self.is_trained:
            print("⚠️  Modelo não treinado. Treinando agora...")
            self.train()
        
        # Preparar input
        X = np.array([[temperature, humidity, wind_velocity, pressure, solar_radiation]])
        X_scaled = self.scaler.transform(X)
        
        # Predição
        thermal_sensation = self.model.predict(X_scaled)[0]
        
        # Calcular confiança (baseado na distância da média de treinamento)
        confidence = self._calculate_confidence(X_scaled)
        
        # Classificar zona de conforto
        comfort_zone = self._classify_comfort_zone(thermal_sensation)
        
        return float(thermal_sensation), comfort_zone, float(confidence)
    
    def predict_batch(self, data: List[Dict]) -> List[Dict]:
        """
        Prever múltiplas observações.
        
        Args:
            data: Lista de dicionários com features
        
        Returns:
            Lista de predições
        """
        predictions = []
        
        for item in data:
            thermal_sensation, comfort_zone, confidence = self.predict(
                temperature=item['temperature'],
                humidity=item['humidity'],
                wind_velocity=item['wind_velocity'],
                pressure=item['pressure'],
                solar_radiation=item['solar_radiation']
            )
            
            predictions.append({
                "thermal_sensation": thermal_sensation,
                "comfort_zone": comfort_zone,
                "confidence": confidence,
                "input": item
            })
        
        return predictions
    
    def _calculate_confidence(self, X_scaled: np.ndarray) -> float:
        """
        Calcular confiança da predição baseado em ensemble ou variância.
        
        Args:
            X_scaled: Features normalizadas
        
        Returns:
            Confiança (0-1)
        """
        # Para Random Forest, usar variância entre árvores
        if hasattr(self.model, 'estimators_'):
            predictions = np.array([tree.predict(X_scaled)[0] for tree in self.model.estimators_])
            variance = np.var(predictions)
            # Converter variância em confiança (menor variância = maior confiança)
            confidence = 1.0 / (1.0 + variance)
            return min(confidence, 1.0)
        
        # Para outros modelos, retornar confiança padrão
        return 0.85
    
    def _classify_comfort_zone(self, thermal_sensation: float) -> str:
        """
        Classificar zona de conforto baseado na sensação térmica.
        
        Args:
            thermal_sensation: Sensação térmica calculada
        
        Returns:
            Nome da zona de conforto
        """
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
    
    def get_feature_importance(self) -> Optional[Dict[str, float]]:
        """
        Obter importância das features (apenas para modelos tree-based).
        
        Returns:
            Dicionário com importância de cada feature
        """
        if not hasattr(self.model, 'feature_importances_'):
            return None
        
        features = ['temperature', 'humidity', 'wind_velocity', 'pressure', 'solar_radiation']
        importances = self.model.feature_importances_
        
        return {
            feature: float(importance)
            for feature, importance in zip(features, importances)
        }


def calculate_thermal_sensation_formula(
    temperature: float,
    humidity: float,
    wind_velocity: float,
    pressure: Optional[float] = None,
    solar_radiation: Optional[float] = None
) -> Tuple[float, str]:
    """
    Calcular sensação térmica usando fórmulas físicas (Heat Index + Wind Chill).
    
    Args:
        temperature: Temperatura do ar (°C)
        humidity: Umidade relativa (%)
        wind_velocity: Velocidade do vento (m/s)
        pressure: Pressão atmosférica (hPa) - opcional
        solar_radiation: Radiação solar (W/m²) - opcional
    
    Returns:
        Tupla (sensação_térmica, zona_conforto)
    """
    # Wind Chill para temperaturas baixas
    if temperature < 27:
        if wind_velocity > 1.79:
            # Fórmula de Wind Chill (JAG/TI)
            wind_chill = (13.12 + 0.6215 * temperature - 
                         11.37 * (wind_velocity * 3.6)**0.16 + 
                         0.3965 * temperature * (wind_velocity * 3.6)**0.16)
            thermal_sensation = wind_chill
        else:
            thermal_sensation = temperature
    else:
        # Heat Index para temperaturas altas
        # Coeficientes da fórmula de Rothfusz
        c1 = -8.78469475556
        c2 = 1.61139411
        c3 = 2.33854883889
        c4 = -0.14611605
        c5 = -0.012308094
        c6 = -0.0164248277778
        c7 = 0.002211732
        c8 = 0.00072546
        c9 = -0.000003582
        
        heat_index = (c1 + (c2 * temperature) + (c3 * humidity) + 
                     (c4 * temperature * humidity) + (c5 * temperature**2) + 
                     (c6 * humidity**2) + (c7 * temperature**2 * humidity) + 
                     (c8 * temperature * humidity**2) + 
                     (c9 * temperature**2 * humidity**2))
        
        # Ajuste por vento
        if wind_velocity > 0:
            wind_factor = 1 - (wind_velocity * 0.05)
            wind_factor = max(wind_factor, 0.7)
            heat_index *= wind_factor
        
        # Ajuste por radiação solar
        if solar_radiation is not None and solar_radiation > 200:
            solar_factor = 1 + (solar_radiation - 200) / 2000
            heat_index *= solar_factor
        
        thermal_sensation = heat_index
    
    # Classificar zona de conforto
    if thermal_sensation < 16:
        comfort_zone = "Frio"
    elif thermal_sensation < 20:
        comfort_zone = "Fresco"
    elif thermal_sensation < 26:
        comfort_zone = "Confortável"
    elif thermal_sensation < 30:
        comfort_zone = "Quente"
    else:
        comfort_zone = "Muito Quente"
    
    return round(thermal_sensation, 2), comfort_zone
