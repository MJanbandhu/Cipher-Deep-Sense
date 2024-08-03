from flask import Flask, request, abort
import os

app = Flask(__name__)

def validate_api_key(api_key):
    # Implement API key validation logic
    return True

@app.route('/api/data', methods=['GET'])
def get_data():
    api_key = request.headers.get('Authorization')
    if not validate_api_key(api_key):
        abort(401)
    # Fetch and return data