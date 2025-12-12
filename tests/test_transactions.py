from fastapi.testclient import TestClient
from main import app

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


def test_customer_summary_success():
    # Customer 10 has 100.0 + 50.0 = 150.0
    response = client.get("/customers/10/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == 10
    assert data["total_transactions"] == 2
    assert data["total_amount"] == 150.0


def test_customer_summary_not_found():
    # Customer 999 does not exist in the static data
    response = client.get("/customers/999/summary")
    assert response.status_code == 404
    assert response.json()["detail"] == "Customer 999 not found or has no transactions."
