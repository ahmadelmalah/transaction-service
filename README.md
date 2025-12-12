# Transaction Service

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Tests](https://img.shields.io/badge/tests-15%20passed-success.svg)

A FastAPI-based REST API for managing financial transactions and customer summaries.

## Overview

This project showcases a well-structured FastAPI application with:

- **Clean separation of concerns** – routes, models, and data layers are properly organized
- **Comprehensive testing** – 15 test cases covering endpoints, validation, and edge cases
- **Type safety** – Pydantic models with enum validation for transaction statuses
- **Auto-generated docs** – Swagger UI and ReDoc interfaces included
- **RESTful design** – Proper HTTP status codes and error handling

The implementation uses mock data to keep things simple, but the architecture is designed to easily swap in a real database layer.

---

## Features

- List transactions with filtering by status, customer ID, and configurable limits
- Get customer summaries with transaction counts and total amounts
- Request validation with clear error messages for invalid inputs
- Interactive API documentation at `/docs` and `/redoc`

---

## Project Structure

```
transaction-service/
├── app/
│   ├── main.py                 # FastAPI app setup
│   ├── models/                 # Pydantic models
│   │   ├── transaction.py      # Transaction model + TransactionStatus enum
│   │   └── summary.py
│   ├── routes/                 # API endpoints
│   │   ├── transactions.py
│   │   └── customers.py
│   └── data/
│       └── mock_data.py        # In-memory transaction data
├── tests/
│   ├── test_transactions.py    # 10 tests
│   └── test_customers.py       # 5 tests
├── requirements.txt
└── README.md
```

---

## Installation

You'll need Python 3.10 or later.

**1. Clone and navigate:**
```bash
git clone https://github.com/ahmadelmalah/transaction-service.git
cd transaction-service
```

**2. Create and activate a virtual environment:**
```bash
python3 -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
# Make sure the virtual environment is activated
source myenv/bin/activate

# Start the server
uvicorn app.main:app --reload
```

The API will be running at `http://localhost:8000`

**Interactive docs:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## API Endpoints

### Transactions

**`GET /transactions/`**

Retrieve transactions with optional filtering.

| Parameter | Type | Default | Constraints | Description |
|-----------|------|---------|-------------|-------------|
| `status` | TransactionStatus | - | `completed`, `pending`, `failed` | Filter by status |
| `customer_id` | int | - | Positive integer | Filter by customer |
| `limit` | int | 100 | 1-1000 | Max results to return |

**Examples:**
```bash
curl http://localhost:8000/transactions
curl "http://localhost:8000/transactions?status=completed"
curl "http://localhost:8000/transactions?customer_id=10&limit=5"
```

**Response:**
```json
[
  {
    "id": 1,
    "customer_id": 10,
    "amount": 100.0,
    "currency": "GBP",
    "status": "completed"
  }
]
```

**Error responses:**
- `422` – Invalid parameters (e.g., invalid status, limit out of range)

### Customers

**`GET /customers/{customer_id}/summary`**

Get aggregated summary for a customer.

**Example:**
```bash
curl http://localhost:8000/customers/10/summary
```

**Response:**
```json
{
  "customer_id": 10,
  "total_transactions": 2,
  "total_amount": 150.0
}
```

**Error responses:**
- `404` – Customer not found or has no transactions
- `422` – Invalid customer_id

### Health Check

**`GET /`**

```bash
curl http://localhost:8000/
```

Returns `{"message": "It Works!"}` to verify the service is running.

---

## Running Tests

The test suite has 15 tests covering all endpoints, validation logic, and edge cases.

**Activate the virtual environment first** (I always forget this step):
```bash
source myenv/bin/activate
```

**Run all tests:**
```bash
pytest -v
```

**Or without activating:**
```bash
myenv/bin/pytest -v
```

**Run specific tests:**
```bash
pytest tests/test_transactions.py
pytest tests/test_customers.py::test_customer_summary_not_found -v
```

### What's Tested

**Transaction endpoints:**
- Filtering by status, customer_id, and combinations
- Limit parameter validation (lower/upper bounds)
- Invalid enum values return 422

**Customer endpoints:**
- Summary aggregation for single/multiple transactions
- 404 handling for non-existent customers
- Invalid customer_id validation

All 15 tests currently passing.

---

## Data Models

### Transaction
```python
{
  "id": int,
  "customer_id": int,
  "amount": float,
  "currency": str,              # e.g., "GBP", "EUR"
  "status": TransactionStatus   # enum: "completed", "pending", "failed"
}
```

The `TransactionStatus` enum ensures only valid statuses are accepted. Invalid values are rejected with a 422 error.

### Summary
```python
{
  "customer_id": int,
  "total_transactions": int,    # Count of all transactions
  "total_amount": float         # Sum across all statuses
}
```

Note: Summaries include transactions with all statuses (completed, pending, and failed).

---

## Production Considerations

This is a demo project, but for production deployment you'd want to add:

**Infrastructure:**
- Database layer with proper indexing on `customer_id` and `status`
- Docker containerization
- CI/CD pipeline with automated testing

**Security:**
- Authentication (JWT tokens)
- Rate limiting
- Input sanitization beyond basic validation

**Observability:**
- Structured logging
- Metrics
- Error tracking (Sentry)

**API improvements:**
- Pagination for large result sets
- API versioning (`/v1/transactions`)
- Date range filtering
- Transaction creation/update endpoints (`POST`, `PATCH`)

The current architecture would support these additions without major refactoring.

---

## Dependencies

Main packages:
- **FastAPI** (0.124.4) – Web framework
- **Uvicorn** (0.38.0) – ASGI server
- **Pydantic** (2.12.5) – Data validation
- **pytest** (9.0.2) – Testing

See `requirements.txt` for the complete list.
