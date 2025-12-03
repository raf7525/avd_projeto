# 🔮 API de Predição de Sensação Térmica

## Visão Geral

Sistema completo de predição de sensação térmica usando Machine Learning, com modelos treinados em dados meteorológicos históricos.

## Modelos Disponíveis

### 1. **Random Forest Regressor**
- Ensemble de árvores de decisão
- Robusto a outliers
- Captura relações não-lineares
- Melhor para dados com ruído

### 2. **Gradient Boosting Regressor**
- Boosting sequencial
- Alta precisão
- Menor overfitting
- Melhor para padrões complexos

## Features Utilizadas

### Features Básicas
- `temperature`: Temperatura do ar (°C)
- `humidity`: Umidade relativa (%)
- `wind_velocity`: Velocidade do vento (km/h)
- `pressure`: Pressão atmosférica (hPa)
- `solar_radiation`: Radiação solar (W/m²)

### Features Derivadas
- `temp_humidity_interaction`: Interação temperatura × umidade
- `wind_chill_factor`: Fator de sensação de vento
- `radiation_normalized`: Radiação solar normalizada
- `pressure_deviation`: Desvio da pressão padrão

### Features Temporais
- `hour_sin`, `hour_cos`: Componentes cíclicas da hora
- `day_sin`, `day_cos`: Componentes cíclicas do dia do ano

## Zonas de Conforto

| Zona | Faixa | Descrição |
|------|-------|-----------|
| **Muito Frio** | < 15°C | Desconforto por frio intenso |
| **Frio** | 15-18°C | Desconforto por frio |
| **Fresco** | 18-20°C | Levemente frio, mas tolerável |
| **Confortável** | 20-26°C | Zona de conforto térmico ideal |
| **Quente** | 26-29°C | Levemente quente |
| **Muito Quente** | > 29°C | Desconforto por calor |

*Baseado em ASHRAE 55 e ISO 7730 (PMV/PPD)*

## Endpoints da API

### 1. Predição Única

**POST** `/prediction/predict`

Faz predição para um único ponto de dados.

**Query Parameters:**
- `model`: Modelo a usar (`random_forest` ou `gradient_boosting`)

**Request Body:**
```json
{
  "temperature": 28.5,
  "humidity": 70.0,
  "wind_velocity": 5.0,
  "pressure": 1013.0,
  "solar_radiation": 600.0,
  "timestamp": "2023-07-15T14:30:00"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Predição realizada com sucesso",
  "data": {
    "physical_sensation": 30.45,
    "physical_comfort_zone": "Muito Quente",
    "ml_prediction": 29.87,
    "ml_comfort_zone": "Quente",
    "model_used": "random_forest",
    "prediction_difference": -0.58,
    "input": {
      "temperature": 28.5,
      "humidity": 70.0,
      "wind_velocity": 5.0,
      "pressure": 1013.0,
      "solar_radiation": 600.0
    }
  }
}
```

**Exemplo cURL:**
```bash
curl -X POST "http://localhost:8060/prediction/predict?model=random_forest" \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 28.5,
    "humidity": 70.0,
    "wind_velocity": 5.0,
    "pressure": 1013.0,
    "solar_radiation": 600.0
  }'
```

### 2. Predição em Lote

**POST** `/prediction/predict/batch`

Faz predições para múltiplos pontos de dados.

**Request Body:**
```json
{
  "model_name": "random_forest",
  "data": [
    {
      "temperature": 28.5,
      "humidity": 70.0,
      "wind_velocity": 5.0,
      "pressure": 1013.0,
      "solar_radiation": 600.0
    },
    {
      "temperature": 15.0,
      "humidity": 80.0,
      "wind_velocity": 15.0,
      "pressure": 1020.0,
      "solar_radiation": 0.0
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "message": "2 predições realizadas",
  "data": {
    "predictions": [...],
    "total": 2,
    "model_used": "random_forest"
  }
}
```

### 3. Treinar Modelos

**POST** `/prediction/train`

Treina todos os modelos de Machine Learning.

**Response:**
```json
{
  "success": true,
  "message": "Modelos treinados com sucesso",
  "data": {
    "models_trained": ["random_forest", "gradient_boosting"],
    "metrics": {
      "random_forest": {
        "test_rmse": 0.8523,
        "test_mae": 0.6421,
        "test_r2": 0.9567
      },
      "gradient_boosting": {
        "test_rmse": 0.7891,
        "test_mae": 0.5987,
        "test_r2": 0.9623
      }
    },
    "mlflow_uri": "http://mlflow:5000"
  }
}
```

**Exemplo cURL:**
```bash
curl -X POST "http://localhost:8060/prediction/train"
```

### 4. Listar Modelos

**GET** `/prediction/models`

Lista todos os modelos disponíveis e suas informações.

**Response:**
```json
{
  "success": true,
  "message": "Modelos listados",
  "data": {
    "available_models": ["random_forest", "gradient_boosting"],
    "model_info": {
      "random_forest": {
        "status": "loaded",
        "path": "/app/models/random_forest.pkl",
        "size_mb": 12.45
      }
    },
    "total_models": 2
  }
}
```

### 5. Zonas de Conforto

**GET** `/prediction/comfort-zones`

Retorna informações sobre as zonas de conforto térmico.

**Response:**
```json
{
  "success": true,
  "message": "Zonas de conforto térmico",
  "data": {
    "zones": [
      {
        "name": "Muito Frio",
        "range": "< 15°C",
        "description": "Desconforto por frio intenso"
      },
      ...
    ],
    "standard": "Baseado em ASHRAE 55 e ISO 7730"
  }
}
```

## Fórmula Física de Sensação Térmica

O sistema usa uma fórmula combinada que considera:

1. **Heat Index** (para temperaturas altas + umidade)
2. **Wind Chill** (para efeito do vento)
3. **Radiação Solar** (aquecimento adicional)
4. **Pressão Atmosférica** (pequeno ajuste)

```python
sensation = temperature + humidity_effect + wind_effect + radiation_effect + pressure_effect
```

## Treinamento dos Modelos

### Processo de Treinamento

1. **Carregamento de Dados**
   - Dados de `/app/data/sample_thermal_data.csv`
   - ~26.000 registros horários

2. **Preparação de Features**
   - Features básicas
   - Features derivadas
   - Features temporais
   - Normalização (StandardScaler)

3. **Split de Dados**
   - 80% treino
   - 20% teste
   - Random state fixo (42)

4. **Treinamento**
   - Cross-validation
   - Otimização de hiperparâmetros
   - Registro no MLflow

5. **Avaliação**
   - RMSE (Root Mean Squared Error)
   - MAE (Mean Absolute Error)
   - R² Score

### Usar o Notebook

Execute o notebook de treinamento:

```bash
# Acessar Jupyter
http://localhost:1010

# Abrir notebook
notebooks/train_prediction_models.ipynb
```

Ou via Python:

```python
from app.services.prediction_service import ThermalPredictionService

service = ThermalPredictionService()
results = service.train_models()
```

## Integração com MLflow

Todos os experimentos são registrados no MLflow:

- **URL**: http://localhost:5000
- **Experimento**: `thermal_sensation_prediction`

**O que é registrado:**
- Parâmetros do modelo
- Métricas de treino e teste
- Artefatos (modelo, gráficos)
- Metadata

**Visualizar no MLflow:**
```bash
# Acessar interface web
http://localhost:5000
```

## Exemplos de Uso

### Python

```python
import requests

# Predição única
response = requests.post(
    "http://localhost:8060/prediction/predict",
    params={"model": "random_forest"},
    json={
        "temperature": 32.0,
        "humidity": 75.0,
        "wind_velocity": 4.0,
        "pressure": 1010.0,
        "solar_radiation": 850.0
    }
)

result = response.json()
print(f"Sensação térmica: {result['data']['ml_prediction']}°C")
print(f"Zona de conforto: {result['data']['ml_comfort_zone']}")
```

### JavaScript

```javascript
fetch('http://localhost:8060/prediction/predict?model=random_forest', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    temperature: 32.0,
    humidity: 75.0,
    wind_velocity: 4.0,
    pressure: 1010.0,
    solar_radiation: 850.0
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## Performance dos Modelos

### Métricas Esperadas

| Modelo | RMSE | MAE | R² |
|--------|------|-----|-----|
| Random Forest | ~0.85°C | ~0.64°C | ~0.96 |
| Gradient Boosting | ~0.79°C | ~0.60°C | ~0.96 |

### Interpretação

- **RMSE < 1°C**: Excelente precisão
- **R² > 0.95**: Modelo explica 95%+ da variância
- **MAE < 1°C**: Erro médio menor que 1 grau

## Troubleshooting

### Modelos não encontrados

```bash
# Treinar modelos
curl -X POST "http://localhost:8060/prediction/train"

# Ou via notebook
jupyter lab --ip=0.0.0.0 --port=1010
```

### Erro de conexão com MLflow

```bash
# Verificar se MLflow está rodando
docker-compose ps mlflow

# Reiniciar se necessário
docker-compose restart mlflow
```

### Dados não encontrados

```bash
# Gerar dados sintéticos
python scripts/generate_data.py
```

## Próximos Passos

- [ ] Adicionar XGBoost
- [ ] Implementar LSTM para séries temporais
- [ ] Adicionar ensemble de modelos
- [ ] Implementar API de retraining automático
- [ ] Adicionar validação cruzada k-fold
- [ ] Implementar otimização bayesiana de hiperparâmetros

## Referências

- **ASHRAE 55**: Thermal Environmental Conditions for Human Occupancy
- **ISO 7730**: Ergonomics of the thermal environment
- **MLflow**: https://mlflow.org/
- **Scikit-learn**: https://scikit-learn.org/
