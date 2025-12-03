from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ThermalDataInput(BaseModel):
    timestamp: datetime
    temperature: float
    humidity: float
    wind_velocity: float
    pressure: float
    solar_radiation: float

class ThermalDataOutput(BaseModel):
    id: int
    timestamp: datetime
    temperature: float
    humidity: float
    wind_velocity: float
    pressure: float
    solar_radiation: float
    thermal_sensation: float
    comfort_zone: str
    created_at: datetime

class ThermalDataBatch(BaseModel):
    data: List[ThermalDataInput]

class APIResponse(BaseModel):
    success: bool
    message: str
    data: dict = None

# Schemas for other routers can be added here
class ClusteringRequest(BaseModel):
    n_clusters: int

class ClusteringResponse(BaseModel):
    task_id: str

class PredictionRequest(BaseModel):
    model_name: str
    data: list

class PredictionResponse(BaseModel):
    prediction: list

class DashboardData(BaseModel):
    # Define fields for dashboard data
    pass

class SystemHealth(BaseModel):
    status: str
    db_connection: bool
    mlflow_connection: bool
