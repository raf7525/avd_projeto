#!/usr/bin/env python3
"""
Quick Start - Sistema de Predição de Sensação Térmica
=====================================================

Script para inicialização rápida do sistema.
"""

import subprocess
import time
import requests
import sys
from typing import Optional

COLORS = {
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'RED': '\033[91m',
    'BLUE': '\033[94m',
    'RESET': '\033[0m',
    'BOLD': '\033[1m'
}

def print_colored(message: str, color: str = 'RESET'):
    """Imprimir mensagem colorida."""
    print(f"{COLORS[color]}{message}{COLORS['RESET']}")

def print_header(title: str):
    """Imprimir cabeçalho."""
    print(f"\n{COLORS['BOLD']}{COLORS['BLUE']}{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}{COLORS['RESET']}\n")

def check_docker():
    """Verificar se Docker está instalado e rodando."""
    try:
        subprocess.run(['docker', '--version'], capture_output=True, check=True)
        subprocess.run(['docker-compose', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def check_api_health(max_retries: int = 20) -> bool:
    """Verificar se API está respondendo."""
    print_colored("🔍 Verificando saúde da API...", 'YELLOW')
    
    for i in range(max_retries):
        try:
            response = requests.get('http://localhost:8060/docs', timeout=3)
            if response.status_code == 200:
                print_colored("✅ API está online!", 'GREEN')
                return True
        except requests.exceptions.RequestException:
            pass
        
        if i < max_retries - 1:
            print(f"⏳ Aguardando API... ({i+1}/{max_retries})")
            time.sleep(3)
    
    return False

def start_services():
    """Iniciar serviços Docker."""
    print_header("🚀 INICIANDO SERVIÇOS")
    
    if not check_docker():
        print_colored("❌ Docker não está instalado ou não está rodando", 'RED')
        print_colored("   Instale o Docker: https://docs.docker.com/get-docker/", 'YELLOW')
        return False
    
    print_colored("🐳 Docker detectado!", 'GREEN')
    print_colored("\n📦 Iniciando containers (isso pode levar alguns minutos)...", 'YELLOW')
    
    try:
        subprocess.run(['docker-compose', 'up', '-d', '--build'], check=True)
        print_colored("\n✅ Containers iniciados!", 'GREEN')
        
        # Aguardar API ficar online
        if check_api_health():
            return True
        else:
            print_colored("\n⚠️ API demorou para responder, mas containers estão rodando", 'YELLOW')
            return True
            
    except subprocess.CalledProcessError as e:
        print_colored(f"\n❌ Erro ao iniciar containers: {e}", 'RED')
        return False

def train_models():
    """Treinar modelos ML."""
    print_header("🎓 TREINANDO MODELOS")
    
    print_colored("📚 Iniciando treinamento dos modelos de ML...", 'YELLOW')
    print_colored("   Isso pode levar 2-5 minutos dependendo do hardware.", 'YELLOW')
    
    try:
        response = requests.post(
            'http://localhost:8060/prediction/train',
            timeout=300  # 5 minutos
        )
        
        if response.status_code == 200:
            result = response.json()
            print_colored("\n✅ Modelos treinados com sucesso!", 'GREEN')
            
            if 'data' in result and 'metrics' in result['data']:
                print_colored("\n📊 Métricas dos modelos:", 'BLUE')
                for model_name, metrics in result['data']['metrics'].items():
                    print(f"\n  {model_name}:")
                    print(f"    RMSE: {metrics.get('test_rmse', 'N/A'):.4f}°C")
                    print(f"    MAE:  {metrics.get('test_mae', 'N/A'):.4f}°C")
                    print(f"    R²:   {metrics.get('test_r2', 'N/A'):.4f}")
            
            return True
        else:
            print_colored(f"\n⚠️ Erro no treinamento: Status {response.status_code}", 'YELLOW')
            print_colored(f"   {response.text}", 'RED')
            return False
            
    except requests.exceptions.Timeout:
        print_colored("\n⏱️ Timeout: Treinamento está demorando mais que o esperado", 'YELLOW')
        print_colored("   Verifique os logs: docker-compose logs app", 'YELLOW')
        return False
    except Exception as e:
        print_colored(f"\n❌ Erro: {e}", 'RED')
        return False

def test_prediction():
    """Fazer uma predição de teste."""
    print_header("🔮 TESTE DE PREDIÇÃO")
    
    test_data = {
        "temperature": 28.5,
        "humidity": 70.0,
        "wind_velocity": 5.0,
        "pressure": 1013.0,
        "solar_radiation": 600.0
    }
    
    print_colored("📤 Enviando dados de teste:", 'BLUE')
    print(f"  • Temperatura: {test_data['temperature']}°C")
    print(f"  • Umidade: {test_data['humidity']}%")
    print(f"  • Vento: {test_data['wind_velocity']} km/h")
    print(f"  • Pressão: {test_data['pressure']} hPa")
    print(f"  • Radiação: {test_data['solar_radiation']} W/m²")
    
    try:
        response = requests.post(
            'http://localhost:8060/prediction/predict',
            params={'model': 'random_forest'},
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()['data']
            
            print_colored("\n✅ Predição realizada com sucesso!", 'GREEN')
            print_colored("\n📊 Resultados:", 'BLUE')
            print(f"  • Sensação Térmica (Física): {result.get('physical_sensation')}°C")
            print(f"  • Zona de Conforto (Física): {result.get('physical_comfort_zone')}")
            
            if 'ml_prediction' in result:
                print(f"  • Sensação Térmica (ML): {result['ml_prediction']}°C")
                print(f"  • Zona de Conforto (ML): {result['ml_comfort_zone']}")
                print(f"  • Diferença: {result['prediction_difference']}°C")
                print(f"  • Modelo usado: {result['model_used']}")
            
            return True
        else:
            print_colored(f"\n⚠️ Erro na predição: Status {response.status_code}", 'YELLOW')
            return False
            
    except Exception as e:
        print_colored(f"\n❌ Erro: {e}", 'RED')
        return False

def show_services():
    """Mostrar informações dos serviços."""
    print_header("🌐 SERVIÇOS DISPONÍVEIS")
    
    services = [
        ("API FastAPI", "http://localhost:8060", "API principal com predições"),
        ("Swagger Docs", "http://localhost:8060/docs", "Documentação interativa"),
        ("MLflow", "http://localhost:5000", "Tracking de experimentos"),
        ("Jupyter Lab", "http://localhost:1010", "Notebooks interativos"),
        ("MinIO Console", "http://localhost:9001", "Storage S3-compatible"),
        ("PostgreSQL", "localhost:5433", "Banco de dados")
    ]
    
    for name, url, description in services:
        print(f"📡 {COLORS['BOLD']}{name}{COLORS['RESET']}")
        print(f"   URL: {COLORS['BLUE']}{url}{COLORS['RESET']}")
        print(f"   {description}\n")

def show_next_steps():
    """Mostrar próximos passos."""
    print_header("📚 PRÓXIMOS PASSOS")
    
    steps = [
        ("1. Ver documentação interativa", "http://localhost:8060/docs"),
        ("2. Testar mais predições", "python scripts/test_prediction_api.py"),
        ("3. Ver experimentos no MLflow", "http://localhost:5000"),
        ("4. Explorar notebooks", "http://localhost:1010"),
        ("5. Ler documentação completa", "docs/PREDICTION_API.md")
    ]
    
    for step, info in steps:
        print(f"{COLORS['GREEN']}✓{COLORS['RESET']} {step}")
        print(f"  {COLORS['BLUE']}{info}{COLORS['RESET']}\n")

def main():
    """Executar inicialização completa."""
    print_colored(f"""
    {COLORS['BOLD']}╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║        🌡️  SISTEMA DE PREDIÇÃO DE SENSAÇÃO TÉRMICA 🌡️            ║
    ║                                                                   ║
    ║              Projeto AVD - CESAR School 2025                      ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """, 'BOLD')
    
    print_colored("\n🚀 Bem-vindo ao Quick Start!\n", 'GREEN')
    print_colored("Este script irá:", 'YELLOW')
    print("  1. Iniciar todos os serviços Docker")
    print("  2. Treinar os modelos de Machine Learning")
    print("  3. Fazer uma predição de teste")
    print("  4. Mostrar informações úteis\n")
    
    # Confirmar execução
    try:
        confirm = input(f"{COLORS['YELLOW']}Deseja continuar? (s/n): {COLORS['RESET']}")
        if confirm.lower() != 's':
            print_colored("\n❌ Operação cancelada pelo usuário", 'RED')
            return
    except (EOFError, KeyboardInterrupt):
        print_colored("\n\n❌ Operação cancelada pelo usuário", 'RED')
        return
    
    # Passo 1: Iniciar serviços
    if not start_services():
        print_colored("\n❌ Falha ao iniciar serviços. Verifique os logs.", 'RED')
        print_colored("   Logs: docker-compose logs", 'YELLOW')
        sys.exit(1)
    
    # Passo 2: Treinar modelos
    print()
    try:
        train_choice = input(f"{COLORS['YELLOW']}Deseja treinar os modelos agora? (s/n): {COLORS['RESET']}")
    except (EOFError, KeyboardInterrupt):
        train_choice = 'n'
        print()
    
    if train_choice.lower() == 's':
        if train_models():
            # Passo 3: Testar predição
            test_prediction()
        else:
            print_colored("\n⚠️ Treinar modelos manualmente mais tarde:", 'YELLOW')
            print_colored("   curl -X POST http://localhost:8060/prediction/train", 'BLUE')
    else:
        print_colored("\n⚠️ Modelos não treinados. Treine antes de fazer predições:", 'YELLOW')
        print_colored("   curl -X POST http://localhost:8060/prediction/train", 'BLUE')
    
    # Mostrar informações
    show_services()
    show_next_steps()
    
    print_header("✅ INICIALIZAÇÃO CONCLUÍDA")
    
    print_colored("🎉 Sistema pronto para uso!", 'GREEN')
    print_colored("\n💡 Dica: Para parar os serviços, execute:", 'YELLOW')
    print_colored("   docker-compose down\n", 'BLUE')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n\n⚠️ Operação interrompida pelo usuário", 'YELLOW')
        sys.exit(0)
    except Exception as e:
        print_colored(f"\n❌ Erro inesperado: {e}", 'RED')
        sys.exit(1)
