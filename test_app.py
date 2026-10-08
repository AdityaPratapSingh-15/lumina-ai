from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def run_tests():
    print("Testing GET / ...")
    response = client.get("/")
    print(f"Status: {response.status_code}")
    print(f"Body: {response.text[:50]}...\n")
    
    print("Testing POST /rewrite ...")
    response = client.post("/rewrite", json={"text": "Hey there, just following up on that thing."})
    print(f"Status: {response.status_code}")
    print(f"Body: {response.json()}\n")

if __name__ == "__main__":
    run_tests()
