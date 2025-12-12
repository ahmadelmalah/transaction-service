from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# Basic functionality tests
def test_list_transactions_no_filter():
    # Should return all transactions
    response = client.get("/transactions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert data[0]["id"] == 1


def test_list_transactions_filter_status():
    # Filter by status
    response = client.get("/transactions?status=pending")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == "pending"


def test_list_transactions_filter_customer():
    # Filter by customer_id
    response = client.get("/transactions?customer_id=20")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(t["customer_id"] == 20 for t in data)


def test_list_transactions_limit():
    # Apply limit parameter
    response = client.get("/transactions?limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2


# Limit validation tests
def test_list_transactions_limit_lower_bound():
    # Limit must be > 0
    response = client.get("/transactions?limit=0")
    assert response.status_code == 422


def test_list_transactions_limit_upper_bound():
    # Limit must be <= 1000, so 1000 is valid
    response = client.get("/transactions?limit=1000")
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_list_transactions_limit_exceeds_max():
    # Limit exceeds maximum allowed (1000)
    response = client.get("/transactions?limit=1001")
    assert response.status_code == 422


# Combined filter tests
def test_list_transactions_combined_filters():
    # Combine status and customer_id filters
    response = client.get("/transactions?status=completed&customer_id=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["customer_id"] == 10
    assert data[0]["status"] == "completed"


def test_list_transactions_all_filters():
    # Combine all three filters: status, customer_id, and limit
    response = client.get("/transactions?status=completed&customer_id=10&limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["customer_id"] == 10
    assert data[0]["status"] == "completed"


# Edge case tests
def test_list_transactions_nonexistent_status():
    # Non-existent status should be rejected with 422 (validation error)
    response = client.get("/transactions?status=nonexistent")
    assert response.status_code == 422
