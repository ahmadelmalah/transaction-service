from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_transactions_no_filter():
    response = client.get("/transactions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert data[0]["id"] == 1


def test_list_transactions_filter_status():
    response = client.get("/transactions?status=pending")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == "pending"


def test_list_transactions_filter_customer():
    response = client.get("/transactions?customer_id=20")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(t["customer_id"] == 20 for t in data)


def test_list_transactions_limit():
    # Request limit of 2
    response = client.get("/transactions?limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_transactions_limit_validation():
    # Request limit > 1000 should fail validation
    response = client.get("/transactions?limit=1001")
    assert response.status_code == 422  # Unprocessable Entity
