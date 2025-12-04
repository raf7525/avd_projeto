# ✅ Checklist de Validação de Requisitos - Projeto AVD

Este documento valida o status atual do projeto em relação à especificação oficial: `[CESAR School] - AVD - Especificação de Projeto.md`.

---

## 1. Arquitetura e Infraestrutura (Seção 4)
*Requisito: O projeto deve rodar em contêineres via Docker Compose com serviços obrigatórios.*

| Status | Requisito | Detalhes |
| :---: | --- | --- |
| ✅ | **Docker Compose** | Arquivo `docker-compose.yml` funcional e completo. |
| ✅ | **FastAPI (Ingestão)** | Configurado na porta `8060`. |
| ✅ | **MinIO (S3)** | Armazenamento de objetos brutos (Portas `9000/9001`). |
| ✅ | **Banco Estruturado** | PostgreSQL configurado na porta `5433` (Substituto válido para Snowflake). |
| ✅ | **Jupyter Notebook** | Ambiente de análise configurado na porta `1010`. |
| ✅ | **MLflow** | Servidor de rastreamento de modelos na porta `5000`. |
| ✅ | **Visualização** | ThingsBoard (`8080`) e Trendz (`8888`) configurados. |

## 2. Fluxo de Dados (Seção 1 e 4)
*Requisito: Pipeline completo de ponta a ponta.*

| Status | Requisito | Detalhes |
| :---: | --- | --- |
| ✅ | **Coleta de Dados** | Script `scripts/convert_inmet_data.py` converte dados brutos. |
| ✅ | **Ingestão** | Script `scripts/ingest_data.py` envia para API e ThingsBoard. |
| ✅ | **Armazenamento Bruto** | API salva JSONs no bucket `avd-raw-data` (MinIO). |
| ✅ | **Armazenamento Estruturado** | API salva dados processados no PostgreSQL. |
| ✅ | **Treinamento ML** | Notebooks consomem dados e treinam modelos. |
| ✅ | **Registro de Modelo** | Integração com MLflow funcional. |
| ✅ | **Consumo de Modelo** | Endpoint `/prediction/predict` exposto para dashboards. |

## 3. Escopo do Problema (Seção 7)
*Requisito: Resolver 1 dos 10 problemas propostos.*

| Status | Requisito | Detalhes |
| :---: | --- | --- |
| ✅ | **Problema Escolhido** | **7.10** (Prever Sensação Térmica) e **7.5** (Classificar Níveis de Conforto Térmico). |
| ✅ | **Variáveis** | Temp, Umidade, Vento, Pressão, Radiação. |
| ✅ | **Modelagem** | Random Forest e Gradient Boosting implementados. |

## 4. Entregáveis Obrigatórios (Seção 6)
*Requisito: Itens físicos que devem constar no repositório.*

| Status | Requisito | Detalhes |
| :---: | --- | --- |
| ✅ | **Código Fonte** | `app/`, `scripts/`, `notebooks/` presentes. |
| ✅ | **Docker Compose** | Presente na raiz. |
| ✅ | **README.md** | Estruturado conforme a Seção 5. |
| ❌ | **Membros da Equipe** | **PENDENTE:** Faltam nomes e usuários GitHub no README. |
| ❌ | **Relatório Técnico (PDF)** | **CRÍTICO:** Pasta `reports/` está vazia. Necessário PDF detalhado. |
| ✅ | **Dashboard Online** | Infraestrutura OK e scripts de configuração (`setup-trendz.sh`) disponíveis. |

## 5. Estrutura de Pastas (Seção 5)
*Requisito: Seguir a organização sugerida.*

| Status | Pasta/Arquivo | Observação |
| :---: | --- | --- |
| ✅ | `/docker-compose.yml` | OK |
| ✅ | `/notebooks` | OK |
| ✅ | `/reports` | Pasta existe, mas vazia. |
| ✅ | `/app` | Equivalente a `/fastapi`. |
| ✅ | `/trendz` | Configurações presentes. |
| ✅ | `/mlflow` | Configurado via Docker. |
| ✅ | `/data` | Dados brutos e processados. |
| ✅ | `/db_init` | Scripts de inicialização do banco. |

## 6. Scripts Utilitários
*Requisito: Ferramentas para facilitar a execução e manutenção.*

| Status | Script | Função |
| :---: | --- | --- |
| ✅ | `convert_inmet_data.py` | Prepara dados brutos do INMET. |
| ✅ | `ingest_data.py` | Envia dados para o sistema. |
| ✅ | `init_tables.py` | Cria tabelas no PostgreSQL. |
| ✅ | `check_dashboard.py` | Valida dados no ThingsBoard. |
| ✅ | `setup-trendz.sh` | Configura dashboards automaticamente. |
| ✅ | `quickstart.py` | Assistente de inicialização interativo. |

---

## 🚨 Ações Imediatas Necessárias

1.  **Preencher Membros:** Editar o `README.md` com os nomes e usuários do Github.
2.  **Criar Relatório Técnico:** Escrever o documento explicativo, gerar o PDF com prints e salvar em `reports/`.