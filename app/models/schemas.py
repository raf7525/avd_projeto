"""
Schemas Pydantic para validação de dados da API
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class ThermalDataInput(BaseModel):
    """Schema para entrada de dados meteorológicos"""
    temperature: float = Field(..., description="Temperatura em °C")
    humidity: float = Field(..., ge=0, le=100, description="Umidade relativa em %")
    wind_velocity: float = Field(..., ge=0, description="Velocidade do vento em km/h")
    pressure: float = Field(..., description="Pressão atmosférica em hPa")
    solar_radiation: float = Field(..., ge=0, description="Radiação solar em W/m²")
    timestamp: Optional[datetime] = Field(None, description="Timestamp da medição")

    class Config:
        json_schema_extra = {
            "example": {
                "temperature": 28.5,
                "humidity": 70.0,
                "wind_velocity": 5.0,
                "pressure": 1013.0,
                "solar_radiation": 600.0,
                "timestamp": "2025-12-03T16:00:00"
            }
        }


class ThermalDataOutput(BaseModel):
    """Schema para saída de dados de conforto térmico"""
    thermal_sensation: float = Field(..., description="Sensação térmica calculada")
    comfort_zone: str = Field(..., description="Zona de conforto térmico")
    recommendations: Optional[List[str]] = Field(None, description="Recomendações")
    input_data: ThermalDataInput = Field(..., description="Dados de entrada")


class ThermalDataBatch(BaseModel):
    """Schema para processamento em lote de dados térmicos"""
    data: List[ThermalDataInput] = Field(..., description="Lista de dados térmicos")
    process_type: Optional[str] = Field("comfort", description="Tipo de processamento")


class PredictionResult(BaseModel):
    """Schema para resultado de predição"""
    thermal_sensation_physical: float = Field(..., description="Sensação térmica calculada por fórmula física")
    thermal_sensation_ml: Optional[float] = Field(None, description="Sensação térmica predita por ML")
    comfort_zone_physical: str = Field(..., description="Zona de conforto pela fórmula física")
    comfort_zone_ml: Optional[str] = Field(None, description="Zona de conforto predita por ML")
    difference: Optional[float] = Field(None, description="Diferença entre predição ML e física")
    model_used: Optional[str] = Field(None, description="Nome do modelo usado")
    timestamp: Optional[datetime] = Field(None, description="Timestamp da predição")


class ClusteringResult(BaseModel):
    """Schema para resultado de clustering"""
    cluster_id: int = Field(..., description="ID do cluster")
    cluster_label: str = Field(..., description="Label do cluster")
    centroid: Dict[str, float] = Field(..., description="Centróide do cluster")
    size: int = Field(..., description="Número de pontos no cluster")


class SystemHealth(BaseModel):
    """Schema para status geral do sistema"""
    status: str = Field(..., description="Status geral: healthy, degraded, unhealthy")
    services: Dict[str, Any] = Field(..., description="Status de cada serviço")
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = Field(default="1.0.0", description="Versão da API")


class HealthStatus(BaseModel):
    """Schema para status de um serviço individual"""
    name: str = Field(..., description="Nome do serviço")
    is_healthy: bool = Field(..., description="Se o serviço está saudável")
    response_time: Optional[float] = Field(None, description="Tempo de resposta em segundos")
    message: Optional[str] = Field(None, description="Mensagem de status")
    details: Optional[Dict[str, Any]] = Field(None, description="Detalhes adicionais")


class APIResponse(BaseModel):
    """Schema genérico para respostas da API"""
    success: bool = Field(..., description="Se a operação foi bem-sucedida")
    message: str = Field(..., description="Mensagem descritiva")
    data: Optional[Dict[str, Any]] = Field(None, description="Dados da resposta")
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operação realizada com sucesso",
                "data": {"key": "value"},
                "timestamp": "2025-12-03T16:00:00"
            }
        }


class TrainingMetrics(BaseModel):
    """Schema para métricas de treinamento"""
    train_rmse: float = Field(..., description="RMSE no conjunto de treino")
    test_rmse: float = Field(..., description="RMSE no conjunto de teste")
    train_mae: float = Field(..., description="MAE no conjunto de treino")
    test_mae: float = Field(..., description="MAE no conjunto de teste")
    train_r2: float = Field(..., description="R² no conjunto de treino")
    test_r2: float = Field(..., description="R² no conjunto de teste")


class ClusteringRequest(BaseModel):
    """Schema para requisição de clustering"""
    data: List[ThermalDataInput] = Field(..., description="Dados para clustering")
    n_clusters: Optional[int] = Field(3, ge=2, le=10, description="Número de clusters")
    algorithm: Optional[str] = Field("kmeans", description="Algoritmo: kmeans, dbscan, hierarchical")


class ClusteringResponse(BaseModel):
    """Schema para resposta de clustering"""
    clusters: List[ClusteringResult] = Field(..., description="Resultados dos clusters")
    total_points: int = Field(..., description="Total de pontos analisados")
    algorithm_used: str = Field(..., description="Algoritmo utilizado")
    execution_time: float = Field(..., description="Tempo de execução em segundos")


class DashboardData(BaseModel):
    """Schema para dados de dashboard"""
    total_predictions: int = Field(0, description="Total de predições realizadas")
    total_trainings: int = Field(0, description="Total de treinamentos")
    average_temperature: Optional[float] = Field(None, description="Temperatura média")
    comfort_distribution: Optional[Dict[str, int]] = Field(None, description="Distribuição por zona de conforto")
    recent_predictions: Optional[List[Dict[str, Any]]] = Field(None, description="Predições recentes")
