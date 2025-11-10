# 🌐 ThingsBoard + Trendz Analytics - Configuração

## O que são essas ferramentas?

### ThingsBoard
- **Plataforma IoT Open Source** para coleta, processamento e visualização de dados de sensores
- Ideal para dashboards em tempo real de dados de vento
- Suporta protocolos: MQTT, HTTP, CoAP, etc.

### Trendz Analytics  
- **Ferramenta de analytics** que se integra com ThingsBoard
- Análises avançadas, machine learning e business intelligence
- Perfeito para análise de padrões de vento ao longo do tempo

## 🎯 Como se relacionam com seu projeto

### Fluxo de Dados:
```
Dados de Vento → ThingsBoard → Trendz Analytics → Insights
     ↓              ↓              ↓
  Sensores      Dashboards     Padrões/ML
```

## 🚀 Configuração no Docker

### Portas configuradas:
- **ThingsBoard**: http://localhost:8080
- **Trendz Analytics**: http://localhost:8888
- **Jupyter**: http://localhost:1010  
- **FastAPI**: http://localhost:8060

### Primeiro acesso - ThingsBoard:
1. Acesse: http://localhost:8080
2. **Login padrão:**
   - Email: `tenant@thingsboard.org`
   - Senha: `tenant`

### Primeiro acesso - Trendz:
1. Acesse: http://localhost:8888
2. **Login inicial:** Será criado durante setup
3. Conecta automaticamente ao ThingsBoard

## 📊 Casos de Uso para Padrões de Vento

### No ThingsBoard:
- **Widgets em tempo real** de velocidade/direção do vento
- **Rosa dos ventos interativa**
- **Alertas** para condições extremas
- **Geolocalização** de sensores

### No Trendz Analytics:
- **Clustering** de padrões de vento
- **Análise temporal** (horário, sazonal)
- **Machine Learning** para previsão
- **Business Intelligence** sobre energia eólica

## 🛠️ Integração com o projeto

### 1. Dados de entrada
```python
# Exemplo de envio de dados para ThingsBoard
import requests

def send_wind_data(velocity, direction, timestamp):
    data = {
        "wind_velocity": velocity,
        "wind_direction": direction, 
        "timestamp": timestamp
    }
    response = requests.post(
        "http://localhost:8080/api/v1/{ACCESS_TOKEN}/telemetry",
        json=data
    )
```

### 2. Análise no Trendz
- Importar dados históricos
- Criar modelos de clustering
- Visualizar padrões sazonais
- Exportar insights para MLflow

## 🔗 Próximos passos

1. **Configurar dispositivos** no ThingsBoard
2. **Importar dados históricos** de vento
3. **Criar dashboards** de monitoramento
4. **Configurar analytics** no Trendz
5. **Integrar** com pipeline ML (MLflow + FastAPI)

## 💡 Dicas importantes

- ThingsBoard usa PostgreSQL para persistir dados
- Trendz se conecta automaticamente ao ThingsBoard
- Dados podem ser exportados via API REST
- Ideal para demonstrações em tempo real