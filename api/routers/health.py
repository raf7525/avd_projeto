"""
Health Check Router
==================

Endpoints para verificação da saúde dos serviços.
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
import psutil
import requests
import asyncio
import time
from typing import Dict, Any

from api.models.schemas import SystemHealth, HealthStatus, APIResponse

router = APIRouter()

@router.get("/", response_model=SystemHealth)
async def health_check():
    """
    🏥 **Check geral de saúde do sistema**
    
    Verifica o status de todos os serviços integrados:
    - API (própria)
    - PostgreSQL
    - MLflow
    - ThingsBoard
    - Trendz Analytics
    - MinIO
    """
    start_time = time.time()
    
    # Verificar cada serviço
    services = []
    
    # API própria
    api_status = HealthStatus(
        service="fastapi",
        status="healthy",
        response_time=0,
        details={"version": "1.0.0", "python": "3.12.12"},
        last_check=datetime.now()
    )
    services.append(api_status)
    
    # PostgreSQL
    postgres_status = await check_postgres()
    services.append(postgres_status)
    
    # MLflow
    mlflow_status = await check_service("http://localhost:5000", "mlflow")
    services.append(mlflow_status)
    
    # ThingsBoard
    tb_status = await check_service("http://localhost:8080", "thingsboard")
    services.append(tb_status)
    
    # Trendz Analytics
    trendz_status = await check_service("http://localhost:8888", "trendz")
    services.append(trendz_status)
    
    # MinIO
    minio_status = await check_service("http://localhost:9001", "minio")
    services.append(minio_status)
    
    # Determinar status geral
    healthy_count = sum(1 for s in services if s.status == "healthy")
    total_services = len(services)
    
    if healthy_count == total_services:
        overall_status = "healthy"
    elif healthy_count >= total_services * 0.5:
        overall_status = "degraded"
    else:
        overall_status = "unhealthy"
    
    uptime = time.time() - start_time
    
    return SystemHealth(
        overall_status=overall_status,
        services=services,
        timestamp=datetime.now(),
        uptime=uptime
    )

@router.get("/simple")
async def simple_health():
    """
    ✅ **Health check simples**
    
    Retorna apenas se a API está respondendo.
    """
    return APIResponse(
        success=True,
        message="API está funcionando normalmente",
        data={
            "status": "healthy",
            "timestamp": datetime.now(),
            "uptime": psutil.boot_time()
        }
    )

@router.get("/services/{service_name}")
async def check_specific_service(service_name: str):
    """
    🔍 **Check de serviço específico**
    
    Verifica o status de um serviço específico.
    """
    service_urls = {
        "postgres": None,  # Verificação especial
        "mlflow": "http://localhost:5000",
        "thingsboard": "http://localhost:8080",
        "trendz": "http://localhost:8888",
        "minio": "http://localhost:9001"
    }
    
    if service_name not in service_urls:
        raise HTTPException(
            status_code=404, 
            detail=f"Serviço '{service_name}' não encontrado"
        )
    
    if service_name == "postgres":
        status = await check_postgres()
    else:
        status = await check_service(service_urls[service_name], service_name)
    
    return APIResponse(
        success=True,
        message=f"Status do serviço {service_name}",
        data=status.dict()
    )

@router.get("/system")
async def system_info():
    """
    💻 **Informações do sistema**
    
    Retorna métricas do sistema operacional.
    """
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return APIResponse(
        success=True,
        message="Informações do sistema",
        data={
            "cpu": {
                "usage_percent": cpu_percent,
                "count": psutil.cpu_count()
            },
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "percent": memory.percent,
                "used": memory.used
            },
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": (disk.used / disk.total) * 100
            },
            "timestamp": datetime.now()
        }
    )

# Funções auxiliares
async def check_service(url: str, service_name: str) -> HealthStatus:
    """Verificar status de um serviço HTTP."""
    start_time = time.time()
    
    try:
        # Usar timeout baixo para não travar
        response = requests.get(url, timeout=5)
        response_time = (time.time() - start_time) * 1000  # em ms
        
        if response.status_code == 200:
            status = "healthy"
            details = {"status_code": response.status_code}
        else:
            status = "unhealthy"
            details = {"status_code": response.status_code, "error": "Non-200 response"}
            
    except requests.exceptions.Timeout:
        response_time = 5000  # timeout de 5s
        status = "unhealthy"
        details = {"error": "Timeout"}
        
    except requests.exceptions.ConnectionError:
        response_time = None
        status = "unhealthy"
        details = {"error": "Connection refused"}
        
    except Exception as e:
        response_time = None
        status = "unknown"
        details = {"error": str(e)}
    
    return HealthStatus(
        service=service_name,
        status=status,
        response_time=response_time,
        details=details,
        last_check=datetime.now()
    )

async def check_postgres() -> HealthStatus:
    """Verificar status do PostgreSQL."""
    start_time = time.time()
    
    try:
        # Tentar importar e conectar
        import psycopg2
        
        conn = psycopg2.connect(
            host="localhost",
            port="5433",
            database="mlflow",
            user="user",
            password="password",
            connect_timeout=5
        )
        
        # Executar query simples
        cur = conn.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        
        cur.close()
        conn.close()
        
        response_time = (time.time() - start_time) * 1000
        
        return HealthStatus(
            service="postgres",
            status="healthy",
            response_time=response_time,
            details={"connection": "successful", "query_result": result[0]},
            last_check=datetime.now()
        )
        
    except psycopg2.OperationalError as e:
        response_time = (time.time() - start_time) * 1000
        return HealthStatus(
            service="postgres",
            status="unhealthy",
            response_time=response_time,
            details={"error": "Connection failed", "details": str(e)},
            last_check=datetime.now()
        )
        
    except Exception as e:
        return HealthStatus(
            service="postgres",
            status="unknown",
            response_time=None,
            details={"error": str(e)},
            last_check=datetime.now()
        )