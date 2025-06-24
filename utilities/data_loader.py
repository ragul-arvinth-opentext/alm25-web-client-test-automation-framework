# utilities/data_loader.py
import json

def load_test_data(filepath="test_data/test_data.json"):
    with open(filepath) as f:
        return json.load(f)
