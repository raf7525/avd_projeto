#!/usr/bin/env python3
"""
Script para verificar dados no ThingsBoard antes de criar dashboard
"""
import requests
from datetime import datetime
import os

# Configurações
THINGSBOARD_HOST = os.getenv("THINGSBOARD_HOST", "http://localhost:8080")
USERNAME = "tenant@thingsboard.org"
PASSWORD = "tenant"

def check_thingsboard_data():
    """Verificar se temos dados no dispositivo"""
    print("🔍 Verificando dados no ThingsBoard...")
    print("=" * 50)
    
    try:
        # 1. Login
        login_url = f"{THINGSBOARD_HOST}/api/auth/login"
        login_data = {"username": USERNAME, "password": PASSWORD}
        
        response = requests.post(login_url, json=login_data, timeout=10)
        if response.status_code != 200:
            print(f"❌ Erro no login: {response.status_code}")
            return
        
        token = response.json().get("token")
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Login realizado com sucesso")
        
        # 2. Buscar dispositivo
        devices_url = f"{THINGSBOARD_HOST}/api/tenant/devices?pageSize=10&page=0"
        response = requests.get(devices_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Erro ao buscar dispositivos: {response.status_code}")
            return
        
        devices = response.json()["data"]
        print(f"📡 Encontrados {len(devices)} dispositivos")
        
        thermal_device = None
        for device in devices:
            if "Térmico" in device["name"] or "Thermal" in device["name"]:
                thermal_device = device
                print(f"🌡️ Dispositivo encontrado: {device['name']}")
                break
        
        if not thermal_device:
            print("❌ Dispositivo térmico não encontrado")
            print("💡 Dispositivos disponíveis:")
            for device in devices:
                print(f"   - {device['name']}")
            return
        
        device_id = thermal_device["id"]["id"]
        
        # 3. Verificar telemetria
        telemetry_url = f"{THINGSBOARD_HOST}/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries"
        response = requests.get(telemetry_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            telemetry = response.json()
            print("📊 Dados de telemetria encontrados:")
            
            for key, values in telemetry.items():
                if values:
                    latest_value = values[0]["value"]
                    latest_time = datetime.fromtimestamp(values[0]["ts"]/1000)
                    print(f"   📈 {key}: {latest_value} (último: {latest_time})")
                else:
                    print(f"   📈 {key}: Sem dados")
            
            # Verificar keys importantes
            important_keys = ["temperature", "humidity", "wind_velocity", "thermal_sensation", "comfort_zone"]
            missing_keys = [key for key in important_keys if key not in telemetry]
            
            if not missing_keys:
                print("\n🎉 PERFEITO! Todos os dados necessários estão disponíveis!")
                print("✅ Você pode criar o dashboard agora!")
                print("\n📋 Próximos passos:")
                print("1. Acesse: http://localhost:8080")
                print("2. Login: tenant@thingsboard.org / tenant")
                print("3. Dashboards → Add new dashboard")
                print("4. Siga o guia: GUIA_DASHBOARD_THINGSBOARD.md")
            else:
                print(f"\n⚠️ Keys faltando: {missing_keys}")
                
        else:
            print(f"❌ Erro ao obter telemetria: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

def show_dashboard_guide():
    """Mostrar resumo do guia do dashboard"""
    print("\n" + "="*50)
    print("📖 GUIA RÁPIDO PARA CRIAR DASHBOARD")
    print("="*50)
    
    widgets = [
        ("🌡️ Temperatura", "Simple Card", "Mostra temperatura atual"),
        ("💧 Umidade", "Simple Card", "Monitora umidade relativa"),
        ("🌬️ Vento", "Radial Gauge", "Velocidade do vento"),
        ("🎯 Sensação Térmica", "Simple Card", "Como o corpo sente"),
        ("🏠 Zona Conforto", "Simple Card", "Classificação de conforto"),
        ("📈 Tendências", "Time Series", "Gráfico temporal"),
        ("🌅 Radiação Solar", "Bar Chart", "Intensidade solar"),
        ("🏠 Distribuição", "Pie Chart", "% tempo em cada zona")
    ]
    
    for name, widget_type, description in widgets:
        print(f"{name:<20} | {widget_type:<15} | {description}")
    
    print("\n🔗 URLs Importantes:")
    print("📊 ThingsBoard: http://localhost:8080")
    print("📖 API Docs: http://localhost:8060/docs")
    print("📋 Guia completo: GUIA_DASHBOARD_THINGSBOARD.md")

if __name__ == "__main__":
    check_thingsboard_data()
    show_dashboard_guide()