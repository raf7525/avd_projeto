# 🌦️ Projeto AVD - Sistema de Predição de Sensação Térmica

![Python](https://img.shields.io/badge/python-3.11-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Docker](https://img.shields.io/badge/docker-24.0-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-15.0-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![MLflow](https://img.shields.io/badge/mlflow-2.8-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.3-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![ThingsBoard](https://img.shields.io/badge/ThingsBoard-CE-26619C?style=for-the-badge&logo=thingsboard&logoColor=white)

**DISCIPLINA:** Análise e Visualização de Dados - 2025.2  
**INSTITUIÇÃO:** CESAR School  

## 👥 Equipe
* [![ticogafa](https://img.shields.io/badge/ticogafa-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ticogafa) - **Tiago Gurgel**
* [![raf7525](https://img.shields.io/badge/raf7525-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/raf7525) - **Rafael Leite**
* [![MigueldsBatista](https://img.shields.io/badge/MigueldsBatista-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/MigueldsBatista) - **Miguel Batista**

---

## 📖 Sobre o Projeto

Este projeto implementa um pipeline completo de **IoT, Business Intelligence (BI) e Machine Learning (ML)** para monitoramento e predição de **Sensação Térmica**. O sistema coleta dados meteorológicos simulados, armazena-os em um Data Lake, processa-os para treinar modelos de ML e disponibiliza visualizações em tempo real via dashboards.

O objetivo central é ir além da temperatura bruta e calcular o **Conforto Térmico Humano**, classificando o ambiente em zonas como "Confortável", "Muito Quente" ou "Frio" usando normas internacionais (ASHRAE 55 / ISO 7730).

---

## 🚀 Quick Start (Início Rápido)

Para rodar todo o ecossistema (Banco de dados, API, MLflow, ThingsBoard, etc) com um único comando:

### 1. Iniciar o Ambiente
```bash
# Opção recomendada (Script de automação)
./scripts/docker-manager.sh start

# OU via Docker Compose tradicional
docker-compose up -d --build
```
*Aguarde cerca de 30-60 segundos para que todos os serviços (especialmente ThingsBoard) inicializem.*

### 2. Verificar Status
```bash
docker-compose ps
```

### 3. Acessar a Aplicação
Abra seu navegador em: **[http://localhost:8060/docs](http://localhost:8060/docs)** para ver a API Swagger.

---

## 🧠 Modelos de Machine Learning

O sistema utiliza dois modelos de regressão robustos para prever a sensação térmica com base em variáveis ambientais.

### 1. Random Forest Regressor
*   **O que é:** Um modelo de "ensemble" que cria centenas de árvores de decisão durante o treinamento e retorna a média das previsões das árvores individuais.
*   **Por que usamos:** É excelente para lidar com relações não-lineares e robusto contra "overfitting" (ajuste excessivo aos dados de treino).
*   **Configuração:**
    *   `n_estimators`: 200 (número de árvores)
    *   `max_depth`: 20 (profundidade máxima)
    *   **Performance Esperada:** RMSE ~0.85°C, R² ~0.96

### 2. Gradient Boosting Regressor
*   **O que é:** Uma técnica que constrói modelos de forma sequencial, onde cada novo modelo tenta corrigir os erros do anterior.
*   **Por que usamos:** Frequentemente oferece a maior precisão possível em dados tabulares estruturados.
*   **Configuração:**
    *   `n_estimators`: 200
    *   `learning_rate`: 0.1
    *   **Performance Esperada:** RMSE ~0.79°C, R² ~0.96

### 🌡️ Zonas de Conforto (ASHRAE 55)
Além da predição numérica, o sistema classifica o resultado em 6 zonas:
1.  🔵 **Muito Frio:** < 15°C
2.  ❄️ **Frio:** 15-18°C
3.  🍃 **Fresco:** 18-20°C
4.  ✅ **Confortável:** 20-26°C (Meta ideal)
5.  ⚠️ **Quente:** 26-29°C
6.  🔴 **Muito Quente:** > 29°C

---

## 🛠️ Tecnologias e Bibliotecas

*   **[FastAPI](https://fastapi.tiangolo.com/):** Framework moderno e de alta performance para construção de APIs com Python 3.11+. Usado para servir os modelos de ML e ingerir dados.
*   **[MLflow](https://mlflow.org/):** Plataforma para ciclo de vida de ML. Usado para rastrear experimentos, registrar parâmetros, métricas e versionar os modelos treinados (`.pkl`).
*   **[Scikit-Learn](https://scikit-learn.org/):** Biblioteca de aprendizado de máquina. Fornece as implementações de RandomForest, GradientBoosting e ferramentas de pré-processamento (`StandardScaler`).
*   **[ThingsBoard](https://thingsboard.io/):** Plataforma IoT open-source. Usada para visualização de telemetria em tempo real e criação de dashboards complexos.
*   **[Trendz Analytics](https://thingsboard.io/products/trendz/):** Ferramenta de BI conectada ao ThingsBoard para análises preditivas e de negócios avançadas.
*   **[MinIO](https://min.io/):** Armazenamento de objetos compatível com S3. Usado como Data Lake (Bronze Layer) e armazenamento de artefatos do MLflow.

---

## 🖥️ Guia de Interfaces (Onde Clicar)

### 1. ThingsBoard (IoT Dashboards)
*   **URL:** [http://localhost:8080](http://localhost:8080)
*   **Login:** `tenant@thingsboard.org`
*   **Senha:** `tenant`
*   **Como Criar Dashboard:**
    1.  Vá em **"Dashboards"** no menu lateral esquerdo.
    2.  Clique no botão **"+"** (Add Dashboard) > "Create new dashboard".
    3.  Dê um nome (ex: "Monitoramento Térmico").
    4.  Abra o dashboard e clique no **Lápis Laranja** (canto inferior direito) para editar.
    5.  Clique em **"Add new widget"** para adicionar gráficos (Charts) ou mostradores (Gauges).
    6.  Selecione o dispositivo "Sensor Térmico AVD" como fonte de dados.

*   **⚠️ IMPORTANTE - Configuração de Alias:**
    *   **Antes de criar widgets**, você deve configurar um **alias** no dashboard para referenciar o dispositivo "Sensor Térmico 01".
    *   No modo de edição do dashboard (lápis laranja), clique em **"Entity aliases"** (ícone de engrenagem no canto superior direito).
    *   Crie um novo alias (ex: "SensorINMET") do tipo **"Single entity"** e selecione o dispositivo "Sensor Térmico 01".
    *   **Sem esta configuração, os widgets não conseguirão mostrar os dados!**
    *   Ao adicionar widgets, use este alias como fonte de dados ao invés de selecionar o dispositivo diretamente.

### 2. MLflow (Tracking de ML)
*   **URL:** [http://localhost:5000](http://localhost:5000)
*   **O que ver:**
    1.  Na tela inicial, clique no experimento `thermal_sensation_prediction` na barra lateral.
    2.  Você verá uma tabela com todas as execuções ("Runs").
    3.  Clique em uma execução para ver os **Parâmetros** (n_estimators, learning_rate), **Métricas** (RMSE, MAE) e **Artefatos** (o modelo salvo).

### 3. API Swagger (Documentação Interativa)
*   **URL:** [http://localhost:8060/docs](http://localhost:8060/docs)
*   **Como usar:**
    1.  Esta interface lista todos os endpoints disponíveis (`POST /prediction/predict`, `POST /prediction/train`, etc.).
    2.  Clique em um endpoint para expandir.
    3.  Clique em **"Try it out"**, preencha o JSON de exemplo e clique em **"Execute"** para testar a API diretamente do navegador.

### 4. Trendz Analytics (BI Avançado)
*   **URL:** [http://localhost:8888](http://localhost:8888)
*   **Login:** Mesmo do ThingsBoard (`tenant@thingsboard.org` / `tenant`).
*   **O que fazer:** Conectar ao ThingsBoard para gerar mapas de calor e previsões de tendências futuras baseadas nos dados históricos armazenados.

### 5. MinIO (Data Lake)
*   **URL:** [http://localhost:9001](http://localhost:9001)
*   **Login:** `minioadmin` / `minioadmin`
*   **O que ver:** Navegue pelos "Buckets" para ver os dados brutos (json) salvos pela API ou os artefatos de modelos do MLflow.

---

## 🕹️ Comandos de Execução e Uso

### Treinar os Modelos
Para treinar (ou retreinar) os modelos com os dados disponíveis no banco:
```bash
curl -X POST "http://localhost:8060/prediction/train"
```
*Resposta esperada: JSON com métricas de performance (RMSE, MAE) dos modelos treinados.*

### Fazer uma Predição (Teste)
Envie dados climáticos para receber a sensação térmica e a zona de conforto:
```bash
curl -X POST "http://localhost:8060/prediction/predict?model=random_forest" \
  -H "Content-Type: application/json" \
  -d '{'\
    "temperature": 32.5,
    "humidity": 60.0,
    "wind_velocity": 3.0,
    "pressure": 1012.0,
    "solar_radiation": 800.0
  }'
```

---

## 🛠️ Scripts Utilitários

Aqui estão alguns scripts úteis para gerenciar o projeto e seus dados:

### Preparar Dados
Se o banco estiver vazio, prepare e ingira os dados:
```bash
# 1. Converter dados do INMET (certifique-se que inmet.csv está na raiz do projeto)
docker-compose exec app python scripts/convert_inmet_data.py

# 2. Ingerir no Banco de Dados (PostgreSQL) e ThingsBoard
docker-compose exec app python scripts/ingest_data.py
```

### Inicializar Tabelas do Banco de Dados
Este script cria as tabelas necessárias no PostgreSQL (para o banco de dados `avd_wind_data`) caso não existam. Isso é útil se o volume do PostgreSQL for reiniciado.
```bash
docker-compose exec app python scripts/init_tables.py
```

### Verificar Dados no ThingsBoard
Use este script para verificar se os dados estão sendo enviados corretamente para o ThingsBoard antes de criar dashboards.
```bash
docker-compose exec app python scripts/check_dashboard.py
```

### Configurar Dashboards do Trendz Analytics
Este script automatiza a configuração inicial do Trendz, incluindo a criação de dashboards de exemplo.
```bash
./scripts/setup-trendz.sh
```

### Quick Start Interativo
Para uma inicialização guiada e interativa que abrange o início dos serviços, treinamento de modelos e teste de predição:
```bash
python scripts/quickstart.py
```

---

## 📂 Estrutura de Pastas Importantes

```
/
├── app/
│   ├── models/          # Definição dos schemas Pydantic
│   ├── routers/         # Endpoints da API (prediction.py, etc)
│   └── services/        # Lógica ML (prediction_service.py)
├── data/                # Dados CSV/JSON locais
├── docs/                # Documentação detalhada (Manuais, Guias)
├── notebooks/           # Jupyter Notebooks para experimentação
├── scripts/             # Scripts de automação (geração de dados, setup)
├── trendz/              # Configurações de dashboards Trendz
├── docker-compose.yml   # Orquestração dos containers
└── README.md            # Este guia
```

## 📚 Referências
*   **ASHRAE Standard 55:** Thermal Environmental Conditions for Human Occupancy.
*   **ISO 7730:** Ergonomics of the thermal environment.
*   **NOAA:** Fórmulas de Heat Index e Wind Chill.

---