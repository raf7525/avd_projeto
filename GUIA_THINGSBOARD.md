# 📊 GUIA COMPLETO - VISUALIZAÇÃO NO THINGSBOARD

## 🎯 O QUE VOCÊ JÁ TEM:
✅ **Dispositivo criado:** "Sensor Térmico AVD"  
✅ **Dados enviados:** 4 registros térmicos  
✅ **Tokens configurados:** Dispositivo ativo  

## 🌐 **PASSO A PASSO - CRIAR DASHBOARD**

### **1. Acessar Dispositivos:**
- Clique em **"Dispositivos"** (menu lateral)
- Encontre **"Sensor Térmico AVD"**
- Clique no dispositivo
- Vá em **"Últimos Dados"** - você verá:
  ```
  temperatura: 28.5
  umidade: 65.0
  sensacao_termica: 28.1
  zona_conforto: "Quente"
  velocidade_vento: 12.0
  pressao: 1015.0
  radiacao_solar: 800.0
  ```

### **2. Criar Dashboard:**
- Clique em **"Dashboards"** (menu lateral)
- Clique em **"+"** (Adicionar dashboard)
- Nome: **"Sensação Térmica AVD"**
- Clique **"Adicionar"**

### **3. Adicionar Widgets:**

#### **Widget 1: Termômetro de Sensação Térmica**
- Clique **"Entrar no modo de edição"** (ícone lápis)
- Clique **"Adicionar novo widget"**
- **Tipo:** `Analogue gauges` > `Gauge`
- **Dispositivo:** Sensor Térmico AVD
- **Chave:** `sensacao_termica`
- **Título:** "Sensação Térmica Atual"
- **Unidade:** °C
- **Min:** 0, **Max:** 50

#### **Widget 2: Gráfico de Temperatura**
- **Tipo:** `Charts` > `Time series - Flot`
- **Dispositivo:** Sensor Térmico AVD
- **Chaves:** `temperatura`, `sensacao_termica`
- **Título:** "Temperatura vs Sensação Térmica"

#### **Widget 3: Indicador de Zona de Conforto**
- **Tipo:** `Cards` > `Entities table`
- **Dispositivo:** Sensor Térmico AVD
- **Chave:** `zona_conforto`
- **Título:** "Zona de Conforto"

#### **Widget 4: Painel de Condições**
- **Tipo:** `Cards` > `Latest values`
- **Dispositivo:** Sensor Térmico AVD
- **Chaves:** `umidade`, `velocidade_vento`, `pressao`

## 🚀 **COMANDOS PARA DADOS EM TEMPO REAL:**

### **A) Enviar dados atuais:**
```bash
cd /home/raf75/quinto-periodo/avd/avd_projeto
python3 enviar_dados_thingsboard.py
```

### **B) Simular dados em tempo real:**
```bash
cd /home/raf75/quinto-periodo/avd/avd_projeto
python3 simular_dados_tempo_real.py
```
(Pressione Ctrl+C para parar)

## 🎨 **CORES PARA ZONAS DE CONFORTO:**
- **Muito Frio:** #0066CC (Azul escuro)
- **Frio:** #66B2FF (Azul claro)  
- **Confortável:** #00CC66 (Verde)
- **Quente:** #FF9900 (Laranja)
- **Muito Quente:** #CC0000 (Vermelho)

## 📈 **WIDGETS AVANÇADOS:**

### **Mapa de Calor por Hora:**
- **Tipo:** `Charts` > `Heatmap`
- **Eixo X:** hora
- **Eixo Y:** sensacao_termica
- **Valor:** intensidade

### **Alertas Automáticos:**
- Vá em **"Regras de cadeia"**
- Criar regra para **sensacao_termica > 32** → Alerta "Muito Quente"
- Criar regra para **sensacao_termica < 16** → Alerta "Muito Frio"

## 🔄 **ATUALIZAÇÕES EM TEMPO REAL:**
Os widgets atualizam automaticamente a cada 5 segundos quando há novos dados.

**Para ver mudanças em tempo real, execute o simulador e observe os widgets mudando!**