import requests
import sys
from pathlib import Path

# Agregar el directorio raíz al path para importar constants
sys.path.append(str(Path(__file__).parent.parent))
from Utils.constants import WEB_SERVICE_URL

def call_web_service(endpoint, method='GET', data=None):
    url = f"{WEB_SERVICE_URL}/{endpoint}"
    try:
        if method == 'GET':
            response = requests.get(url, params=data)
        elif method == 'POST':
            response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json(), response.status_code
    except requests.RequestException as e:
        print(f"Error calling web service: {e}")
        return None, None