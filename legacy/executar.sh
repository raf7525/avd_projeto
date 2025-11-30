#!/bin/bash

# 🚀 Script de Execução - Sistema de Predição de Sensação Térmica
# Este script automatiza o processo de inicialização e verificação do sistema

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir mensagens coloridas
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Função para verificar se uma porta está em uso
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_warning "Porta $port está em uso"
        return 1
    else
        print_success "Porta $port está disponível"
        return 0
    fi
}

# Função para verificar serviço via HTTP
check_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1
    
    print_status "Verificando $service_name..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s -I "$url" >/dev/null 2>&1; then
            print_success "$service_name está funcionando! ($url)"
            return 0
        fi
        
        echo -n "."
        sleep 2
        ((attempt++))
    done
    
    print_error "$service_name não está respondendo após $max_attempts tentativas"
    return 1
}

# Função principal
main() {
    echo "🌡️ Iniciando Sistema de Predição de Sensação Térmica"
    echo "=================================================="
    
    # 1. Verificar se estamos no diretório correto
    if [ ! -f "docker-compose.yml" ]; then
        print_error "docker-compose.yml não encontrado!"
        print_status "Navegando para o diretório correto..."
        cd /home/raf75/quinto-periodo/avd/avd_projeto
        
        if [ ! -f "docker-compose.yml" ]; then
            print_error "Ainda não foi possível encontrar docker-compose.yml"
            exit 1
        fi
    fi
    
    print_success "Diretório correto encontrado: $(pwd)"
    
    # 2. Verificar se Docker está rodando
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker não está rodando! Inicie o Docker primeiro."
        exit 1
    fi
    
    print_success "Docker está rodando"
    
    # 3. Verificar portas disponíveis
    print_status "Verificando portas necessárias..."
    ports=(8060 1010 5000 8080 8888 9000 9001 5433)
    for port in "${ports[@]}"; do
        if ! check_port $port; then
            print_warning "Porta $port está ocupada. Tentando continuar..."
        fi
    done
    
    # 4. Parar containers existentes (se houver)
    print_status "Parando containers existentes..."
    docker-compose down >/dev/null 2>&1
    
    # 5. Iniciar todos os serviços
    print_status "Iniciando todos os serviços..."
    if docker-compose up -d; then
        print_success "Containers iniciados com sucesso!"
    else
        print_error "Falha ao iniciar containers"
        exit 1
    fi
    
    # 6. Aguardar serviços subirem
    print_status "Aguardando serviços iniciarem (30 segundos)..."
    sleep 30
    
    # 7. Verificar status dos containers
    print_status "Verificando status dos containers..."
    docker-compose ps
    
    # 8. Verificar serviços individualmente
    echo ""
    print_status "Testando conectividade dos serviços..."
    
    # Lista de serviços para verificar
    declare -A services=(
        ["FastAPI"]="http://localhost:8060"
        ["Jupyter"]="http://localhost:1010"
        ["MLflow"]="http://localhost:5000"
        ["ThingsBoard"]="http://localhost:8080"
        ["Trendz"]="http://localhost:8888"
        ["MinIO"]="http://localhost:9001"
    )
    
    success_count=0
    total_services=${#services[@]}
    
    for service in "${!services[@]}"; do
        if check_service "${services[$service]}" "$service"; then
            ((success_count++))
        fi
    done
    
    echo ""
    echo "=================================================="
    
    if [ $success_count -eq $total_services ]; then
        print_success "🎉 TODOS OS SERVIÇOS ESTÃO FUNCIONANDO! ($success_count/$total_services)"
        echo ""
        echo "🌐 URLs de Acesso:"
        echo "  • FastAPI: http://localhost:8060"
        echo "  • Documentação API: http://localhost:8060/docs"
        echo "  • Jupyter Lab: http://localhost:1010"
        echo "  • MLflow: http://localhost:5000"
        echo "  • ThingsBoard: http://localhost:8080"
        echo "  • Trendz Analytics: http://localhost:8888"
        echo "  • MinIO Console: http://localhost:9001"
        echo ""
        echo "📊 Dataset: 157.800 registros térmicos (2000-2017)"
        echo "🎯 Sistema: Predição de Sensação Térmica"
        echo ""
        echo "✅ Sistema pronto para uso!"
        
    elif [ $success_count -gt 0 ]; then
        print_warning "⚠️  ALGUNS SERVIÇOS FUNCIONANDO ($success_count/$total_services)"
        print_status "Verifique os logs para mais detalhes:"
        echo "  docker-compose logs"
        
    else
        print_error "❌ NENHUM SERVIÇO FUNCIONANDO"
        print_status "Execute para verificar problemas:"
        echo "  docker-compose logs"
        echo "  docker-compose ps"
        exit 1
    fi
}

# Função para mostrar ajuda
show_help() {
    echo "🌡️ Sistema de Predição de Sensação Térmica - Script de Execução"
    echo ""
    echo "Uso: $0 [opção]"
    echo ""
    echo "Opções:"
    echo "  start, up     - Inicia todos os serviços (padrão)"
    echo "  stop, down    - Para todos os serviços"
    echo "  restart       - Reinicia todos os serviços"
    echo "  status, ps    - Mostra status dos containers"
    echo "  logs          - Mostra logs dos serviços"
    echo "  test          - Testa conectividade dos serviços"
    echo "  clean         - Para e remove tudo (incluindo volumes)"
    echo "  help          - Mostra esta ajuda"
    echo ""
    echo "Exemplos:"
    echo "  $0              # Inicia sistema"
    echo "  $0 start        # Inicia sistema"
    echo "  $0 stop         # Para sistema"
    echo "  $0 logs         # Mostra logs"
}

# Processar argumentos
case "${1:-start}" in
    start|up|"")
        main
        ;;
    stop|down)
        print_status "Parando todos os serviços..."
        docker-compose down
        print_success "Serviços parados"
        ;;
    restart)
        print_status "Reiniciando todos os serviços..."
        docker-compose restart
        sleep 15
        print_success "Serviços reiniciados"
        ;;
    status|ps)
        print_status "Status dos containers:"
        docker-compose ps
        ;;
    logs)
        print_status "Logs dos serviços:"
        docker-compose logs --tail=50
        ;;
    test)
        print_status "Testando conectividade..."
        services=(
            "http://localhost:8060 FastAPI"
            "http://localhost:1010 Jupyter"
            "http://localhost:5000 MLflow"
            "http://localhost:8080 ThingsBoard"
            "http://localhost:8888 Trendz"
            "http://localhost:9001 MinIO"
        )
        
        for service in "${services[@]}"; do
            url=$(echo $service | cut -d' ' -f1)
            name=$(echo $service | cut -d' ' -f2)
            check_service "$url" "$name"
        done
        ;;
    clean)
        print_warning "⚠️  ATENÇÃO: Isto irá remover TODOS os dados!"
        read -p "Tem certeza? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_status "Removendo tudo..."
            docker-compose down -v
            docker system prune -f
            print_success "Sistema limpo"
        else
            print_status "Operação cancelada"
        fi
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Opção inválida: $1"
        show_help
        exit 1
        ;;
esac