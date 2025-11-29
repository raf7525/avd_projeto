
from fastapi import APIRouter, HTTPException
from fastapi.models.schemas import PredictionRequest, PredictionResponse, APIResponse

router = APIRouter()

@router.post("/predict", response_model=APIResponse)
async def predict_thermal(request: PredictionRequest):
    return APIResponse(
        success=True,
        message="Predição em desenvolvimento",
        data={"status": "coming_soon", "request": request.dict()},
        errors=None
    )