import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Arivu Supply Chain API"}


def test_inventory_add_and_get():
    item = {"id": 1, "name": "Flour", "quantity": 10}
    add_resp = client.post("/inventory/", json=item)
    assert add_resp.status_code == 200
    get_resp = client.get("/inventory/1")
    assert get_resp.json()["name"] == "Flour"
