from fastapi import APIRouter
from app.models.schemas import ClusteringRequest, APIResponse

router = APIRouter()

@router.post("/analyze", response_model=APIResponse)
async def analyze_clustering(request: ClusteringRequest):
    
    return APIResponse(
        success=True,
        message="Clustering em desenvolvimento",
        data={"status": "coming_soon", "request": request.dict()},
        errors=None
    )