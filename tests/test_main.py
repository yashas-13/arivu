import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi.testclient import TestClient

from supply_chain_system.main import app

def test_root_serves_html():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


def test_inventory_add_and_get():
    with TestClient(app) as client:
        item = {"id": 99, "name": "TestItem", "quantity": 10}
        add_resp = client.post("/inventory/", json=item)
        assert add_resp.status_code == 200
        get_resp = client.get("/inventory/99")
        assert get_resp.json()["name"] == "TestItem"


def test_register_and_login():
    with TestClient(app) as client:
        reg = client.post("/auth/register", params={"username": "test", "password": "pass"})
        assert reg.status_code == 200
        log = client.post("/auth/login", params={"username": "test", "password": "pass"})
        assert log.status_code == 200
        assert "token" in log.json()


def test_dashboards():
    with TestClient(app) as client:
        client.post("/customers", json={"id": 1, "name": "Store"})
        client.post("/inventory", json={"id": 100, "name": "Widget", "quantity": 3})
        client.post("/orders", json={"id": 1, "customer_id": 1, "items": [100]})
        client.post("/invoices", json={"id": 1, "customer_id": 1, "amount": 50.0})

        admin_resp = client.get("/dashboard/admin")
        assert admin_resp.status_code == 200
        data = admin_resp.json()
        assert data["total_sales"] == 50.0
        assert data["low_stock"][0]["product_id"] == 100

        retailer_resp = client.get("/dashboard/retailer/1")
        assert retailer_resp.status_code == 200
        rdata = retailer_resp.json()
        assert rdata["spend"] == 50.0
