"""
Modelos de dados da API
======================

Exporta todos os modelos Pydantic para validação de dados.
"""

from .schemas import (
    WindDataInput,
    WindDataOutput,
    WindDataBatch,
    ClusteringRequest,
    ClusteringResponse,
    ClusterResult,
    PredictionRequest,
    PredictionResponse,
    PredictionResult,
    DashboardData,
    HealthStatus,
    SystemHealth,
    APIResponse,
    WindDirection
)

__all__ = [
    "WindDataInput",
    "WindDataOutput", 
    "WindDataBatch",
    "ClusteringRequest",
    "ClusteringResponse",
    "ClusterResult",
    "PredictionRequest",
    "PredictionResponse",
    "PredictionResult", 
    "DashboardData",
    "HealthStatus",
    "SystemHealth",
    "APIResponse",
    "WindDirection"
]