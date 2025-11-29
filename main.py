"""
FastAPI - Sistema de Predição de Sensação Térmica
=================================================

API REST para análise de sensação térmica e predição de conforto térmico.
Integrado com MLflow, ThingsBoard e Trendz Analytics.

Endpoints principais:
- /thermal/data: CRUD de dados térmicos (temperatura, umidade, pressão, radiação solar)
- /thermal/analysis: Cálculo de sensação térmica e classificação de conforto
- /thermal/prediction: Predições ML de conforto térmico
- /dashboard: Visualizações de zonas de conforto e análises temporais
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import os
from datetime import datetime

# Routers
from app.routers import thermal_comfort, prediction, dashboard, health, clustering

# Configurações
app = FastAPI(
    title="AVD - Sistema de Predição de Sensação Térmica",
    description="API REST para predição de conforto térmico com Machine Learning e análise de sensação térmica",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS - Permitir acesso de outras origens (ThingsBoard, Trendz, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar origens
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(thermal_comfort.router, prefix="/thermal", tags=["Thermal Comfort"])
app.include_router(clustering.router, prefix="/analysis", tags=["Thermal Analysis"])
app.include_router(prediction.router, prefix="/prediction", tags=["Thermal Prediction"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Thermal Dashboard"])

# Servir arquivos estáticos (se necessário)
# app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Página inicial da API com links para documentação e serviços."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AVD - Sistema de Predição de Sensação Térmica</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                max-width: 800px; 
                margin: 50px auto; 
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .header { 
                text-align: center; 
                color: #2c3e50;
                margin-bottom: 30px;
            }
            .links { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }
            .link-card {
                background: #e74c3c;
                color: white;
                padding: 15px;
                text-decoration: none;
                border-radius: 5px;
                text-align: center;
                transition: background 0.3s;
            }
            .link-card:hover { background: #c0392b; }
            .status { 
                background: #fff3cd; 
                padding: 15px; 
                border-radius: 5px; 
                margin: 20px 0;
                border-left: 4px solid #27ae60;
            }
            .emoji { font-size: 1.5em; margin-right: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌡️ AVD - Sistema de Predição de Sensação Térmica</h1>
                <p>API REST para predição de conforto térmico com Machine Learning</p>
            </div>
            
            <div class="status">
                <strong>🌡️ Status:</strong> API Online - Análise Térmica Ativa - """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """
            </div>

            <h2>🔗 Links Úteis</h2>
            <div class="links">
                <a href="/docs" class="link-card">
                    <span class="emoji">📚</span><br>
                    Documentação API<br>
                    <small>(Swagger UI)</small>
                </a>
                <a href="/redoc" class="link-card">
                    <span class="emoji">📖</span><br>
                    Documentação ReDoc<br>
                    <small>(Alternativa)</small>
                </a>
                <a href="/health/status" class="link-card">
                    <span class="emoji">❤️</span><br>
                    Health Check<br>
                    <small>(Status Serviços)</small>
                </a>
                <a href="http://localhost:1010" class="link-card">
                    <span class="emoji">📊</span><br>
                    Jupyter Notebooks<br>
                    <small>(Análise Térmica)</small>
                </a>
                <a href="http://localhost:5000" class="link-card">
                    <span class="emoji">🔬</span><br>
                    MLflow<br>
                    <small>(ML Térmico)</small>
                </a>
                <a href="http://localhost:8080" class="link-card">
                    <span class="emoji">🌐</span><br>
                    ThingsBoard<br>
                    <small>(Dados Térmicos)</small>
                </a>
                <a href="http://localhost:8888" class="link-card">
                    <span class="emoji">📈</span><br>
                    Trendz Analytics<br>
                    <small>(Análise Térmica)</small>
                </a>
                <a href="http://localhost:9001" class="link-card">
                    <span class="emoji">🗄️</span><br>
                    MinIO Console<br>
                    <small>(Storage Térmico)</small>
                </a>
            </div>

            <h2>🎯 Endpoints Principais</h2>
            <ul>
                <li><strong>GET /thermal/data</strong> - Listar dados de sensação térmica</li>
                <li><strong>POST /thermal/data</strong> - Adicionar dados térmicos</li>
                <li><strong>POST /thermal/calculate</strong> - Calcular sensação térmica</li>
                <li><strong>GET /thermal/comfort-zones</strong> - Análise de zonas de conforto</li>
                <li><strong>POST /prediction/thermal</strong> - Predição de conforto térmico</li>
                <li><strong>GET /dashboard/thermal-stats</strong> - Estatísticas térmicas</li>
            </ul>

            <div class="status">
                <strong>🚀 Projeto:</strong> Sistema de Predição de Sensação Térmica<br>
                <strong>🎯 Objetivo:</strong> Predizer sensação térmica e classificar zonas de conforto<br>
                <strong>📊 Dataset:</strong> 157.800 registros históricos (2000-2017) + 5 zonas de conforto
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

@app.get("/info")
async def info():
    """Informações da API e versão."""
    return {
        "name": "AVD - Sistema de Predição de Sensação Térmica",
        "version": "2.0.0",
        "description": "API REST para predição de conforto térmico com Machine Learning",
        "timestamp": datetime.now().isoformat(),
        "dataset": {
            "records": 157800,
            "period": "2000-2017",
            "comfort_zones": 5,
            "algorithm": "Heat Index + Wind Chill"
        },
        "docs": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json"
        },
        "services": {
            "jupyter": "http://localhost:1010",
            "mlflow": "http://localhost:5000",
            "thingsboard": "http://localhost:8080",
            "trendz": "http://localhost:8888",
            "minio": "http://localhost:9001"
        }
    }

if __name__ == "__main__":
    # Configuração para desenvolvimento
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8060,
        reload=True,
        log_level="info"
    )