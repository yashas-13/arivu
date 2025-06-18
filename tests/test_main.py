import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi.testclient import TestClient

from supply_chain_system.main import app

client = TestClient(app)

def test_root_serves_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_inventory_add_and_get():
    item = {"id": 99, "name": "Flour", "quantity": 10}
    add_resp = client.post("/inventory/", json=item)
    assert add_resp.status_code == 200
    get_resp = client.get("/inventory/99")
    assert get_resp.json()["name"] == "Flour"


def test_inventory_crud():
    initial = client.get("/inventory")
    assert len(initial.json()) >= 3
    item = {"id": 100, "name": "Sugar", "quantity": 5}
    assert client.post("/inventory", json=item).status_code == 200
    updated = {"id": 100, "name": "Sugar", "quantity": 8}
    assert client.put("/inventory/100", json=updated).status_code == 200
    assert client.delete("/inventory/100").status_code == 200
    missing = client.get("/inventory/100")
    assert missing.status_code == 404


def test_register_and_login():
    reg = client.post(
        "/auth/register",
        params={"username": "test", "password": "pass", "role": "retailer"},
    )
    assert reg.status_code == 200
    log = client.post(
        "/auth/login", params={"username": "test", "password": "pass"}
    )
    assert log.status_code == 200
    body = log.json()
    assert "token" in body
    assert body["role"] == "retailer"


def test_dashboards():
    client.post("/customers", json={"id": 1, "name": "Store"})
    client.post("/inventory", json={"id": 1, "name": "Flour", "quantity": 3})
    client.post("/orders", json={"id": 1, "customer_id": 1, "items": [1]})
    client.post("/invoices", json={"id": 1, "customer_id": 1, "amount": 50.0})

    admin_resp = client.get("/dashboard/admin")
    assert admin_resp.status_code == 200
    data = admin_resp.json()
    assert data["total_sales"] == 50.0
    assert data["low_stock"][0]["product_id"] == 1

    retailer_resp = client.get("/dashboard/retailer/1")
    assert retailer_resp.status_code == 200
    rdata = retailer_resp.json()
    assert rdata["spend"] == 50.0
