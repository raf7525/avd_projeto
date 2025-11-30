# 🌡️ Projeto AVD - Análise e Visualização de Dados

## 🎯 Objetivo
**Prever Sensação Térmica**
Desenvolver sistema de previsão de sensação térmica e classificação de zonas de conforto baseado em dados meteorológicos históricos.

## 🏗️ Arquitetura
- **FastAPI**: Ingestão e API de dados (Porta 8060)
- **Jupyter Notebook**: Análise e Modelagem (Porta 1010)
- **MLflow**: Versionamento de Modelos (Porta 5000)
- **ThingsBoard**: Visualização IoT (Porta 8080)
- **Trendz Analytics**: Analytics Avançado (Porta 8888)
- **MinIO**: Armazenamento de Objetos (S3) (Porta 9000/9001)
- **PostgreSQL**: Banco de Dados Relacional

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
- `data/`: Dados brutos e processados
- `docs/`: Documentação detalhada
- `notebooks/`: Notebooks Jupyter para análise
- `scripts/`: Scripts de automação (ingestão, geração de dados)
- `legacy/`: Arquivos antigos/descontinuados

## 🛠️ Solução de Problemas
Se os gráficos no ThingsBoard estiverem vazios:
1. Verifique se o script `scripts/ingest_data.py` foi executado com sucesso.
2. Verifique se o dispositivo "Sensor Térmico 01" foi criado no ThingsBoard.
3. Certifique-se de que os widgets do dashboard estão configurados para usar a fonte de dados correta (Entity alias).

