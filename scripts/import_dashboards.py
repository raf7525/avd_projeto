import json
import os

import requests

# Configurações
THINGSBOARD_HOST = os.getenv("THINGSBOARD_HOST", "http://localhost:8080")
USERNAME = os.getenv("TB_USER", "tenant@thingsboard.org")
PASSWORD = os.getenv("TB_PASSWORD", "tenant")
DASHBOARD_FILE = "data/thingsboard.json"

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

def import_dashboard(token):
    """Import dashboard from JSON file"""
    if not os.path.exists(DASHBOARD_FILE):
        print(f"❌ Arquivo {DASHBOARD_FILE} não encontrado.")
        return

    try:
        with open(DASHBOARD_FILE, 'r') as f:
            dashboard_data = json.load(f)
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Check if dashboard already exists (by title) to avoid duplicates?
        # ThingsBoard API doesn't easily support "update by name" on import without ID.
        # But we can just save it as a new one.
        
        url = f"{THINGSBOARD_HOST}/api/dashboard"
        
        # The exported JSON structure might differ slightly from the creation payload.
        # Exported JSON usually has "configuration" wrapped.
        # Let's try posting it directly first.
        
        # If the JSON has an ID, remove it to create a new one, or keep it to update?
        # Usually safer to remove 'id' to avoid conflicts if UUIDs don't match system DB.
        if 'id' in dashboard_data:
            del dashboard_data['id']
            
        response = requests.post(url, headers=headers, json=dashboard_data)
        
        if response.status_code == 200:
            print(f"✅ Dashboard '{dashboard_data.get('title', 'Unknown')}' importado com sucesso!")
            print(f"   ID: {response.json().get('id', {}).get('id')}")
        else:
            print(f"❌ Falha ao importar dashboard: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"❌ Erro durante a importação: {e}")

if __name__ == "__main__":
    print("🔄 Iniciando importação automática de dashboards...")
    token = get_token()
    if token:
        import_dashboard(token)
