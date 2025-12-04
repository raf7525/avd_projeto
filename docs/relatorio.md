# Pipeline de Dados Meteorológicos: Monitoramento e Previsão de Conforto Térmico

<center>
<b>ticogafa, raf7525, MigueldsBatista</b>
<br>
CESAR School – Análise e Visualização de Dados (2025.2)
<br>
Recife – PE – Brazil
<br>
<code>{@ticogafa, @raf7525, @MigueldsBatista}</code>
</center>

**Abstract.** *This project presents the development of an End-to-End Data Pipeline capable of ingesting, processing, storing, and analyzing real-time climatic data. The solution addresses specific challenges such as classifying thermal comfort levels and predicting thermal sensation using Machine Learning. The architecture utilizes containerized microservices (Docker), including FastAPI for ingestion, MinIO and PostgreSQL for storage, and MLflow for experiment tracking. Results show that the Gradient Boosting Regressor achieved an RMSE of 0.16°C. Final visualizations are provided via ThingsBoard.*

**Resumo.** *Este projeto apresenta o desenvolvimento de um Pipeline de Dados Completo (End-to-End) capaz de ingerir, processar, armazenar e analisar dados climáticos em tempo real. A solução aborda desafios específicos como a classificação de níveis de conforto térmico e a previsão de sensação térmica utilizando Machine Learning. A arquitetura utiliza microsserviços conteinerizados (Docker), incluindo FastAPI para ingestão, MinIO e PostgreSQL para armazenamento e MLflow para rastreamento de experimentos. Os resultados mostram que o modelo Gradient Boosting Regressor obteve um RMSE de 0.16°C. As visualizações finais são disponibilizadas via ThingsBoard.*

## 1. Introdução e Objetivos

A análise de dados meteorológicos é fundamental para diversos setores, desde a agricultura até o planejamento urbano. Este projeto tem como objetivo principal o desenvolvimento de um **Pipeline de Dados Completo (End-to-End)**, capaz de ingerir, processar, armazenar e analisar dados climáticos em tempo real.

O foco específico da análise recai sobre dois problemas da especificação:

1.  **Classificação de Níveis de Conforto Térmico:** Categorização do ambiente em zonas (ex: "Confortável", "Quente", "Frio").
2.  **Previsão de Sensação Térmica:** Utilização de Machine Learning para estimar a sensação térmica percebida com base em variáveis ambientais.

## 2. Arquitetura da Solução

A solução foi desenvolvida utilizando uma arquitetura de microsserviços conteinerizados via Docker, garantindo reprodutibilidade e escalabilidade.

### 2.1. Diagrama Geral
> *[INSERIR AQUI: Print ou Diagrama da Arquitetura do Docker Compose]*

### 2.2. Ferramentas Utilizadas

*   **Ingestão:**
    *   **Python Scripts:** Simulação de sensores IoT enviando dados via HTTP/MQTT.
    *   **FastAPI:** Gateway de entrada que recebe os dados e orquestra o armazenamento.
*   **Armazenamento:**
    *   **MinIO (S3 Compatible):** Armazenamento de dados brutos (Raw Data) em formato JSON (Data Lake - Camada Bronze).
    *   **PostgreSQL:** Banco de dados relacional para armazenamento de dados tratados e metadados do MLflow (Data Warehouse - Camada Silver).
*   **Processamento e Machine Learning:**
    *   **Jupyter Notebook:** Ambiente para análise exploratória e prototipagem.
    *   **Scikit-Learn:** Biblioteca para treinamento dos modelos (Random Forest/Gradient Boosting).
    *   **MLflow:** Plataforma para rastreamento de experimentos, métricas e versionamento de modelos.
*   **Visualização:**
    *   **ThingsBoard:** Plataforma IoT para dashboards em tempo real.
    *   **Trendz Analytics:** Ferramenta de BI para análises históricas avançadas.

## 3. Metodologia

### 3.1. Coleta e Tratamento de Dados

Os dados utilizados simulam estações automáticas do INMET no estado de Pernambuco. As seguintes variáveis são monitoradas:
*   Temperatura (°C)
*   Umidade Relativa (%)
*   Velocidade do Vento (m/s)
*   Pressão Atmosférica (hPa)
*   Radiação Solar (KJ/m²)

**Fluxo de Tratamento:**
1.  Os dados brutos chegam via API e são salvos no S3 (MinIO) para auditoria/backup.
2.  O sistema valida os tipos de dados e remove inconsistências básicas.
3.  Os dados limpos são inseridos no PostgreSQL para consumo pelos modelos.

### 3.2. Modelagem Preditiva

Para resolver o problema da **Sensação Térmica**, testamos algoritmos de regressão para prever a variável alvo com base nas entradas (Temperatura, Umidade, Vento).

*   **Algoritmos Testados:** Random Forest Regressor e Gradient Boosting.
*   **Métrica de Avaliação:** RMSE (Root Mean Squared Error) e R² (Coeficiente de Determinação).

O MLflow foi utilizado para registrar cada execução de treinamento, permitindo comparar qual hiperparâmetro gerou o menor erro.

> *[INSERIR AQUI: Print da interface do MLflow mostrando os experimentos listados]*

## 4. Análises e Resultados

### 4.1. Desempenho do Modelo

O modelo selecionado para produção foi o **Gradient Boosting Regressor**, apresentando os seguintes resultados nos dados de teste:

*   **RMSE:** 0.1606°C (Erro médio muito baixo).
*   **R²:** 0.9988 (O modelo explica 99.8% da variância dos dados).

### 4.2. Importância das Variáveis

A análise de *Feature Importance* demonstrou que a **Temperatura** é o fator dominante absoluto para a sensação térmica (aprox. 94.8%), seguida pela radiação solar (normalizada e absoluta) e velocidade do vento. A umidade apresentou uma influência menor no modelo final.

> *[INSERIR AQUI: Gráfico de Feature Importance gerado no Jupyter]*

## 5. Dashboard e Insights

O dashboard no **ThingsBoard** foi configurado para permitir o monitoramento em tempo real pelos operadores.

### 5.1. Visualizações Implementadas

1.  **Cards de Tempo Real:** Exibem a temperatura atual, umidade e a sensação térmica predita pelo modelo.
2.  **Gráficos de Linha:** Histórico das últimas 24 horas.
3.  **Alarms/Widgets:** Indicadores visuais da "Zona de Conforto". Se a predição indica "Muito Quente", o widget muda de cor (ex: Vermelho).

> *[INSERIR AQUI: Print Principal do Dashboard no ThingsBoard]*

> *[INSERIR AQUI: Print de um gráfico histórico ou detalhe do Trendz]*

## 6. Conclusões

O projeto cumpriu com sucesso o objetivo de implementar um pipeline de dados moderno e conteinerizado. A integração entre **FastAPI, MLflow e ThingsBoard** provou ser robusta, permitindo que um modelo treinado em Python fosse consumido instantaneamente por uma interface de IoT.

**Melhorias Futuras:**
*   Integração com a API real do INMET para dados ao vivo.
*   Implementação de alertas por SMS/Email via ThingsBoard quando a zona de conforto atingir níveis críticos ("Perigo").
*   Aumento da janela de dados históricos para capturar sazonalidade anual.

## Referências

[1] Documentação do Scikit-Learn. Disponível em: https://scikit-learn.org/

[2] Documentação do MLflow. Disponível em: https://mlflow.org/

[3] Documentação do ThingsBoard. Disponível em: https://thingsboard.io/

