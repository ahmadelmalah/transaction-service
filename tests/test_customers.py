from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_customer_summary_multiple_transactions():
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


def test_customer_summary_single_transaction():
    # Customer 30 has only 1 transaction for 300.0
    response = client.get("/customers/30/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == 30
    assert data["total_transactions"] == 1
    assert data["total_amount"] == 300.0


def test_customer_summary_invalid_customer_id():
    # Passing a string instead of int should return 422
    response = client.get("/customers/invalid/summary")
    assert response.status_code == 422


def test_customer_summary_includes_all_statuses():
    # Customer 20 has completed (200.0) + failed (25.0) = 225.0
    # Verifies that all transaction statuses are included in totals
    response = client.get("/customers/20/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_amount"] == 225.0  # Both completed and failed included
