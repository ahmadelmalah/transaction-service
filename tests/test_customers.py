from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


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
