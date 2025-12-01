from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    errors: Optional[List[str]] = None

class ThermalDataInput(BaseModel):
    timestamp: datetime
    temperature: float
    humidity: float
    wind_velocity: float
    pressure: float
    solar_radiation: float

class ThermalDataOutput(ThermalDataInput):
    id: int
    thermal_sensation: float
    comfort_zone: str
    created_at: datetime

class ThermalDataBatch(BaseModel):
    data: List[ThermalDataInput]

class ClusteringRequest(BaseModel):
    algorithm: str = "kmeans"
    parameters: Dict[str, Any] = {}

class ClusteringResponse(BaseModel):
    clusters: List[Dict[str, Any]]

class PredictionRequest(BaseModel):
    features: Dict[str, float]

class PredictionResponse(BaseModel):
    prediction: float
    probability: Optional[float] = None

class DashboardData(BaseModel):
    metrics: Dict[str, Any]

class SystemHealth(BaseModel):
    status: str
    database: bool
    mlflow: bool
