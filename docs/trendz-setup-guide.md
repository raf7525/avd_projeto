# 📊 Configuração Trendz Analytics - Análise de Padrões de Vento

## 🎯 Objetivo

Configurar o Trendz Analytics para realizar análise avançada de padrões de vento, incluindo clustering, visualizações e insights de business intelligence.

## 🚀 Configuração Rápida

### 1. Executar Setup Automático
```bash
# No diretório do projeto
./setup-trendz.sh
```

### 2. Configuração Manual

#### Iniciar Serviços
```bash
docker-compose up -d postgres thingsboard trendz
```

#### Aguardar Inicialização
- PostgreSQL: ~30 segundos
- ThingsBoard: ~2-3 minutos
- Trendz Analytics: ~3-4 minutos

#### Executar Configuração Python
```bash
docker-compose exec app python trendz/config.py
docker-compose exec app python trendz/dashboard.py
```

## 🌐 Acesso aos Serviços

| Serviço | URL | Credenciais |
|---------|-----|-------------|
| **Trendz Analytics** | http://localhost:8888 | tenant@thingsboard.org / tenant |
| **ThingsBoard** | http://localhost:8080 | tenant@thingsboard.org / tenant |
| **FastAPI** | http://localhost:8060 | - |
| **Jupyter** | http://localhost:1010 | - |

## 📊 Dashboards Configurados

### 1. Rosa dos Ventos com Clusters
- **Visualização**: Gráfico polar colorido
- **Dados**: Direção e velocidade do vento
- **Agrupamento**: 5 clusters por padrões comportamentais
- **Filtros**: Período, velocidade mínima/máxima

### 2. Padrões Temporais
- **Heatmap**: Velocidade por hora/dia da semana
- **Linha temporal**: Tendências por cluster
- **Distribuição**: Gráfico de barras por cluster
- **Scatter**: Velocidade vs Direção

### 3. Painel de Estatísticas
- **KPIs**: Velocidade média e máxima
- **Gauge**: Direção predominante
- **Histograma**: Distribuição de velocidades

## 🔧 Estrutura de Arquivos

```
trendz/
├── config.py          # Configuração e integração
├── dashboard.py       # Criação de dashboards
└── logs/              # Logs do Trendz

data/
├── sample_wind_data.csv           # Dados de exemplo
└── trendz_dashboard_config.json   # Configuração dos dashboards
```

## 📈 Dados de Exemplo

O sistema gera automaticamente **30 dias** de dados sintéticos incluindo:
- **Timestamp**: Registros de hora em hora
- **Velocidade do vento**: 0-15 m/s com padrões sazonais
- **Direção do vento**: 0-360° com variações temporais
- **Temperatura**: 15-25°C correlacionada com hora
- **Umidade**: 30-70% com variação sazonal

## 🤖 Algoritmos de Clustering

### K-Means (5 clusters)
- **Features**: velocidade, direção, hora, dia da semana
- **Preprocessamento**: Normalização e tratamento circular da direção
- **Objetivo**: Identificar padrões comportamentais

### Interpretação dos Clusters
- **Cluster 0**: Ventos noturnos fracos
- **Cluster 1**: Ventos matutinos moderados
- **Cluster 2**: Ventos vespertinos intensos
- **Cluster 3**: Ventos irregulares
- **Cluster 4**: Ventos constantes diurnos

## 🔄 Fluxo de Dados

```
Dados de Vento → ThingsBoard → Trendz Analytics → Insights
     ↓              ↓              ↓
  Sensores      Dashboard      Clustering/ML
     ↓              ↓              ↓
  CSV/API      Tempo Real    Business Intelligence
```

## 📋 Checklist de Configuração

### ✅ Pré-requisitos
- [ ] Docker e Docker Compose instalados
- [ ] Portas 8080, 8888, 5432 disponíveis
- [ ] Pelo menos 4GB de RAM livres

### ✅ Configuração
- [ ] Serviços Docker iniciados
- [ ] ThingsBoard acessível
- [ ] Trendz Analytics acessível
- [ ] Dados de exemplo gerados
- [ ] Dashboards configurados

### ✅ Validação
- [ ] Login no Trendz realizado
- [ ] Dados importados com sucesso
- [ ] Rosa dos ventos visível
- [ ] Clusters identificados
- [ ] Métricas calculadas

## 🛠️ Solução de Problemas

### Trendz não inicia
```bash
# Verificar logs
docker-compose logs trendz

# Verificar dependências
docker-compose ps

# Reiniciar serviços
docker-compose restart trendz
```

### Erro de autenticação
1. Verificar se ThingsBoard está rodando
2. Usar credenciais padrão: tenant@thingsboard.org / tenant
3. Aguardar inicialização completa (~5 minutos)

### Dados não aparecem
1. Verificar arquivo CSV gerado em `/data/`
2. Executar novamente: `python trendz/dashboard.py`
3. Verificar conexão entre ThingsBoard e Trendz

## 🎨 Personalização

### Adicionar Novos Dashboards
```python
# No arquivo trendz/dashboard.py
def create_custom_dashboard():
    return {
        "name": "Meu Dashboard",
        "type": "custom_chart",
        "configuration": {
            # Sua configuração aqui
        }
    }
```

### Modificar Clustering
```python
# No arquivo trendz/dashboard.py
def perform_clustering(self, n_clusters=7, algorithm='DBSCAN'):
    # Implementar algoritmo personalizado
```

### Integrar Dados Reais
```python
# Substituir dados sintéticos por dados reais
def load_real_data(self, sensor_api_url):
    # Conectar com API de sensores reais
```

## 📊 Métricas de Monitoramento

- **Performance**: Tempo de resposta < 2s
- **Disponibilidade**: Uptime > 99%
- **Dados**: Processamento de 1000+ registros/hora
- **Clustering**: Convergência em < 5 iterações
- **Dashboards**: Atualização em tempo real

## 🚀 Próximos Passos

1. **Integração com sensores reais**
2. **Alertas automáticos** para condições extremas
3. **Previsão de padrões** com ML avançado
4. **Exportação de relatórios** em PDF
5. **API de insights** para outras aplicações

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique os logs: `docker-compose logs`
2. Consulte a documentação do Trendz
3. Acesse o painel de saúde: http://localhost:8888/health