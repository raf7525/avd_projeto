# 📊 Guia Completo: Dashboard ThingsBoard para Dados Térmicos

Este guia te ensina como criar dashboards profissionais no ThingsBoard para visualizar dados de sensação térmica.

## 🎯 O que é o ThingsBoard Dashboard?

O **Dashboard** é onde você visualiza todos os dados do seu dispositivo IoT em **tempo real** através de **widgets interativos**.

### 📈 **Para que serve:**
- **Monitorar** temperatura, umidade, vento em tempo real
- **Analisar tendências** históricas (você tem dados de 2000-2017!)
- **Identificar padrões** de conforto térmico
- **Alertar** sobre condições extremas
- **Relatórios** para tomada de decisão

## 🚀 Passo a Passo: Criando seu Dashboard

### **Passo 1: Acessar ThingsBoard**
```
URL: http://localhost:8080
Usuário: tenant@thingsboard.org
Senha: tenant
```

### **Passo 2: Ir para Dashboards**
1. No menu lateral esquerdo, clique em **"Dashboards"**
2. Clique no botão **"+"** (adicionar novo dashboard)
3. Digite o nome: **"Análise de Sensação Térmica"**
4. Descrição: **"Dashboard para monitoramento e análise de dados térmicos"**
5. Clique **"Add"**

### **Passo 3: Entrar no Dashboard**
1. Clique no dashboard recém-criado
2. Clique no ícone de **"lápis"** (modo de edição)
3. Agora você pode adicionar widgets!

## 🎨 Widgets Essenciais para Dados Térmicos

### **1. 🌡️ Widget de Temperatura Atual**
**Para que serve:** Mostra a temperatura atual em tempo real

**Como criar:**
1. Clique **"Add widget"** → **"Cards"** → **"Simple card"**
2. **Datasource:** Selecione seu dispositivo "Sensor Térmico AVD"
3. **Keys:** Selecione "temperature"
4. **Appearance:**
   - Título: "Temperatura Atual"
   - Unidade: "°C"
   - Cor: Azul para frio, vermelho para quente
5. Clique **"Add"**

### **2. 💧 Widget de Umidade**
**Para que serve:** Monitora umidade relativa do ar

**Como criar:**
1. **"Add widget"** → **"Cards"** → **"Simple card"**
2. **Keys:** "humidity"
3. **Título:** "Umidade Relativa"
4. **Unidade:** "%"
5. **Cor:** Azul claro

### **3. 🌬️ Widget de Vento**
**Para que serve:** Mostra velocidade do vento

**Como criar:**
1. **"Add widget"** → **"Gauges"** → **"Radial gauge"**
2. **Keys:** "wind_velocity"
3. **Título:** "Velocidade do Vento"
4. **Unidade:** "m/s"
5. **Range:** 0 a 30 m/s

### **4. 🌡️ Widget de Sensação Térmica**
**Para que serve:** Mostra como o corpo humano "sente" a temperatura

**Como criar:**
1. **"Add widget"** → **"Cards"** → **"Simple card"**
2. **Keys:** "thermal_sensation"
3. **Título:** "Sensação Térmica"
4. **Unidade:** "°C"
5. **Cores condicionais:**
   - < 15°C: Azul (Frio)
   - 15-20°C: Verde claro (Fresco)
   - 20-26°C: Verde (Confortável)
   - 26-30°C: Amarelo (Quente)
   - > 30°C: Vermelho (Muito Quente)

### **5. 🎯 Widget de Zona de Conforto**
**Para que serve:** Classifica se o ambiente está confortável

**Como criar:**
1. **"Add widget"** → **"Cards"** → **"Simple card"**
2. **Keys:** "comfort_zone"
3. **Título:** "Zona de Conforto"
4. **Cores:**
   - Confortável: Verde
   - Quente/Frio: Amarelo
   - Muito Quente/Muito Frio: Vermelho

### **6. 📈 Gráfico de Tendência Temporal**
**Para que serve:** Mostra como os valores mudam ao longo do tempo

**Como criar:**
1. **"Add widget"** → **"Charts"** → **"Time series chart"**
2. **Keys:** Selecione múltiplas:
   - temperature
   - thermal_sensation
   - humidity
3. **Título:** "Tendências Térmicas"
4. **Período:** Últimas 24 horas
5. **Cores diferentes** para cada linha

### **7. 🌅 Gráfico de Radiação Solar**
**Para que serve:** Monitora intensidade solar

**Como criar:**
1. **"Add widget"** → **"Charts"** → **"Bar chart"**
2. **Keys:** "solar_radiation"
3. **Título:** "Radiação Solar"
4. **Unidade:** "W/m²"

### **8. 🏠 Distribuição de Conforto (Pizza Chart)**
**Para que serve:** Mostra % de tempo em cada zona de conforto

**Como criar:**
1. **"Add widget"** → **"Charts"** → **"Pie chart"**
2. **Keys:** "comfort_zone"
3. **Título:** "Distribuição de Conforto"
4. **Agrupar por valor** da zona de conforto

## 🎨 Layout Recomendado do Dashboard

```
┌─────────────────────────────────────────────────┐
│                  DASHBOARD TITLE                │
├─────────────────────────────────────────────────┤
│ 🌡️ Temp   💧 Umid   🌬️ Vento   🎯 Conforto    │
│  25.5°C    65%      8m/s      Confortável      │
├─────────────────────────────────────────────────┤
│           📈 GRÁFICO DE TENDÊNCIAS              │
│                (últimas 24h)                   │
├─────────────────────────────────────────────────┤
│ 🌅 Radiação │         🏠 Distribuição          │
│   Solar     │       de Conforto (Pizza)       │
└─────────────────────────────────────────────────┘
```

## 🔧 Configurações Avançadas

### **Atualizações em Tempo Real:**
- Configure **"Real-time"** para atualizar automaticamente
- Intervalo recomendado: **5 segundos**

### **Filtros Temporais:**
- Adicione filtros para **"Última hora"**, **"Último dia"**, **"Última semana"**
- Permite análise de diferentes períodos

### **Alertas:**
- Configure **limites** para temperatura extrema
- **Notificações** quando sair da zona de conforto

## 📱 Responsividade

O dashboard funciona em:
- 💻 **Desktop** (melhor experiência)
- 📱 **Mobile** (visualização simplificada)
- 📟 **Tablet** (layout intermediário)

## 🎯 Casos de Uso Práticos

### **Para Meteorologia:**
- Monitorar **estações climáticas**
- Prever **tendências** térmicas
- Alertar sobre **mudanças bruscas**

### **Para Conforto Ambiental:**
- **Climatização inteligente**
- **Economia de energia**
- **Bem-estar** dos ocupantes

### **Para Pesquisa:**
- Análise de **padrões históricos** (2000-2017)
- **Correlações** entre variáveis
- **Relatórios** científicos

## 🔍 Como Interpretar os Dados

### **Sensação Térmica:**
- **< 15°C:** Frio - precisa de aquecimento
- **15-20°C:** Fresco - confortável com roupa
- **20-26°C:** **IDEAL** - zona de conforto
- **26-30°C:** Quente - pode precisar de ventilação
- **> 30°C:** Muito quente - necessita resfriamento

### **Correlações Importantes:**
- **Alta umidade + alta temperatura** = sensação de muito calor
- **Vento forte + baixa temperatura** = sensação de muito frio
- **Radiação solar alta** = aquecimento durante o dia

## 🚀 Próximos Passos

Após criar o dashboard básico, você pode:

1. **Adicionar mais dispositivos** (outras estações)
2. **Criar alertas personalizados**
3. **Exportar relatórios** para análise
4. **Integrar com Trendz** para análises avançadas
5. **Configurar APIs** para apps mobile

---

## 💡 Dica Final

**Você tem 157.800 registros históricos!** Isso significa dados de **18 anos** para análise. Use isso para:
- Identificar **mudanças climáticas** ao longo dos anos
- Encontrar **padrões sazonais**
- **Comparar** anos diferentes
- Fazer **predições** baseadas em histórico

---

**🎯 Pronto!** Com este guia você terá um dashboard profissional funcionando. Cada widget tem um propósito específico e juntos formam uma ferramenta poderosa de análise térmica! 🌡️📊