import requests

def call_web_service(endpoint, method='GET', data=None):
    url = f"http://127.0.0.1:5000/{endpoint}"
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