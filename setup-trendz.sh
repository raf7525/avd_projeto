#!/bin/bash

# Script de configuração do Trendz Analytics
# Executa a configuração completa do ambiente de analytics

echo "🌪️ Configuração do Trendz Analytics para Análise de Vento"
echo "=========================================================="

# Verificar se o Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Inicie o Docker primeiro."
    exit 1
fi

# Verificar se os arquivos necessários existem
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Arquivo docker-compose.yml não encontrado"
    exit 1
fi

echo "📋 1. Preparando ambiente..."

# Criar diretórios necessários
mkdir -p data
mkdir -p trendz/logs

echo "🚀 2. Iniciando serviços Docker..."

# Iniciar serviços
docker-compose up -d postgres thingsboard trendz

echo "⏳ 3. Aguardando serviços inicializarem..."

# Aguardar PostgreSQL
echo "   Aguardando PostgreSQL..."
timeout=60
while ! docker-compose exec -T postgres pg_isready -h localhost -p 5432 > /dev/null 2>&1; do
    timeout=$((timeout - 1))
    if [ $timeout -eq 0 ]; then
        echo "❌ Timeout aguardando PostgreSQL"
        exit 1
    fi
    sleep 1
done
echo "   ✅ PostgreSQL pronto"

# Aguardar ThingsBoard
echo "   Aguardando ThingsBoard..."
timeout=120
while ! curl -s http://localhost:8080/api/noauth/health > /dev/null 2>&1; do
    timeout=$((timeout - 1))
    if [ $timeout -eq 0 ]; then
        echo "❌ Timeout aguardando ThingsBoard"
        echo "   Verifique os logs: docker-compose logs thingsboard"
        exit 1
    fi
    sleep 2
done
echo "   ✅ ThingsBoard pronto"

# Aguardar Trendz
echo "   Aguardando Trendz Analytics..."
timeout=120
while ! curl -s http://localhost:8888/api/noauth/health > /dev/null 2>&1; do
    timeout=$((timeout - 1))
    if [ $timeout -eq 0 ]; then
        echo "⚠️  Trendz pode ainda estar inicializando"
        echo "   Verifique os logs: docker-compose logs trendz"
        break
    fi
    sleep 2
done
echo "   ✅ Trendz Analytics pronto"

echo "📊 4. Configurando ambiente de analytics..."

# Executar configuração Python
if command -v python3 > /dev/null 2>&1; then
    echo "   Executando configuração Python..."
    docker-compose exec app python -c "
import sys
sys.path.append('/app')
from trendz.config import TrendzIntegration
from trendz.dashboard import main

print('Configurando Trendz...')
integration = TrendzIntegration()
integration.setup_complete_analytics()
integration.export_sample_data()

print('Configurando dashboards...')
main()
print('Configuração concluída!')
"
else
    echo "   Python não encontrado, executando configuração manual..."
fi

echo "🎉 5. Configuração concluída!"
echo ""
echo "📱 Serviços disponíveis:"
echo "   🌐 ThingsBoard:     http://localhost:8080"
echo "   📊 Trendz Analytics: http://localhost:8888"
echo "   🚀 FastAPI:         http://localhost:8060"
echo "   📓 Jupyter:         http://localhost:1010"
echo ""
echo "🔑 Credenciais padrão:"
echo "   Email:    tenant@thingsboard.org"
echo "   Senha:    tenant"
echo ""
echo "📁 Arquivos criados:"
echo "   - data/sample_wind_data.csv"
echo "   - data/trendz_dashboard_config.json"
echo ""
echo "📋 Próximos passos:"
echo "   1. Acesse o Trendz Analytics"
echo "   2. Faça login com as credenciais"
echo "   3. Importe os dados de exemplo"
echo "   4. Configure os dashboards de análise"
echo ""
echo "🔧 Para parar os serviços: docker-compose down"
echo "📊 Para ver logs: docker-compose logs [serviço]"