# 🌡️ Projeto AVD - Análise e Visualização de Dados

## 🎯 Objetivo
**Prever Sensação Térmica**
Desenvolver sistema de previsão de sensação térmica e classificação de zonas de conforto baseado em dados meteorológicos históricos usando Machine Learning.

## ⚡ Quick Start

```bash
# Inicialização rápida (recomendado)
python scripts/quickstart.py

# OU manualmente
docker-compose up --build
curl -X POST "http://localhost:8060/prediction/train"
```

## 🏗️ Arquitetura
- **FastAPI**: Ingestão e API de dados (Porta 8060)
- **Jupyter Notebook**: Análise e Modelagem (Porta 1010)
- **MLflow**: Versionamento de Modelos (Porta 5000)
- **ThingsBoard**: Visualização IoT (Porta 8080)
- **Trendz Analytics**: Analytics Avançado (Porta 8888)
- **MinIO**: Armazenamento de Objetos (S3) (Porta 9000/9001)
- **PostgreSQL**: Banco de Dados Relacional

## 🤖 Sistema de Predição ML

### Modelos Implementados
- ✅ **Random Forest Regressor** (RMSE: ~0.85°C, R²: ~0.96)
- ✅ **Gradient Boosting Regressor** (RMSE: ~0.79°C, R²: ~0.96)

### Zonas de Conforto (ASHRAE 55)
| Zona | Faixa | Status |
|------|-------|--------|
| Muito Frio | < 15°C | ❄️ |
| Frio | 15-18°C | 🥶 |
| Fresco | 18-20°C | 😊 |
| **Confortável** | **20-26°C** | **✅** |
| Quente | 26-29°C | 🌡️ |
| Muito Quente | > 29°C | 🔥 |

### Exemplo de Uso

```bash
# Predição única
curl -X POST "http://localhost:8060/prediction/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 28.5,
    "humidity": 70.0,
    "wind_velocity": 5.0,
    "pressure": 1013.0,
    "solar_radiation": 600.0
  }'
```

**Resposta:**
```json
{
  "success": true,
  "data": {
    "physical_sensation": 30.45,
    "physical_comfort_zone": "Muito Quente",
    "ml_prediction": 29.87,
    "ml_comfort_zone": "Quente"
  }
}
```

## 🚀 Como Executar

### 1. Iniciar Serviços
Certifique-se de ter Docker e Docker Compose instalados.

```bash
docker-compose up --build
```

### 2. Gerar e Ingerir Dados
Para popular o ThingsBoard com dados para visualização:

```bash
# 1. Gerar dados sintéticos (se necessário)
python3 scripts/generate_data.py #JA TEMOS!!!

# 2. Enviar dados para o ThingsBoard
python3 scripts/ingest_data.py
```

### 3. Acessar Dashboards
- **ThingsBoard**: http://localhost:8080
  - **Login**: tenant@thingsboard.org
  - **Senha**: tenant
- **Trendz**: http://localhost:8888

## 📂 Estrutura do Projeto
- `app/`: Código fonte da API FastAPI
  - `routers/`: Endpoints da API (predição, thermal, dashboard)
  - `services/`: Serviços (predição ML, database, storage)
- `data/`: Dados brutos e processados (~26k registros)
- `docs/`: Documentação detalhada
  - `PREDICTION_API.md`: Documentação completa da API de predição
  - `QUICKSTART_PREDICTION.md`: Guia rápido de uso
  - `SUMMARY_PREDICTION.md`: Resumo da implementação
- `notebooks/`: Notebooks Jupyter para análise
  - `train_prediction_models.ipynb`: Treinamento de modelos ML
  - `pipeline_ml.ipynb`: Pipeline completo
- `scripts/`: Scripts de automação
  - `quickstart.py`: 🚀 Inicialização automática
  - `test_prediction_api.py`: Testes da API
  - `generate_data.py`: Geração de dados sintéticos
  - `ingest_data.py`: Ingestão para ThingsBoard
- `legacy/`: Arquivos antigos/descontinuados

## 📚 Documentação

### 🔮 Sistema de Predição
- **[API Completa](docs/PREDICTION_API.md)**: Documentação detalhada de todos os endpoints
- **[Quick Start](docs/QUICKSTART_PREDICTION.md)**: Guia rápido de uso
- **[Resumo](docs/SUMMARY_PREDICTION.md)**: Visão geral da implementação

### 📊 Endpoints Principais
- `GET /docs` - Documentação Swagger interativa
- `POST /prediction/predict` - Predição única
- `POST /prediction/predict/batch` - Predição em lote
- `POST /prediction/train` - Treinar modelos
- `GET /prediction/models` - Listar modelos disponíveis

### 🧪 Testes
```bash
# Teste completo da API
python scripts/test_prediction_api.py

# Quick start automatizado
python scripts/quickstart.py
```

## 🛠️ Solução de Problemas

### Modelos ML não encontrados
```bash
curl -X POST "http://localhost:8060/prediction/train"
```

### Gráficos ThingsBoard vazios
1. Verifique se o script `scripts/ingest_data.py` foi executado com sucesso.
2. Verifique se o dispositivo "Sensor Térmico 01" foi criado no ThingsBoard.
3. Certifique-se de que os widgets do dashboard estão configurados para usar a fonte de dados correta (Entity alias).

### Erro de conexão com serviços
```bash
# Ver status dos containers
docker-compose ps

# Ver logs
docker-compose logs app mlflow

# Reiniciar serviços
docker-compose restart app mlflow
```

