# 🌡️ Configuração Trendz Analytics - Sistema de Predição de Sensação Térmica

## 🎯 Objetivo

Configurar o Trendz Analytics para realizar análise avançada de sensação térmica e predição de conforto térmico, incluindo visualizações de zonas de conforto, mapas de calor térmico e insights de business intelligence sobre conforto humano.

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

### 1. Mapa de Calor de Conforto Térmico
- **Visualização**: Heatmap de sensação térmica
- **Dados**: Temperatura, umidade, sensação térmica calculada
- **Zonas de Conforto**: 5 classificações (Muito Frio → Muito Quente)
- **Filtros**: Período, zona de conforto, faixa térmica

### 2. Análise Temporal de Conforto
- **Heatmap**: Sensação térmica por hora/dia da semana
- **Linha temporal**: Tendências por zona de conforto
- **Distribuição**: Gráfico de barras por zona
- **Scatter**: Temperatura vs Umidade com zonas coloridas

### 3. Painel de Estatísticas Térmicas
- **KPIs**: Sensação térmica média e distribuição
- **Gauge**: Índice de conforto predominante
- **Histograma**: Distribuição de sensações térmicas

## 🔧 Estrutura de Arquivos

```
trendz/
├── config.py          # Configuração térmica e integração
├── dashboard.py       # Dashboards de conforto térmico
└── logs/              # Logs do Trendz

data/
├── sample_thermal_data.csv           # Dataset térmico (157.800 registros)
└── trendz_dashboard_config.json   # Configuração térmica dos dashboards
```

## 📈 Dataset Térmico

O sistema utiliza **157.800 registros históricos (2000-2017)** incluindo:
- **Timestamp**: Registros históricos detalhados
- **Temperatura**: 10-45°C com padrões climáticos brasileiros
- **Umidade**: 20-95% com variações sazonais
- **Velocidade do vento**: 0-15 m/s para cálculo térmico
- **Pressão atmosférica**: 980-1030 hPa
- **Radiação solar**: 0-1200 W/m² com ciclos diário/sazonal
- **Sensação térmica**: 5-87°C (Heat Index + Wind Chill)
- **Zona de conforto**: Muito Frio, Frio, Confortável, Quente, Muito Quente

## 🤖 Algoritmos de Cálculo Térmico

### Heat Index (Temperaturas ≥ 27°C)
- **Fórmula**: Rothfusz com ajustes para umidade brasileira
- **Variáveis**: Temperatura do ar + Umidade relativa
- **Ajustes**: Pressão atmosférica e radiação solar

### Wind Chill (Temperaturas < 27°C)
- **Fórmula**: Joint Action Group for Temperature Indices
- **Variáveis**: Temperatura + Velocidade do vento
- **Correção**: Adaptação para clima tropical/subtropical brasileiro

### Classificação de Zonas de Conforto
- **Muito Frio**: < 16°C sensação térmica
- **Frio**: 16-21°C sensação térmica
- **Confortável**: 21-26°C sensação térmica (zona ideal)
- **Quente**: 26-32°C sensação térmica
- **Muito Quente**: > 32°C sensação térmica

## 🔄 Fluxo de Dados Térmicos

```
Dados Climáticos → Cálculo Térmico → ThingsBoard → Trendz Analytics → Insights
       ↓                 ↓              ↓              ↓
   Sensores         Heat Index      Dashboard      Predição ML
       ↓             Wind Chill         ↓              ↓
   CSV/API         Zona Conforto   Tempo Real   Business Intelligence
```

## 📋 Checklist de Configuração

### ✅ Pré-requisitos
- [ ] Docker e Docker Compose instalados
- [ ] Portas 8080, 8888, 5432 disponíveis
- [ ] Pelo menos 4GB de RAM livres
- [ ] Dataset térmico de 157.800 registros

### ✅ Configuração Térmica
- [ ] Serviços Docker iniciados
- [ ] ThingsBoard acessível
- [ ] Trendz Analytics acessível
- [ ] Dataset térmico carregado
- [ ] Dashboards configurados

### ✅ Validação
- [ ] Login no Trendz realizado
- [ ] Dados térmicos importados com sucesso
- [ ] Mapas de calor térmico visíveis
- [ ] Zonas de conforto identificadas
- [ ] Métricas de sensação térmica calculadas

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