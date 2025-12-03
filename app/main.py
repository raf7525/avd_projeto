"""
FastAPI Application - Análise de Padrões de Vento
=================================================

API REST para análise de padrões de vento usando ML.
Integrada com MLflow, ThingsBoard e Trendz Analytics.
"""

import logging
import os
import sys
from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Adicionar o diretório raiz ao Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.schemas import APIResponse
from app.routers import clustering, dashboard, health, prediction, thermal_comfort
from app.services.database import get_db_connection
from app.services.mlflow_service import MLflowService

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Inicializar FastAPI
app = FastAPI(
    title="thermal Pattern Analysis API",
    description="""
    🌪️ **API para Análise de Padrões de Vento**
    
    Esta API oferece funcionalidades completas para:
    
    * 📊 **Coleta e armazenamento** de dados de vento
    * 🤖 **Análise de clustering** para identificar padrões
    * 🔮 **Predição** de comportamento futuro do vento
    * 📈 **Dashboards** interativos e visualizações
    * 🏥 **Monitoramento** de saúde do sistema
    
    **Tecnologias integradas:**
    - MLflow para tracking de experimentos
    - PostgreSQL para persistência
    - ThingsBoard para IoT
    - Trendz Analytics para BI
    """,
    version="1.0.0",
    contact={
        "name": "Projeto AVD - Padrões de Vento",
        "url": "http://localhost:8060",
    },
    license_info={
        "name": "MIT License",
    },
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para logging de requests
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = datetime.now()
    
    response = await call_next(request)
    
    process_time = (datetime.now() - start_time).total_seconds()
    
    logger.info(
        f"{request.method} {request.url} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.2f}s"
    )
    
    return response

# Inicializar serviços
mlflow_service = None

@app.on_event("startup")
async def startup_event():
    """Inicializar serviços na inicialização da aplicação."""
    global mlflow_service
    
    logger.info("🚀 Inicializando thermal Pattern Analysis API...")
    
    try:
        # Inicializar MLflow
        mlflow_service = MLflowService()
        logger.info("✅ MLflow service inicializado")
        
        # Testar conexão com banco
        db = get_db_connection()
        if db:
            logger.info("✅ Conexão com banco de dados estabelecida")
            db.close()
        
        logger.info("🎉 API inicializada com sucesso!")
        
    except Exception as e:
        logger.error(f"❌ Erro na inicialização: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup na finalização da aplicação."""
    logger.info("🛑 Finalizando Thermal Pattern Analysis API...")

# Incluir routers
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(thermal_comfort.router, prefix="/thermal_comfort", tags=["Thermal Comfort"])
app.include_router(clustering.router, prefix="/clustering", tags=["Clustering"])
app.include_router(prediction.router, prefix="/prediction", tags=["Prediction"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])

# Endpoints principais
@app.get("/", response_model=APIResponse)
async def root():
    """
    🏠 **Endpoint raiz da API**
    
    Retorna informações básicas sobre a API e status geral.
    """
    return APIResponse(
        success=True,
        message="thermal Pattern Analysis API está funcionando!",
        data={
            "version": "1.0.0",
            "description": "API para análise de padrões de vento",
            "docs": "/docs",
            "health": "/health",
            "timestamp": datetime.now(),
            "endpoints": {
                "thermal_data": "/api/v1/thermal",
                "clustering": "/api/v1/clustering", 
                "prediction": "/api/v1/prediction",
                "dashboard": "/api/v1/dashboard"
            }
        }
    )

@app.get("/info")
async def api_info():
    """
    ℹ️ **Informações detalhadas da API**
    
    Retorna informações técnicas sobre a configuração da API.
    """
    return {
        "api_name": "thermal Pattern Analysis API",
        "version": "1.0.0",
        "python_version": sys.version,
        "environment": {
            "PYTHON_PATH": sys.executable,
            "VIRTUAL_ENV": os.environ.get("VIRTUAL_ENV", "Não detectado"),
            "PORT": os.environ.get("PORT", "8060"),
        },
        "services": {
            "mlflow": "http://localhost:5000",
            "postgres": "localhost:5433",
            "thingsboard": "http://localhost:8080",
            "trendz": "http://localhost:8888"
        },
        "features": [
            "Coleta de dados de vento",
            "Análise de clustering",
            "Predição ML",
            "Dashboard interativo",
            "Integração IoT"
        ]
    }

# Tratamento de exceções
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handler personalizado para HTTPExceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(
            success=False,
            message=exc.detail,
            errors=[f"HTTP {exc.status_code}: {exc.detail}"],
            timestamp=datetime.now()
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handler geral para exceções não tratadas."""
    logger.error(f"Erro não tratado: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=APIResponse(
            success=False,
            message="Erro interno do servidor",
            errors=[str(exc)],
            timestamp=datetime.now()
        ).dict()
    )

# Configuração para desenvolvimento
if __name__ == "__main__":
    # Porta configurada para 8060 conforme requisitos
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8060,
        reload=True,
        log_level="info"
    )