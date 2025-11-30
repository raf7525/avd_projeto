#!/bin/bash
# Script para gerenciar o ambiente Docker do projeto

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para exibir ajuda
show_help() {
    echo -e "${BLUE}=== GERENCIADOR DOCKER - Projeto AVD ===${NC}"
    echo ""
    echo "Uso: ./docker-manager.sh [COMANDO]"
    echo ""
    echo "Comandos disponíveis:"
    echo -e "  ${GREEN}start${NC}     - Iniciar todos os serviços"
    echo -e "  ${GREEN}stop${NC}      - Parar todos os serviços"
    echo -e "  ${GREEN}restart${NC}   - Reiniciar todos os serviços"
    echo -e "  ${GREEN}build${NC}     - Construir/reconstruir as imagens"
    echo -e "  ${GREEN}logs${NC}      - Visualizar logs de todos os serviços"
    echo -e "  ${GREEN}status${NC}    - Ver status dos containers"
    echo -e "  ${GREEN}clean${NC}     - Limpar containers, imagens e volumes"
    echo -e "  ${GREEN}jupyter${NC}   - Obter token do Jupyter"
    echo -e "  ${GREEN}shell${NC}     - Abrir shell no container principal"
    echo -e "  ${GREEN}urls${NC}      - Mostrar URLs dos serviços"
    echo ""
}

# Função para mostrar URLs
show_urls() {
    echo -e "${BLUE}=== SERVIÇOS DISPONÍVEIS ===${NC}"
    echo -e "🚀 ${GREEN}FastAPI:${NC}         http://localhost:8060"
    echo -e "📊 ${GREEN}Jupyter:${NC}         http://localhost:1010"
    echo -e "🔬 ${GREEN}MLflow:${NC}          http://localhost:5000"
    echo -e "📈 ${GREEN}Trendz Analytics:${NC} http://localhost:8888"
    echo -e "🌐 ${GREEN}ThingsBoard:${NC}     http://localhost:8080"
    echo -e "🗄️  ${GREEN}MinIO Console:${NC}    http://localhost:9001 (admin/minioadmin)"
    echo -e "🐘 ${GREEN}PostgreSQL:${NC}      localhost:5433 (user/password)"
    echo ""
}

# Detectar comando Docker Compose disponível
detect_docker_compose() {
    if command -v docker-compose &> /dev/null; then
        echo "docker-compose"
    elif docker compose version &> /dev/null; then
        echo "docker compose"
    else
        echo ""
    fi
}

# Verificar se Docker Compose está disponível
check_docker_compose() {
    DOCKER_COMPOSE_CMD=$(detect_docker_compose)
    if [ -z "$DOCKER_COMPOSE_CMD" ]; then
        echo -e "${RED}❌ Docker Compose não encontrado!${NC}"
        echo -e "${YELLOW}Por favor, instale o Docker Compose:${NC}"
        echo -e "  - Ubuntu/Debian: ${GREEN}sudo apt install docker-compose-plugin${NC}"
        echo -e "  - Ou baixe do site oficial: ${BLUE}https://docs.docker.com/compose/install/${NC}"
        exit 1
    fi
    echo "$DOCKER_COMPOSE_CMD"
}

# Função para iniciar serviços
start_services() {
    DOCKER_COMPOSE=$(check_docker_compose)
    echo -e "${GREEN}🚀 Iniciando serviços...${NC}"
    $DOCKER_COMPOSE up -d
    echo -e "${GREEN}✅ Serviços iniciados!${NC}"
    sleep 2
    show_urls
}

# Função para parar serviços
stop_services() {
    DOCKER_COMPOSE=$(check_docker_compose)
    echo -e "${YELLOW}🛑 Parando serviços...${NC}"
    $DOCKER_COMPOSE down
    echo -e "${GREEN}✅ Serviços parados!${NC}"
}

# Função para restart
restart_services() {
    DOCKER_COMPOSE=$(check_docker_compose)
    echo -e "${YELLOW}🔄 Reiniciando serviços...${NC}"
    $DOCKER_COMPOSE restart
    echo -e "${GREEN}✅ Serviços reiniciados!${NC}"
    show_urls
}

# Função para build
build_services() {
    DOCKER_COMPOSE=$(check_docker_compose)
    echo -e "${BLUE}🔨 Construindo imagens...${NC}"
    $DOCKER_COMPOSE build
    echo -e "${GREEN}✅ Build concluído!${NC}"
}

# Função para logs
show_logs() {
    DOCKER_COMPOSE=$(check_docker_compose)
    echo -e "${BLUE}📋 Exibindo logs...${NC}"
    $DOCKER_COMPOSE logs -f
}

# Função para status
show_status() {
    DOCKER_COMPOSE=$(check_docker_compose)
    echo -e "${BLUE}📊 Status dos containers:${NC}"
    $DOCKER_COMPOSE ps
}

# Função para limpeza
clean_all() {
    DOCKER_COMPOSE=$(check_docker_compose)
    echo -e "${RED}🧹 ATENÇÃO: Isso vai remover TODOS os containers, imagens e volumes!${NC}"
    read -p "Tem certeza? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Limpando...${NC}"
        $DOCKER_COMPOSE down -v
        docker system prune -af
        echo -e "${GREEN}✅ Limpeza concluída!${NC}"
    else
        echo -e "${BLUE}Operação cancelada.${NC}"
    fi
}

# Função para obter token do Jupyter
get_jupyter_token() {
    DOCKER_COMPOSE=$(check_docker_compose)
    echo -e "${BLUE}🔑 Token do Jupyter:${NC}"
    $DOCKER_COMPOSE exec app jupyter notebook list 2>/dev/null || \
    $DOCKER_COMPOSE logs app | grep -E "token|127.0.0.1" | tail -3
}

# Função para shell
open_shell() {
    DOCKER_COMPOSE=$(check_docker_compose)
    echo -e "${BLUE}🐚 Abrindo shell no container...${NC}"
    $DOCKER_COMPOSE exec app bash
}

# Main switch
case "${1:-help}" in
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    build)
        build_services
        ;;
    logs)
        show_logs
        ;;
    status)
        show_status
        ;;
    clean)
        clean_all
        ;;
    jupyter)
        get_jupyter_token
        ;;
    shell)
        open_shell
        ;;
    urls)
        show_urls
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}❌ Comando inválido: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac