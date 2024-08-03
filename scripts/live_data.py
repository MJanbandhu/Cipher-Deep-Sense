import requests

def fetch_live_data():
    response = requests.get('https://your-secure-server.com/api/live-data')
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching live data: {response.status_code}")