import requests
import os

def test_health():
    url = os.getenv("BACKEND_URL", "http://backend:8000/health")
    r = requests.get(url)
    assert r.status_code == 200
    j = r.json()
    assert "ready" in j
