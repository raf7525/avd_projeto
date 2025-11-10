"""
Modelos Pydantic para validação de dados da API
===============================================

Modelos para dados de vento, análises e predições.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class WindDirection(str, Enum):
    """Direções do vento em graus ou pontos cardeais."""
    N = "N"
    NE = "NE"
    E = "E"
    SE = "SE"
    S = "S"
    SW = "SW"
    W = "W"
    NW = "NW"

class WindDataInput(BaseModel):
    """Modelo para entrada de dados de vento."""
    timestamp: datetime = Field(..., description="Timestamp da medição")
    velocity: float = Field(..., ge=0, le=200, description="Velocidade do vento em km/h")
    direction: float = Field(..., ge=0, le=360, description="Direção do vento em graus (0-360)")
    temperature: Optional[float] = Field(None, description="Temperatura em °C")
    humidity: Optional[float] = Field(None, ge=0, le=100, description="Umidade em %")
    pressure: Optional[float] = Field(None, description="Pressão atmosférica em hPa")
    location_id: Optional[str] = Field(None, description="ID da localização/sensor")
    
    @validator('direction')
    def validate_direction(cls, v):
        if not 0 <= v <= 360:
            raise ValueError('Direção deve estar entre 0 e 360 graus')
        return v
    
    @validator('velocity')
    def validate_velocity(cls, v):
        if v < 0:
            raise ValueError('Velocidade não pode ser negativa')
        return v

class WindDataOutput(WindDataInput):
    """Modelo para saída de dados de vento."""
    id: Optional[int] = Field(None, description="ID único do registro")
    created_at: Optional[datetime] = Field(None, description="Timestamp de criação")
    direction_cardinal: Optional[str] = Field(None, description="Direção cardinal (N, NE, etc.)")
    
    class Config:
        from_attributes = True

class WindDataBatch(BaseModel):
    """Modelo para inserção em lote de dados de vento."""
    data: List[WindDataInput] = Field(..., description="Lista de dados de vento")
    
    @validator('data')
    def validate_data_not_empty(cls, v):
        if not v:
            raise ValueError('Lista de dados não pode estar vazia')
        return v

class ClusteringRequest(BaseModel):
    """Parâmetros para análise de clustering."""
    algorithm: str = Field(default="kmeans", description="Algoritmo de clustering (kmeans, dbscan, hierarchical)")
    n_clusters: Optional[int] = Field(default=5, ge=2, le=20, description="Número de clusters (para k-means)")
    features: List[str] = Field(default=["velocity", "direction"], description="Features para clustering")
    time_grouping: str = Field(default="hour", description="Agrupamento temporal (hour, day, week)")
    date_start: Optional[datetime] = Field(None, description="Data inicial para análise")
    date_end: Optional[datetime] = Field(None, description="Data final para análise")
    
    @validator('algorithm')
    def validate_algorithm(cls, v):
        allowed = ["kmeans", "dbscan", "hierarchical"]
        if v not in allowed:
            raise ValueError(f'Algoritmo deve ser um de: {allowed}')
        return v

class ClusterResult(BaseModel):
    """Resultado da análise de clustering."""
    cluster_id: int = Field(..., description="ID do cluster")
    data_points: int = Field(..., description="Número de pontos no cluster")
    center_velocity: float = Field(..., description="Velocidade média do cluster")
    center_direction: float = Field(..., description="Direção média do cluster")
    variance_velocity: float = Field(..., description="Variância da velocidade")
    variance_direction: float = Field(..., description="Variância da direção")
    time_periods: List[str] = Field(..., description="Períodos de tempo associados")
    
class ClusteringResponse(BaseModel):
    """Resposta completa da análise de clustering."""
    algorithm: str = Field(..., description="Algoritmo utilizado")
    n_clusters: int = Field(..., description="Número de clusters encontrados")
    silhouette_score: Optional[float] = Field(None, description="Score de silhueta")
    clusters: List[ClusterResult] = Field(..., description="Resultados dos clusters")
    execution_time: float = Field(..., description="Tempo de execução em segundos")
    total_data_points: int = Field(..., description="Total de pontos analisados")
    date_range: Dict[str, datetime] = Field(..., description="Período analisado")

class PredictionRequest(BaseModel):
    """Parâmetros para predição de vento."""
    timestamp: datetime = Field(..., description="Timestamp para predição")
    historical_hours: int = Field(default=24, ge=1, le=168, description="Horas históricas para contexto")
    model_type: str = Field(default="ensemble", description="Tipo de modelo (linear, rf, ensemble)")
    features: List[str] = Field(default=["velocity", "direction", "hour"], description="Features para predição")
    confidence_interval: bool = Field(default=True, description="Incluir intervalo de confiança")

class PredictionResult(BaseModel):
    """Resultado de uma predição."""
    timestamp: datetime = Field(..., description="Timestamp da predição")
    predicted_velocity: float = Field(..., description="Velocidade predita")
    predicted_direction: float = Field(..., description="Direção predita")
    confidence_velocity: Optional[Dict[str, float]] = Field(None, description="Intervalo de confiança velocidade")
    confidence_direction: Optional[Dict[str, float]] = Field(None, description="Intervalo de confiança direção")
    model_confidence: float = Field(..., description="Confiança do modelo (0-1)")

class PredictionResponse(BaseModel):
    """Resposta completa de predição."""
    model_type: str = Field(..., description="Tipo de modelo usado")
    predictions: List[PredictionResult] = Field(..., description="Resultados das predições")
    model_metrics: Dict[str, float] = Field(..., description="Métricas do modelo")
    execution_time: float = Field(..., description="Tempo de execução")

class DashboardData(BaseModel):
    """Dados formatados para dashboard."""
    timestamp: datetime = Field(..., description="Timestamp dos dados")
    metrics: Dict[str, Any] = Field(..., description="Métricas calculadas")
    charts: Dict[str, Any] = Field(..., description="Dados para gráficos")
    alerts: List[Dict[str, Any]] = Field(default=[], description="Alertas ativos")

class HealthStatus(BaseModel):
    """Status de saúde dos serviços."""
    service: str = Field(..., description="Nome do serviço")
    status: str = Field(..., description="Status (healthy, unhealthy, unknown)")
    response_time: Optional[float] = Field(None, description="Tempo de resposta em ms")
    details: Optional[Dict[str, Any]] = Field(None, description="Detalhes adicionais")
    last_check: datetime = Field(..., description="Último check realizado")

class SystemHealth(BaseModel):
    """Status geral do sistema."""
    overall_status: str = Field(..., description="Status geral (healthy, degraded, unhealthy)")
    services: List[HealthStatus] = Field(..., description="Status dos serviços")
    timestamp: datetime = Field(..., description="Timestamp do check")
    uptime: float = Field(..., description="Uptime em segundos")

class APIResponse(BaseModel):
    """Resposta padrão da API."""
    success: bool = Field(..., description="Indica se a operação foi bem-sucedida")
    message: str = Field(..., description="Mensagem descritiva")
    data: Optional[Any] = Field(None, description="Dados de resposta")
    errors: Optional[List[str]] = Field(None, description="Lista de erros, se houver")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp da resposta")