"""
Prediction Router
=================

Endpoints para predição de sensação térmica usando Machine Learning.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import sys
import os

# Adicionar path do projeto
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.services.prediction_service import ThermalPredictionService

router = APIRouter()

# Inicializar serviço de predição
prediction_service = ThermalPredictionService()

# Tentar carregar modelos existentes
if not prediction_service.load_models():
    print("⚠️ Modelos não encontrados. Execute /prediction/train para treinar.")

# Schemas
class PredictionInput(BaseModel):
    temperature: float
    humidity: float
    wind_velocity: float
    pressure: float
    solar_radiation: float
    timestamp: Optional[datetime] = None

class PredictionBatchInput(BaseModel):
    data: List[PredictionInput]
    model_name: Optional[str] = "random_forest"

class APIResponse(BaseModel):
    success: bool
    message: str
    data: dict = None

@router.post("/predict", response_model=APIResponse)
async def predict_thermal_sensation(
    input_data: PredictionInput,
    model: str = Query("random_forest", description="Modelo a usar: random_forest, gradient_boosting")
):
    """
    🔮 **Predizer sensação térmica**
    
    Faz predição da sensação térmica baseada em dados meteorológicos.
    
    **Modelos disponíveis:**
    - `random_forest`: Random Forest Regressor (padrão)
    - `gradient_boosting`: Gradient Boosting Regressor
    
    **Retorna:**
    - Sensação térmica física (fórmula)
    - Sensação térmica ML (modelo treinado)
    - Zona de conforto
    - Diferença entre predições
    """
    try:
        # Validar dados
        if not (0 <= input_data.humidity <= 100):
            raise HTTPException(status_code=400, detail="Umidade deve estar entre 0 e 100")
        
        if input_data.temperature < -50 or input_data.temperature > 60:
            raise HTTPException(status_code=400, detail="Temperatura fora do intervalo válido")
        
        # Fazer predição
        prediction = prediction_service.predict(
            temperature=input_data.temperature,
            humidity=input_data.humidity,
            wind_velocity=input_data.wind_velocity,
            pressure=input_data.pressure,
            solar_radiation=input_data.solar_radiation,
            model_name=model,
            timestamp=input_data.timestamp
        )
        
        return APIResponse(
            success=True,
            message="Predição realizada com sucesso",
            data=prediction
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na predição: {str(e)}")

@router.post("/predict/batch", response_model=APIResponse)
async def predict_batch(
    batch_input: PredictionBatchInput
):
    """
    🔮 **Predição em lote**
    
    Faz predições para múltiplos pontos de dados.
    """
    try:
        data_list = [item.dict() for item in batch_input.data]
        
        predictions = prediction_service.predict_batch(
            data=data_list,
            model_name=batch_input.model_name
        )
        
        return APIResponse(
            success=True,
            message=f"{len(predictions)} predições realizadas",
            data={
                "predictions": predictions,
                "total": len(predictions),
                "model_used": batch_input.model_name
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na predição em lote: {str(e)}")

@router.post("/train", response_model=APIResponse)
async def train_models():
    """
    🎓 **Treinar modelos de predição**
    
    Treina todos os modelos de Machine Learning usando os dados disponíveis.
    
    **Modelos treinados:**
    - Random Forest Regressor
    - Gradient Boosting Regressor
    
    **Processo:**
    1. Carrega dados de `/app/data/sample_thermal_data.csv`
    2. Prepara features (incluindo features derivadas)
    3. Treina modelos com validação
    4. Salva modelos e registra no MLflow
    """
    try:
        results = prediction_service.train_models()
        
        return APIResponse(
            success=True,
            message="Modelos treinados com sucesso",
            data={
                "models_trained": list(results.keys()),
                "metrics": results,
                "mlflow_uri": prediction_service.mlflow_uri
            }
        )
        
    except FileNotFoundError:
        raise HTTPException(
            status_code=404, 
            detail="Arquivo de dados não encontrado. Execute generate_data.py primeiro."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no treinamento: {str(e)}")

@router.get("/models", response_model=APIResponse)
async def list_models():
    """
    📋 **Listar modelos disponíveis**
    
    Retorna informações sobre os modelos treinados e disponíveis.
    """
    try:
        available_models = list(prediction_service.models.keys())
        
        model_info = {}
        for model_name in available_models:
            model_path = os.path.join(prediction_service.model_dir, f"{model_name}.pkl")
            if os.path.exists(model_path):
                model_info[model_name] = {
                    "status": "loaded",
                    "path": model_path,
                    "size_mb": round(os.path.getsize(model_path) / (1024 * 1024), 2)
                }
        
        return APIResponse(
            success=True,
            message="Modelos listados",
            data={
                "available_models": available_models,
                "model_info": model_info,
                "total_models": len(available_models)
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar modelos: {str(e)}")

@router.get("/comfort-zones", response_model=APIResponse)
async def get_comfort_zones():
    """
    🌡️ **Informações sobre zonas de conforto**
    
    Retorna a classificação das zonas de conforto térmico.
    """
    return APIResponse(
        success=True,
        message="Zonas de conforto térmico",
        data={
            "zones": [
                {"name": "Muito Frio", "range": "< 15°C", "description": "Desconforto por frio intenso"},
                {"name": "Frio", "range": "15-18°C", "description": "Desconforto por frio"},
                {"name": "Fresco", "range": "18-20°C", "description": "Levemente frio, mas tolerável"},
                {"name": "Confortável", "range": "20-26°C", "description": "Zona de conforto térmico ideal"},
                {"name": "Quente", "range": "26-29°C", "description": "Levemente quente"},
                {"name": "Muito Quente", "range": "> 29°C", "description": "Desconforto por calor"}
            ],
            "standard": "Baseado em ASHRAE 55 e ISO 7730"
        }
    )
