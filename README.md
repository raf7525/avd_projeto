# 🌡️ Projeto AVD - Análise e Visualização de Dados  
## PROBLEMA SELECIONADO
**Prever Sensação Térmica**  
Objetivo: Desenvolver sistema de previsão de sensação térmica e classificação de zonas de conforto baseado em dados meteorológicos históricos.  
Dados: Temperatura, umidade, velocidade do vento, pressão atmosférica e radiação solar (2000-2017).  
Visualização: Mapas de calor de conforto térmico + dashboards de predição + análises temporais de zonas de conforto.

## 🚀 CONFIGURAÇÃO RÁPIDA TRENDZ ANALYTICS - ANÁLISE TÉRMICA

### Executar configuração automática:
```bash
./setup-trendz.sh
```

### Acesso aos serviços:
- **Trendz Analytics**: http://localhost:8888 (tenant@thingsboard.org / tenant)  
- **ThingsBoard**: http://localhost:8080 (tenant@thingsboard.org / tenant)

📖 **Guia completo**: [docs/trendz-setup-guide.md](docs/trendz-setup-guide.md)

### 🌡️ Dataset Térmico  
- **157.800 registros** históricos (2000-2017)  
- **Campos**: temperature, humidity, wind_velocity, pressure, solar_radiation, thermal_sensation, comfort_zone  
- **5 Zonas de Conforto**: Muito Frio, Frio, Confortável, Quente, Muito Quente  
- **Algoritmos**: Heat Index + Wind Chill para cálculo de sensação térmica


# PORTAS
como requisitado no projeto as portas são essas:
 FastAPI:         http://localhost:8060
 Jupyter:         http://localhost:1010
 MLflow:          http://localhost:5000
 Trendz Analytics: http://localhost:8888
 ThingsBoard:     http://localhost:8080
  MinIO Console:    http://localhost:9001 (admin/minioadmin)
 PostgreSQL:      localhost:5433 (user/password)

# PASSOS FASTAPI - PREDIÇÃO TÉRMICA
 ✅ API de Sensação Térmica: Endpoints para cálculo e predição (thermal_comfort.py)  
 ✅ Banco PostgreSQL: Dataset de 157.800 registros térmicos integrado  
 🔄 ML Pipeline: Modelos de predição de conforto térmico em desenvolvimento  
 🔄 Dashboard: Visualizações de zonas de conforto e mapas de calor  
 ✅ Deploy: Sistema containerizado com Docker Compose funcionando