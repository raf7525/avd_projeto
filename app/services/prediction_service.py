"""
Prediction Service
==================

Serviço para previsão de sensação térmica usando Machine Learning.
Suporta múltiplos modelos: Random Forest, Gradient Boosting, XGBoost, LSTM.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import mlflow
import mlflow.sklearn

class ThermalPredictionService:
    """Serviço de predição de sensação térmica."""
    
    def __init__(self):
        """Inicializar serviço de predição."""
        self.models = {}
        self.scalers = {}
        self.model_dir = "/app/models"
        self.mlflow_uri = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
        
        # Criar diretório de modelos se não existir
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Configurar MLflow
        mlflow.set_tracking_uri(self.mlflow_uri)
        mlflow.set_experiment("thermal_sensation_prediction")
    
    def calculate_thermal_sensation(
        self,
        temperature: float,
        humidity: float,
        wind_velocity: float,
        pressure: float,
        solar_radiation: float
    ) -> float:
        """
        Calcular sensação térmica usando fórmula física.
        
        Fórmula baseada em Heat Index e Wind Chill com ajustes para radiação solar.
        """
        # Base: temperatura
        sensation = temperature
        
        # Ajuste por umidade (Heat Index simplificado)
        if temperature > 27:
            humidity_factor = 0.5555 * (humidity / 100 - 1) * (temperature - 14.5)
            sensation += humidity_factor
        
        # Ajuste por vento (Wind Chill)
        if wind_velocity > 4.8:  # > 4.8 km/h tem efeito perceptível
            wind_chill = 13.12 + 0.6215 * temperature - 11.37 * (wind_velocity ** 0.16) + 0.3965 * temperature * (wind_velocity ** 0.16)
            sensation = min(sensation, wind_chill)
        
        # Ajuste por radiação solar
        if solar_radiation > 0:
            radiation_effect = (solar_radiation / 800) * 2.5  # Máximo +2.5°C
            sensation += radiation_effect
        
        # Ajuste por pressão (pequeno efeito)
        pressure_effect = (pressure - 1013) * 0.01
        sensation += pressure_effect
        
        return round(sensation, 2)
    
    def get_comfort_zone(self, thermal_sensation: float) -> str:
        """
        Classificar zona de conforto baseada na sensação térmica.
        
        Baseado em ASHRAE 55 e ISO 7730 (PMV/PPD).
        """
        if thermal_sensation < 15:
            return "Muito Frio"
        elif thermal_sensation < 18:
            return "Frio"
        elif thermal_sensation < 20:
            return "Fresco"
        elif thermal_sensation < 26:
            return "Confortável"
        elif thermal_sensation < 29:
            return "Quente"
        else:
            return "Muito Quente"
    
    def prepare_features(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Preparar features para treinamento.
        
        Args:
            df: DataFrame com dados meteorológicos
            
        Returns:
            X: Features normalizadas
            y: Target (sensação térmica)
        """
        # Features básicas
        feature_columns = ['temperature', 'humidity', 'wind_velocity', 'pressure', 'solar_radiation']
        
        # Adicionar features derivadas
        df['temp_humidity_interaction'] = df['temperature'] * df['humidity'] / 100
        df['wind_chill_factor'] = df['wind_velocity'] ** 0.16
        df['radiation_normalized'] = df['solar_radiation'] / 1000
        df['pressure_deviation'] = (df['pressure'] - 1013) / 10
        
        # Features temporais (se timestamp disponível)
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['hour'] = df['timestamp'].dt.hour
            df['day_of_year'] = df['timestamp'].dt.dayofyear
            df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
            df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
            df['day_sin'] = np.sin(2 * np.pi * df['day_of_year'] / 365)
            df['day_cos'] = np.cos(2 * np.pi * df['day_of_year'] / 365)
            
            feature_columns.extend(['hour_sin', 'hour_cos', 'day_sin', 'day_cos'])
        
        feature_columns.extend([
            'temp_humidity_interaction',
            'wind_chill_factor', 
            'radiation_normalized',
            'pressure_deviation'
        ])
        
        X = df[feature_columns].values
        y = df['thermal_sensation'].values
        
        return X, y
    
    def train_random_forest(self, X_train, X_test, y_train, y_test) -> Dict:
        """Treinar modelo Random Forest."""
        print("Treinando Random Forest...")
        
        with mlflow.start_run(run_name="random_forest"):
            # Hiperparâmetros
            params = {
                'n_estimators': 200,
                'max_depth': 20,
                'min_samples_split': 5,
                'min_samples_leaf': 2,
                'random_state': 42,
                'n_jobs': -1
            }
            
            # Log parâmetros
            mlflow.log_params(params)
            
            # Treinar
            model = RandomForestRegressor(**params)
            model.fit(X_train, y_train)
            
            # Avaliar
            y_pred_train = model.predict(X_train)
            y_pred_test = model.predict(X_test)
            
            metrics = {
                'train_rmse': np.sqrt(mean_squared_error(y_train, y_pred_train)),
                'test_rmse': np.sqrt(mean_squared_error(y_test, y_pred_test)),
                'train_mae': mean_absolute_error(y_train, y_pred_train),
                'test_mae': mean_absolute_error(y_test, y_pred_test),
                'train_r2': r2_score(y_train, y_pred_train),
                'test_r2': r2_score(y_test, y_pred_test)
            }
            
            # Log métricas
            mlflow.log_metrics(metrics)
            
            # Salvar modelo
            mlflow.sklearn.log_model(model, "model")
            model_path = os.path.join(self.model_dir, "random_forest.pkl")
            joblib.dump(model, model_path)
            
            self.models['random_forest'] = model
            
            print(f"✅ Random Forest - Test RMSE: {metrics['test_rmse']:.4f}, R²: {metrics['test_r2']:.4f}")
            
            return metrics
    
    def train_gradient_boosting(self, X_train, X_test, y_train, y_test) -> Dict:
        """Treinar modelo Gradient Boosting."""
        print("Treinando Gradient Boosting...")
        
        with mlflow.start_run(run_name="gradient_boosting"):
            # Hiperparâmetros
            params = {
                'n_estimators': 200,
                'learning_rate': 0.1,
                'max_depth': 7,
                'min_samples_split': 5,
                'min_samples_leaf': 2,
                'subsample': 0.8,
                'random_state': 42
            }
            
            # Log parâmetros
            mlflow.log_params(params)
            
            # Treinar
            model = GradientBoostingRegressor(**params)
            model.fit(X_train, y_train)
            
            # Avaliar
            y_pred_train = model.predict(X_train)
            y_pred_test = model.predict(X_test)
            
            metrics = {
                'train_rmse': np.sqrt(mean_squared_error(y_train, y_pred_train)),
                'test_rmse': np.sqrt(mean_squared_error(y_test, y_pred_test)),
                'train_mae': mean_absolute_error(y_train, y_pred_train),
                'test_mae': mean_absolute_error(y_test, y_pred_test),
                'train_r2': r2_score(y_train, y_pred_train),
                'test_r2': r2_score(y_test, y_pred_test)
            }
            
            # Log métricas
            mlflow.log_metrics(metrics)
            
            # Salvar modelo
            mlflow.sklearn.log_model(model, "model")
            model_path = os.path.join(self.model_dir, "gradient_boosting.pkl")
            joblib.dump(model, model_path)
            
            self.models['gradient_boosting'] = model
            
            print(f"✅ Gradient Boosting - Test RMSE: {metrics['test_rmse']:.4f}, R²: {metrics['test_r2']:.4f}")
            
            return metrics
    
    def train_models(self, data_path: str = "/app/data/sample_thermal_data.csv") -> Dict:
        """
        Treinar todos os modelos.
        
        Args:
            data_path: Caminho para arquivo CSV com dados
            
        Returns:
            Dict com métricas de todos os modelos
        """
        print(f"📊 Carregando dados de {data_path}...")
        df = pd.read_csv(data_path)
        
        print(f"Total de registros: {len(df)}")
        
        # Preparar features
        X, y = self.prepare_features(df)
        
        # Normalizar features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Salvar scaler
        scaler_path = os.path.join(self.model_dir, "scaler.pkl")
        joblib.dump(scaler, scaler_path)
        self.scalers['standard'] = scaler
        
        # Split treino/teste
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )
        
        print(f"Treino: {X_train.shape}, Teste: {X_test.shape}")
        
        # Treinar modelos
        results = {}
        results['random_forest'] = self.train_random_forest(X_train, X_test, y_train, y_test)
        results['gradient_boosting'] = self.train_gradient_boosting(X_train, X_test, y_train, y_test)
        
        print("\n🎉 Treinamento concluído!")
        return results
    
    def load_models(self) -> bool:
        """
        Carregar modelos salvos.
        
        Returns:
            True se modelos foram carregados com sucesso
        """
        try:
            # Carregar scaler
            scaler_path = os.path.join(self.model_dir, "scaler.pkl")
            if os.path.exists(scaler_path):
                self.scalers['standard'] = joblib.load(scaler_path)
                print("✅ Scaler carregado")
            
            # Carregar Random Forest
            rf_path = os.path.join(self.model_dir, "random_forest.pkl")
            if os.path.exists(rf_path):
                self.models['random_forest'] = joblib.load(rf_path)
                print("✅ Random Forest carregado")
            
            # Carregar Gradient Boosting
            gb_path = os.path.join(self.model_dir, "gradient_boosting.pkl")
            if os.path.exists(gb_path):
                self.models['gradient_boosting'] = joblib.load(gb_path)
                print("✅ Gradient Boosting carregado")
            
            return len(self.models) > 0
            
        except Exception as e:
            print(f"❌ Erro ao carregar modelos: {e}")
            return False
    
    def predict(
        self,
        temperature: float,
        humidity: float,
        wind_velocity: float,
        pressure: float,
        solar_radiation: float,
        model_name: str = "random_forest",
        timestamp: Optional[datetime] = None
    ) -> Dict:
        """
        Fazer predição de sensação térmica.
        
        Args:
            temperature: Temperatura em °C
            humidity: Umidade relativa (%)
            wind_velocity: Velocidade do vento (km/h)
            pressure: Pressão atmosférica (hPa)
            solar_radiation: Radiação solar (W/m²)
            model_name: Nome do modelo ('random_forest', 'gradient_boosting')
            timestamp: Timestamp opcional para features temporais
            
        Returns:
            Dict com predição e informações
        """
        # Calcular sensação térmica física (baseline)
        physical_sensation = self.calculate_thermal_sensation(
            temperature, humidity, wind_velocity, pressure, solar_radiation
        )
        
        result = {
            'physical_sensation': physical_sensation,
            'physical_comfort_zone': self.get_comfort_zone(physical_sensation),
            'input': {
                'temperature': temperature,
                'humidity': humidity,
                'wind_velocity': wind_velocity,
                'pressure': pressure,
                'solar_radiation': solar_radiation
            }
        }
        
        # Se modelo ML disponível, fazer predição
        if model_name in self.models and 'standard' in self.scalers:
            try:
                # Preparar features
                features = {
                    'temperature': temperature,
                    'humidity': humidity,
                    'wind_velocity': wind_velocity,
                    'pressure': pressure,
                    'solar_radiation': solar_radiation,
                    'temp_humidity_interaction': temperature * humidity / 100,
                    'wind_chill_factor': wind_velocity ** 0.16,
                    'radiation_normalized': solar_radiation / 1000,
                    'pressure_deviation': (pressure - 1013) / 10
                }
                
                # Features temporais
                if timestamp:
                    hour = timestamp.hour
                    day_of_year = timestamp.timetuple().tm_yday
                    features['hour_sin'] = np.sin(2 * np.pi * hour / 24)
                    features['hour_cos'] = np.cos(2 * np.pi * hour / 24)
                    features['day_sin'] = np.sin(2 * np.pi * day_of_year / 365)
                    features['day_cos'] = np.cos(2 * np.pi * day_of_year / 365)
                else:
                    # Valores padrão se timestamp não fornecido
                    features['hour_sin'] = 0
                    features['hour_cos'] = 1
                    features['day_sin'] = 0
                    features['day_cos'] = 1
                
                # Montar array de features
                feature_array = np.array([list(features.values())]).reshape(1, -1)
                
                # Normalizar
                feature_scaled = self.scalers['standard'].transform(feature_array)
                
                # Predição
                ml_prediction = self.models[model_name].predict(feature_scaled)[0]
                
                result['ml_prediction'] = round(float(ml_prediction), 2)
                result['ml_comfort_zone'] = self.get_comfort_zone(ml_prediction)
                result['model_used'] = model_name
                result['prediction_difference'] = round(ml_prediction - physical_sensation, 2)
                
            except Exception as e:
                result['ml_error'] = str(e)
        
        return result
    
    def predict_batch(
        self,
        data: List[Dict],
        model_name: str = "random_forest"
    ) -> List[Dict]:
        """
        Fazer predições em lote.
        
        Args:
            data: Lista de dicts com dados meteorológicos
            model_name: Nome do modelo
            
        Returns:
            Lista de predições
        """
        results = []
        
        for item in data:
            timestamp = None
            if 'timestamp' in item:
                timestamp = pd.to_datetime(item['timestamp'])
            
            prediction = self.predict(
                temperature=item['temperature'],
                humidity=item['humidity'],
                wind_velocity=item['wind_velocity'],
                pressure=item['pressure'],
                solar_radiation=item['solar_radiation'],
                model_name=model_name,
                timestamp=timestamp
            )
            
            results.append(prediction)
        
        return results
