# scripts/utils.py

def load_config(file_path):
    """Load configuration from a file."""
    import json
    with open(file_path, 'r') as f:
        config = json.load(f)
    return config