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
| ✅ | **Coleta de Dados** | Script `ingest_data.py` simula coleta e envio. |
| ✅ | **Armazenamento Bruto** | API salva JSONs no bucket `avd-raw-data` (MinIO). |
| ✅ | **Armazenamento Estruturado** | API salva dados processados no PostgreSQL. |
| ✅ | **Treinamento ML** | Notebooks consomem dados e treinam modelos. |
| ✅ | **Registro de Modelo** | Integração com MLflow funcional. |
| ✅ | **Consumo de Modelo** | Endpoint `/prediction/predict` exposto para dashboards. |

## 3. Escopo do Problema (Seção 7)
*Requisito: Resolver 1 dos 10 problemas propostos.*

| Status | Requisito | Detalhes |
| :---: | --- | --- |
| ✅ | **Problema Escolhido** | **7.5** (Conforto Térmico) e **7.10** (Sensação Térmica). |
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
| ⚠️ | **Dashboard Online** | Infraestrutura OK, mas configuração visual (widgets) é manual. |

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

---

## 🚨 Ações Imediatas Necessárias

1.  **Preencher Membros:** Editar o `README.md` com os nomes e usuários do Github.
2.  **Criar Relatório Técnico:** Escrever o documento explicativo, gerar o PDF com prints e salvar em `reports/`.
3.  **Configurar Dashboard:** Acessar `localhost:8080` e criar os gráficos manualmente.
