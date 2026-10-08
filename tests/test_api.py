from fastapi.testclient import TestClient
import sys
import os

# Ensure the parent directory is in the path so we can import main
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app

client = TestClient(app)

def test_read_main():
    """Test if the main frontend endpoint returns a 200 OK status."""
    response = client.get("/")
    assert response.status_code == 200

def test_react_validation_handling():
    """Test if the API properly handles incoming data by rejecting invalid short text."""
    # Text length 2 is less than the required min_length of 5
    response = client.post("/react", json={"text": "hi"})
    assert response.status_code == 422
