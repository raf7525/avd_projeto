"""
Dashboard Router
===============

Endpoints para dados de dashboard e visualizações.
"""

from fastapi import APIRouter, HTTPException
from fastapi.models.schemas import DashboardData, APIResponse

router = APIRouter()

@router.get("/data", response_model=APIResponse)
async def get_dashboard_data():
    """
    📈 **Dados para dashboard**
    
    Retorna dados formatados para visualizações.
    """
    return APIResponse(
        success=True,
        message="Dashboard em desenvolvimento",
        data={"status": "coming_soon"},
        errors=None
    )