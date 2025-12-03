# Projeto AVD - Pipeline de Dados Meteorológicos

**DISCIPLINA:** Análise e Visualização de Dados - 2025.2  
**INSTITUIÇÃO:** CESAR School  

## 👥 Equipe
* **Nome do Aluno 1** (@usuario_github)
* **Nome do Aluno 2** (@usuario_github)
* **Nome do Aluno 3** (@usuario_github)
* **Nome do Aluno 4** (@usuario_github)
* **Nome do Aluno 5** (@usuario_github)
* **Nome do Aluno 6** (@usuario_github)

---

## 📝 Descrição do Projeto

Este projeto implementa um pipeline completo de Business Intelligence (BI) e Machine Learning (ML) para análise de dados meteorológicos. O objetivo principal é coletar dados, armazená-los de forma estruturada e bruta, realizar tratamento, treinar modelos preditivos de **Sensação Térmica** e **Zonas de Conforto**, e visualizar os resultados em dashboards interativos.

### 🎯 Problema Solucionado (Seção 7.5 e 7.10)
O sistema resolve o problema de **Classificação de Níveis de Conforto Térmico** e **Previsão de Sensação Térmica**, permitindo identificar se o ambiente está "Frio", "Confortável" ou "Quente" com base em variáveis como temperatura, umidade e vento.

## 🏗️ Arquitetura e Fluxo de Dados

O projeto utiliza uma arquitetura baseada em microsserviços com Docker:

1. **Ingestão (FastAPI + Scripts):** Dados são gerados/coletados e enviados para a API (Porta 8060) e para o ThingsBoard.
2. **Armazenamento Bruto (MinIO/S3):** A API salva os dados brutos (JSON) em um bucket S3 (MinIO).
3. **Armazenamento Estruturado (PostgreSQL):** Os dados tratados são persistidos em banco relacional (substituindo Snowflake/SQLite para este ambiente).
4. **Processamento e ML (Jupyter + MLflow):** Notebooks consomem os dados, treinam modelos (Regressão/Classificação) e registram métricas/artefatos no MLflow (Porta 5000).
5. **Visualização (ThingsBoard + Trendz):** Dashboards consomem dados de telemetria e exibem gráficos históricos e predições.

| Serviço | Porta | Função |
|---------|-------|--------|
| **FastAPI** | 8060 | API de Ingestão e Predição |
| **ThingsBoard** | 8080 | Plataforma IoT e Dashboards |
| **Trendz** | 8888 | Analytics Avançado |
| **Jupyter** | 1010 | Ambiente de Desenvolvimento |
| **MLflow** | 5000 | Registro de Modelos |
| **MinIO** | 9000/9001 | Object Storage (S3 Compatible) |

## 🚀 Como Executar

### Pré-requisitos
- Docker e Docker Compose instalados.
- Git instalado.

### Passo a Passo

1. **Clonar o Repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd avd_projeto
   ```

2. **Iniciar a Infraestrutura:**
   O script abaixo levanta todos os containers necessários.
   ```bash
   docker-compose up --build -d
   ```
   *Aguarde alguns minutos para que todos os serviços (especialmente ThingsBoard e Postgres) inicializem completamente.*

3. **Gerar e Ingerir Dados:**
   Execute os scripts para popular o banco de dados e o ThingsBoard.
   ```bash
   # Instalar dependências locais dos scripts (opcional, se rodar fora do container)
   pip install -r requirements.txt

   # 1. Gerar dados sintéticos
   python3 scripts/generate_data.py

   # 2. Ingerir dados na API e ThingsBoard
   python3 scripts/ingest_data.py
   ```

4. **Treinar o Modelo de ML:**
   Você pode treinar o modelo via API ou via Jupyter.
   
   **Via API:**
   ```bash
   curl -X POST "http://localhost:8060/prediction/train"
   ```

   **Via Jupyter:**
   - Acesse `http://localhost:1010` (Token pode ser visto nos logs: `docker-compose logs app`)
   - Abra `notebooks/pipeline_ml.ipynb` e execute as células.

5. **Acessar os Dashboards:**
   - **ThingsBoard:** Acesse `http://localhost:8080`
     - **Login:** `tenant@thingsboard.org`
     - **Senha:** `tenant`
   - **MLflow:** Acesse `http://localhost:5000` para ver os modelos registrados.
   - **MinIO:** Acesse `http://localhost:9001` (User/Pass: `minioadmin`) para ver os arquivos no bucket `avd-raw-data`.

## 📂 Estrutura do Repositório

```
/
├── app/                 # Código fonte da aplicação (FastAPI)
│   ├── main.py          # Entrypoint da API
│   ├── routers/         # Rotas da API
│   └── services/        # Lógica de negócios e integrações
├── data/                # Dados locais (CSV/JSON)
├── docs/                # Documentação complementar
├── notebooks/           # Notebooks para análise e treino
├── reports/             # Relatórios PDF e imagens
├── scripts/             # Scripts auxiliares (ingestão, setup)
├── trendz/              # Configurações do Trendz
├── docker-compose.yml   # Definição dos serviços
└── README.md            # Este arquivo
```

## 🧪 Testes e Verificação

Para verificar se a API de predição está funcionando:

```bash
# Teste de predição única
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

