from fastapi import APIRouter, HTTPException
from typing import List
import pandas as pd
from app.models.schemas import ThermalDataInput, APIResponse
from app.services.mlflow_service import MLflowService

router = APIRouter()

# Initialize service and load model at startup
mlflow_service = MLflowService()
# NOTE: In a production system, you might want to manage model loading more robustly.
# For this project, loading on module import is sufficient.
MODEL_NAME = "random_forest_model"
try:
    # Attempt to load Production model first, fall back to Staging
    model = mlflow_service.load_model(MODEL_NAME, stage="Production")
    if model is None:
        print("Falling back to 'Staging' model.")
        model = mlflow_service.load_model(MODEL_NAME, stage="Staging")
except Exception as e:
    model = None
    print(f"Could not load any version of model '{MODEL_NAME}'. Predictions will fail. Error: {e}")

class PredictionRequest(BaseModel):
    data: List[ThermalDataInput]

@router.post("/predict", response_model=APIResponse)
async def predict_comfort_zone(request: PredictionRequest):
    """
    Realiza predições da zona de conforto térmico usando um modelo de ML.
    """
    if model is None:
        raise HTTPException(
            status_code=503, 
            detail="Modelo de predição não está disponível no momento."
        )

    try:
        # Convert input data to DataFrame
        input_data = [item.dict() for item in request.data]
        df = pd.DataFrame(input_data)
        
        # Ensure correct feature order
        features = ['temperature', 'humidity', 'wind_velocity', 'pressure', 'solar_radiation']
        df = df[features]

        # Make predictions
        predictions = model.predict(df)
        
        # Combine input with predictions for a comprehensive response
        results = []
        for i, item in enumerate(input_data):
            result = item.copy()
            result['predicted_comfort_zone'] = predictions[i]
            results.append(result)

        return APIResponse(
            success=True,
            message=f"{len(predictions)} predições realizadas com sucesso.",
            data={"predictions": results}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro durante a predição: {e}")