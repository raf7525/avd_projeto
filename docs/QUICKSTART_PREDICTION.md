# 🚀 Guia Rápido - Sistema de Predição de Sensação Térmica

## ⚡ Início Rápido

### 1. Iniciar o Sistema

```bash
# Subir todos os serviços
docker-compose up --build

# Aguardar até que todos os serviços estejam rodando
# API estará disponível em: http://localhost:8060
# MLflow em: http://localhost:5000
# Jupyter em: http://localhost:1010
```

### 2. Treinar os Modelos

**Opção A: Via API**
```bash
curl -X POST "http://localhost:8060/prediction/train"
```

**Opção B: Via Script Python**
```bash
python scripts/test_prediction_api.py
# Selecione a opção de treinar modelos
```

**Opção C: Via Notebook Jupyter**
```bash
# Acessar: http://localhost:1010
# Abrir: notebooks/train_prediction_models.ipynb
# Executar todas as células
```

### 3. Fazer uma Predição

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

**Resposta:**
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
    "prediction_difference": -0.58
  }
}
```

## 📊 Endpoints Principais

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/prediction/predict` | POST | Predição única |
| `/prediction/predict/batch` | POST | Predição em lote |
| `/prediction/train` | POST | Treinar modelos |
| `/prediction/models` | GET | Listar modelos |
| `/prediction/comfort-zones` | GET | Info zonas de conforto |

## 🎯 Casos de Uso

### 1. Análise em Tempo Real

```python
import requests

def analyze_current_weather():
    response = requests.post(
        "http://localhost:8060/prediction/predict",
        json={
            "temperature": 28.5,
            "humidity": 70.0,
            "wind_velocity": 5.0,
            "pressure": 1013.0,
            "solar_radiation": 600.0
        }
    )
    return response.json()
```

### 2. Análise Histórica em Lote

```python
import pandas as pd
import requests

# Carregar dados históricos
df = pd.read_csv("data/sample_thermal_data.csv")

# Preparar batch
batch = {
    "model_name": "random_forest",
    "data": df[['temperature', 'humidity', 'wind_velocity', 
                'pressure', 'solar_radiation']].to_dict('records')
}

# Fazer predição
response = requests.post(
    "http://localhost:8060/prediction/predict/batch",
    json=batch
)
```

### 3. Integração com Dashboard

```javascript
// Buscar predição e atualizar dashboard
async function updateThermalDashboard(sensorData) {
  const response = await fetch(
    'http://localhost:8060/prediction/predict',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(sensorData)
    }
  );
  
  const result = await response.json();
  updateUI(result.data);
}
```

## 🔧 Troubleshooting

### Problema: Modelos não encontrados

```bash
# Solução: Treinar os modelos
curl -X POST "http://localhost:8060/prediction/train"
```

### Problema: Erro de conexão

```bash
# Verificar se serviços estão rodando
docker-compose ps

# Reiniciar se necessário
docker-compose restart app mlflow
```

### Problema: Erro no treinamento

```bash
# Verificar logs
docker-compose logs app

# Verificar se dados existem
ls -lh data/sample_thermal_data.csv

# Gerar dados se necessário
docker-compose exec app python scripts/generate_data.py
```

## 📈 Monitoramento

### Ver Experimentos no MLflow

```bash
# Acessar: http://localhost:5000
# - Ver runs de treinamento
# - Comparar métricas
# - Baixar modelos
```

### Ver Logs em Tempo Real

```bash
# Logs da aplicação
docker-compose logs -f app

# Logs do MLflow
docker-compose logs -f mlflow
```

## 🎓 Modelos Disponíveis

### Random Forest
- **Tipo**: Ensemble de árvores
- **Vantagens**: Robusto, rápido, bom para dados com ruído
- **Uso**: Predições em produção

### Gradient Boosting
- **Tipo**: Boosting sequencial
- **Vantagens**: Alta precisão, captura padrões complexos
- **Uso**: Análises detalhadas

## 🌡️ Zonas de Conforto

| Zona | Faixa | Ação Recomendada |
|------|-------|------------------|
| Muito Frio | < 15°C | Aquecimento necessário |
| Frio | 15-18°C | Aquecimento leve |
| Fresco | 18-20°C | Conforto aceitável |
| Confortável | 20-26°C | ✅ Zona ideal |
| Quente | 26-29°C | Ventilação recomendada |
| Muito Quente | > 29°C | Refrigeração necessária |

## 🔬 Features Utilizadas

### Básicas
- Temperatura (°C)
- Umidade (%)
- Velocidade do vento (km/h)
- Pressão atmosférica (hPa)
- Radiação solar (W/m²)

### Derivadas
- Interação temperatura × umidade
- Fator de wind chill
- Radiação normalizada
- Desvio de pressão

### Temporais
- Hora do dia (componentes sen/cos)
- Dia do ano (componentes sen/cos)

## 📚 Documentação Completa

- **API Detalhada**: [docs/PREDICTION_API.md](./PREDICTION_API.md)
- **Swagger UI**: http://localhost:8060/docs
- **ReDoc**: http://localhost:8060/redoc

## 🧪 Testes

```bash
# Executar suite de testes
python scripts/test_prediction_api.py

# Testes individuais
pytest tests/test_prediction.py -v

# Coverage
pytest --cov=app tests/
```

## 🚀 Performance

### Tempo de Resposta
- Predição única: ~50ms
- Predição batch (100 pontos): ~500ms
- Treinamento completo: ~2-5 min

### Precisão
- RMSE: < 1°C
- MAE: < 0.7°C
- R²: > 0.95

## 💡 Dicas

1. **Treinar periodicamente**: Retreine modelos com novos dados
2. **Usar batch para histórico**: Mais eficiente que múltiplas chamadas
3. **Escolher modelo adequado**: Random Forest para produção, GB para análise
4. **Monitorar MLflow**: Acompanhe drift de modelo
5. **Validar entrada**: Verifique ranges de valores

## 🔗 Links Úteis

- API Swagger: http://localhost:8060/docs
- MLflow UI: http://localhost:5000
- Jupyter: http://localhost:1010
- PostgreSQL: localhost:5433
- MinIO: http://localhost:9001

## 📞 Suporte

Para questões técnicas, consulte:
- [Documentação completa](./PREDICTION_API.md)
- [Issues do projeto](https://github.com/seu-usuario/avd_projeto/issues)
- Logs: `docker-compose logs app`
