import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi.testclient import TestClient

from supply_chain_system.main import app

client = TestClient(app)

def test_root_serves_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_inventory_add_and_get():
    item = {"id": 1, "name": "Flour", "quantity": 10}
    add_resp = client.post("/inventory/", json=item)
    assert add_resp.status_code == 200
    get_resp = client.get("/inventory/1")
    assert get_resp.json()["name"] == "Flour"


def test_register_and_login():
    reg = client.post("/auth/register", params={"username": "test", "password": "pass"})
    assert reg.status_code == 200
    log = client.post("/auth/login", params={"username": "test", "password": "pass"})
    assert log.status_code == 200
    assert "token" in log.json()
