"""
FastAPI - Análise de Padrões de Vento
=====================================

API REST para análise de padrões de vento com clustering e visualização.
Integrado com MLflow, ThingsBoard e Trendz Analytics.

Endpoints principais:
- /wind/data: CRUD de dados de vento
- /wind/analysis: Análise e clustering
- /wind/prediction: Predições ML
- /dashboard: Integrações com dashboards
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import os
from datetime import datetime

# Routers
from api.routers import wind_data, analysis, prediction, dashboard, health

# Configurações
app = FastAPI(
    title="AVD - Análise de Padrões de Vento",
    description="API REST para análise de padrões de vento com Machine Learning",
    version="1.0.0",
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
app.include_router(wind_data.router, prefix="/wind", tags=["Wind Data"])
app.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
app.include_router(prediction.router, prefix="/prediction", tags=["Prediction"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

# Servir arquivos estáticos (se necessário)
# app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Página inicial da API com links para documentação e serviços."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AVD - Análise de Padrões de Vento</title>
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
                background: #3498db;
                color: white;
                padding: 15px;
                text-decoration: none;
                border-radius: 5px;
                text-align: center;
                transition: background 0.3s;
            }
            .link-card:hover { background: #2980b9; }
            .status { 
                background: #e8f5e8; 
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
                <h1>🌪️ AVD - Análise de Padrões de Vento</h1>
                <p>API REST para análise de padrões de vento com Machine Learning</p>
            </div>
            
            <div class="status">
                <strong>📊 Status:</strong> API Online - """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """
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
                    <small>(Desenvolvimento)</small>
                </a>
                <a href="http://localhost:5000" class="link-card">
                    <span class="emoji">🔬</span><br>
                    MLflow<br>
                    <small>(Tracking ML)</small>
                </a>
                <a href="http://localhost:8080" class="link-card">
                    <span class="emoji">🌐</span><br>
                    ThingsBoard<br>
                    <small>(IoT Platform)</small>
                </a>
                <a href="http://localhost:8888" class="link-card">
                    <span class="emoji">📈</span><br>
                    Trendz Analytics<br>
                    <small>(Business Intelligence)</small>
                </a>
                <a href="http://localhost:9001" class="link-card">
                    <span class="emoji">🗄️</span><br>
                    MinIO Console<br>
                    <small>(Storage)</small>
                </a>
            </div>

            <h2>🎯 Endpoints Principais</h2>
            <ul>
                <li><strong>GET /wind/data</strong> - Listar dados de vento</li>
                <li><strong>POST /wind/data</strong> - Adicionar dados de vento</li>
                <li><strong>POST /analysis/cluster</strong> - Análise de clustering</li>
                <li><strong>GET /analysis/patterns</strong> - Padrões identificados</li>
                <li><strong>POST /prediction/wind</strong> - Predição de vento</li>
                <li><strong>GET /dashboard/thingsboard</strong> - Dados para ThingsBoard</li>
            </ul>

            <div class="status">
                <strong>🚀 Projeto:</strong> Agrupar Padrões de Vento<br>
                <strong>🎯 Objetivo:</strong> Agrupar horários/dias com comportamentos semelhantes de vento<br>
                <strong>📊 Visualização:</strong> Rosa dos ventos colorida por cluster + painel com médias
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
        "name": "AVD - Análise de Padrões de Vento",
        "version": "1.0.0",
        "description": "API REST para análise de padrões de vento com Machine Learning",
        "timestamp": datetime.now().isoformat(),
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