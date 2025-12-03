#!/usr/bin/env python3
"""
Script de Teste - API de Predição de Sensação Térmica
=====================================================

Testa os endpoints da API de predição.
"""

import requests
import json

# Configuração
API_BASE_URL = "http://localhost:8060"
PREDICTION_ENDPOINT = f"{API_BASE_URL}/prediction"

def print_section(title: str):
    """Imprimir seção formatada."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def print_result(response: requests.Response):
    """Imprimir resultado formatado."""
    try:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        print(response.text)

def test_comfort_zones():
    """Testar endpoint de zonas de conforto."""
    print_section("1. ZONAS DE CONFORTO TÉRMICO")
    
    response = requests.get(f"{PREDICTION_ENDPOINT}/comfort-zones")
    print(f"Status: {response.status_code}")
    print_result(response)

def test_single_prediction():
    """Testar predição única."""
    print_section("2. PREDIÇÃO ÚNICA - DIA QUENTE DE VERÃO")
    
    payload = {
        "temperature": 32.0,
        "humidity": 70.0,
        "wind_velocity": 3.5,
        "pressure": 1013.0,
        "solar_radiation": 850.0,
        "timestamp": "2023-07-15T14:30:00"
    }
    
    print("📤 Enviando dados:")
    print(json.dumps(payload, indent=2))
    print()
    
    response = requests.post(
        f"{PREDICTION_ENDPOINT}/predict",
        params={"model": "random_forest"},
        json=payload
    )
    
    print(f"📥 Resposta (Status {response.status_code}):")
    print_result(response)

def test_multiple_scenarios():
    """Testar múltiplos cenários."""
    print_section("3. MÚLTIPLOS CENÁRIOS CLIMÁTICOS")
    
    scenarios = [
        {
            "name": "🌞 Dia Quente de Verão",
            "data": {
                "temperature": 32.0,
                "humidity": 70.0,
                "wind_velocity": 3.5,
                "pressure": 1013.0,
                "solar_radiation": 850.0
            }
        },
        {
            "name": "❄️ Noite Fria de Inverno",
            "data": {
                "temperature": 12.0,
                "humidity": 80.0,
                "wind_velocity": 15.0,
                "pressure": 1020.0,
                "solar_radiation": 0.0
            }
        },
        {
            "name": "🌤️ Tarde Confortável",
            "data": {
                "temperature": 24.0,
                "humidity": 60.0,
                "wind_velocity": 5.0,
                "pressure": 1015.0,
                "solar_radiation": 400.0
            }
        },
        {
            "name": "🌧️ Dia Chuvoso e Ventoso",
            "data": {
                "temperature": 18.0,
                "humidity": 90.0,
                "wind_velocity": 25.0,
                "pressure": 1005.0,
                "solar_radiation": 100.0
            }
        }
    ]
    
    for scenario in scenarios:
        print(f"\n{scenario['name']}")
        print("-" * 70)
        
        response = requests.post(
            f"{PREDICTION_ENDPOINT}/predict",
            params={"model": "random_forest"},
            json=scenario['data']
        )
        
        if response.status_code == 200:
            result = response.json()['data']
            
            print("  Entrada:")
            print(f"    • Temperatura: {scenario['data']['temperature']}°C")
            print(f"    • Umidade: {scenario['data']['humidity']}%")
            print(f"    • Vento: {scenario['data']['wind_velocity']} km/h")
            print(f"    • Radiação: {scenario['data']['solar_radiation']} W/m²")
            
            print("\n  Resultado:")
            print(f"    • Sensação Física: {result.get('physical_sensation')}°C")
            print(f"    • Zona Física: {result.get('physical_comfort_zone')}")
            
            if 'ml_prediction' in result:
                print(f"    • Predição ML: {result['ml_prediction']}°C")
                print(f"    • Zona ML: {result['ml_comfort_zone']}")
                print(f"    • Diferença: {result['prediction_difference']}°C")
            else:
                print("    • ⚠️ Modelos ML não treinados ainda")
        else:
            print(f"  ❌ Erro: {response.status_code}")

def test_batch_prediction():
    """Testar predição em lote."""
    print_section("4. PREDIÇÃO EM LOTE")
    
    payload = {
        "model_name": "random_forest",
        "data": [
            {
                "temperature": 28.5,
                "humidity": 65.0,
                "wind_velocity": 5.0,
                "pressure": 1013.0,
                "solar_radiation": 600.0
            },
            {
                "temperature": 22.0,
                "humidity": 70.0,
                "wind_velocity": 8.0,
                "pressure": 1015.0,
                "solar_radiation": 300.0
            },
            {
                "temperature": 16.0,
                "humidity": 85.0,
                "wind_velocity": 12.0,
                "pressure": 1018.0,
                "solar_radiation": 50.0
            }
        ]
    }
    
    print(f"📤 Enviando {len(payload['data'])} pontos de dados...")
    print()
    
    response = requests.post(
        f"{PREDICTION_ENDPOINT}/predict/batch",
        json=payload
    )
    
    print(f"📥 Resposta (Status {response.status_code}):")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ {result['message']}")
        print(f"Total: {result['data']['total']} predições")
        print(f"Modelo: {result['data']['model_used']}")
        
        print("\nResultados:")
        for i, pred in enumerate(result['data']['predictions'], 1):
            print(f"\n  Ponto {i}:")
            print(f"    • Temperatura: {pred['input']['temperature']}°C")
            print(f"    • Sensação Física: {pred['physical_sensation']}°C ({pred['physical_comfort_zone']})")
            if 'ml_prediction' in pred:
                print(f"    • Predição ML: {pred['ml_prediction']}°C ({pred['ml_comfort_zone']})")
    else:
        print_result(response)

def test_list_models():
    """Testar listagem de modelos."""
    print_section("5. MODELOS DISPONÍVEIS")
    
    response = requests.get(f"{PREDICTION_ENDPOINT}/models")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()['data']
        
        if result['available_models']:
            print(f"\n✅ {result['total_models']} modelo(s) disponível(veis):")
            for model_name in result['available_models']:
                if model_name in result['model_info']:
                    info = result['model_info'][model_name]
                    print(f"\n  📦 {model_name}")
                    print(f"     Status: {info['status']}")
                    print(f"     Tamanho: {info['size_mb']} MB")
                    print(f"     Path: {info['path']}")
        else:
            print("\n⚠️ Nenhum modelo treinado ainda")
            print("   Execute: curl -X POST http://localhost:8060/prediction/train")
    else:
        print_result(response)

def test_train_models():
    """Testar treinamento de modelos."""
    print_section("6. TREINAR MODELOS")
    
    print("⚠️ ATENÇÃO: Este processo pode levar alguns minutos...")
    confirm = input("Deseja continuar? (s/n): ")
    
    if confirm.lower() != 's':
        print("❌ Treinamento cancelado")
        return
    
    print("\n🎓 Iniciando treinamento...")
    
    try:
        response = requests.post(
            f"{PREDICTION_ENDPOINT}/train",
            timeout=300  # 5 minutos
        )
        
        print(f"\n📥 Resposta (Status {response.status_code}):")
        print_result(response)
        
    except requests.exceptions.Timeout:
        print("\n⏱️ Timeout: O treinamento está demorando mais que o esperado")
        print("   Verifique os logs do container para acompanhar o progresso")
    except Exception as e:
        print(f"\n❌ Erro: {e}")

def main():
    """Executar todos os testes."""
    print("=" * 70)
    print("  🔮 TESTE DA API DE PREDIÇÃO DE SENSAÇÃO TÉRMICA")
    print("=" * 70)
    print(f"\n🌐 API Base URL: {API_BASE_URL}")
    print(f"📡 Prediction Endpoint: {PREDICTION_ENDPOINT}")
    
    # Verificar se API está online
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API está online!\n")
        else:
            print(f"⚠️ API retornou status {response.status_code}\n")
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar à API")
        print("   Certifique-se de que o servidor está rodando")
        return
    
    # Executar testes
    try:
        test_comfort_zones()
        test_list_models()
        test_single_prediction()
        test_multiple_scenarios()
        test_batch_prediction()
        
        # Perguntar se deseja treinar modelos
        print("\n" + "="*70)
        test_train_models()
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Testes interrompidos pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
    
    print("\n" + "="*70)
    print("  ✅ TESTES CONCLUÍDOS")
    print("="*70)
    print("\n📚 Para mais informações, acesse:")
    print(f"   • Documentação Interativa: {API_BASE_URL}/docs")
    print("   • MLflow UI: http://localhost:5000")
    print("   • Guia completo: docs/PREDICTION_API.md")
    print()

if __name__ == "__main__":
    main()
