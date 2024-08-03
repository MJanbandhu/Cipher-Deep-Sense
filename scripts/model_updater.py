import requests
import time

def update_model_periodically(interval):
    while True:
        try:
            response = requests.get('http://localhost:5000/api/update-model')  # Update with your server endpoint
            if response.status_code == 200:
                print("Model updated successfully.")
            else:
                print(f"Error updating model: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(interval)

if __name__ == "__main__":
    update_model_periodically(interval=60)  # Update model every 60 seconds
