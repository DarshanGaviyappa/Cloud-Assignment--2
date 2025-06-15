import requests

def test_health_check():
    url = "http://18.226.248.96:8080/index.html"  # Updated IP
    response = requests.get(url, timeout=5)
    assert response.status_code == 200