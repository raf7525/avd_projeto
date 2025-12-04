import json
import requests
import os

# Configurações
THINGSBOARD_HOST = os.getenv("THINGSBOARD_HOST", "http://localhost:8080")
USERNAME = os.getenv("TB_USER", "tenant@thingsboard.org")
PASSWORD = os.getenv("TB_PASSWORD", "tenant")

def get_token():
    """Login to ThingsBoard and get JWT token"""
    url = f"{THINGSBOARD_HOST}/api/auth/login"
    try:
        response = requests.post(url, json={"username": USERNAME, "password": PASSWORD})
        response.raise_for_status()
        return response.json().get("token")
    except Exception as e:
        print(f"❌ Erro no login: {e}")
        return None

def list_dashboards(token):
    """List dashboards in ThingsBoard"""
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{THINGSBOARD_HOST}/api/tenant/dashboards?pageSize=100&page=0" # Get up to 100 dashboards
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        dashboards = response.json().get("data", [])
        
        print("\n📊 Dashboards encontrados no ThingsBoard:")
        if not dashboards:
            print("   (Nenhum dashboard)")
            return False
            
        found_inmet_dashboard = False
        for db in dashboards:
            print(f"   - {db.get('title')} (ID: {db.get('id', {}).get('id')})")
            if db.get('title') == "Dashboard INMET":
                found_inmet_dashboard = True
        
        if found_inmet_dashboard:
            print("\n✅ Dashboard 'Dashboard INMET' encontrado na lista!")
            return True
        else:
            print("\n❌ Dashboard 'Dashboard INMET' NÃO encontrado na lista.")
            return False

    except Exception as e:
        print(f"❌ Erro ao listar dashboards: {e}")
        return False

if __name__ == "__main__":
    token = get_token()
    if token:
        list_dashboards(token)
