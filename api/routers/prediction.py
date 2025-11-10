"""
Prediction Router
================

Endpoints para predições de padrões de vento.
"""

from fastapi import APIRouter, HTTPException
from api.models.schemas import PredictionRequest, PredictionResponse, APIResponse

router = APIRouter()

@router.post("/predict", response_model=APIResponse)
async def predict_wind(request: PredictionRequest):
    """
    🔮 **Predição de padrões de vento**
    
    Usa modelos ML para predizer comportamento futuro do vento.
    """
    return APIResponse(
        success=True,
        message="Predição em desenvolvimento",
        data={"status": "coming_soon", "request": request.dict()},
        errors=None
    )