from fastapi import APIRouter, HTTPException
from app.models.schemas import ClusteringRequest, ClusteringResponse, APIResponse

router = APIRouter()

@router.post("/analyze", response_model=APIResponse)
async def analyze_clustering(request: ClusteringRequest):
    
    return APIResponse(
        success=True,
        message="Clustering em desenvolvimento",
        data={"status": "coming_soon", "request": request.dict()},
        errors=None
    )