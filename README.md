# Transaction Service

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.124.4-green.svg)
![Tests](https://img.shields.io/badge/tests-15%20passed-success.svg)
![Code Style](https://img.shields.io/badge/code%20style-type--safe-brightgreen.svg)

A production-ready FastAPI-based REST API service for managing and querying financial transactions and customer summaries. Built as an interview assessment demonstrating clean architecture, comprehensive testing, and modern Python development practices.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Technical Highlights](#technical-highlights)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Example Usage](#example-usage)
- [Running Tests](#running-tests)
- [Data Model](#data-model)
- [Production Considerations](#production-considerations)

---

## Project Overview

This is an interview assessment project demonstrating a clean, well-architected REST API built with FastAPI. The project showcases:

- **Clean Architecture**: Separation of concerns with organized routes, models, and data layers
- **Comprehensive Testing**: 15 test cases covering happy paths, edge cases, and validation scenarios
- **Input Validation**: Type-safe query parameters with Pydantic models and enum constraints
- **API Design**: RESTful endpoints with proper error handling and response modeling
- **Code Quality**: Type hints, docstrings, and adherence to Python best practices

---

## Technical Highlights

This implementation demonstrates key software engineering principles:

- **Type Safety**: Pydantic models with strict type validation and `TransactionStatus` enum
- **Request Validation**: FastAPI automatic validation with meaningful error messages (422 status codes)
- **Test-Driven Development**: 15 comprehensive test cases with 100% endpoint coverage
- **Proper Error Handling**: RESTful HTTP status codes (200, 404, 422)
- **Code Organization**: Modular structure following separation of concerns
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Developer Experience**: Type hints enable IDE autocomplete and early error detection

---

## Features

- **Get Transactions**: Retrieve all transactions with optional filtering by status, customer ID, and result limiting
- **Customer Summary**: Get transaction summaries for specific customers including transaction count and total amount
- **Automatic Validation**: Invalid inputs are caught at the API layer with clear error messages
- **Interactive Documentation**: Built-in Swagger UI and ReDoc interfaces

---

## Project Structure

```
transaction-service/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application and routing setup
│   ├── models/                 # Pydantic data models
│   │   ├── __init__.py
│   │   ├── transaction.py      # Transaction model with TransactionStatus enum
│   │   └── summary.py          # Summary model
│   ├── routes/                 # API route handlers
│   │   ├── __init__.py
│   │   ├── transactions.py     # Transaction endpoints
│   │   └── customers.py        # Customer endpoints
│   └── data/                   # Data storage
│       ├── __init__.py
│       └── mock_data.py        # Mock transaction data
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_transactions.py    # Transaction endpoint tests (10 tests)
│   └── test_customers.py       # Customer endpoint tests (5 tests)
├── myenv/                      # Virtual environment (not committed)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## Installation

### Prerequisites

- **Python 3.10+**
- **pip** (Python package installer)
- **git** (for cloning the repository)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ahmadelmalah/transaction-service.git
   cd transaction-service
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv myenv
   ```

3. **Activate the virtual environment:**
   ```bash
   # On Linux/macOS:
   source myenv/bin/activate
   
   # On Windows:
   myenv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Application

Start the development server with hot-reload:

```bash
# Make sure your virtual environment is activated
source myenv/bin/activate

# Start the server
uvicorn app.main:app --reload
```

The API will be available at **`http://localhost:8000`**

### Interactive API Documentation

Once the server is running, you can explore the API using:

- **Swagger UI**: http://localhost:8000/docs (interactive testing interface)
- **ReDoc**: http://localhost:8000/redoc (beautiful API documentation)

---

## API Endpoints

### Health Check

#### `GET /`
Verify that the service is running.

**Response:**
```json
{
  "message": "It Works!"
}
```

---

### Transactions

#### `GET /transactions/`
Retrieve all transactions with optional filtering.

**Query Parameters:**
| Parameter | Type | Required | Default | Constraints | Description |
|-----------|------|----------|---------|-------------|-------------|
| `status` | `TransactionStatus` | No | - | `completed`, `pending`, `failed` | Filter by transaction status |
| `customer_id` | `int` | No | - | Positive integer | Filter by customer ID |
| `limit` | `int` | No | `100` | 1-1000 | Maximum number of results |

**Example Requests:**
```
GET /transactions
GET /transactions?status=completed
GET /transactions?customer_id=10
GET /transactions?status=completed&customer_id=10&limit=50
```

**Success Response (200):**
```json
[
  {
    "id": 1,
    "customer_id": 10,
    "amount": 100.0,
    "currency": "GBP",
    "status": "completed"
  },
  {
    "id": 2,
    "customer_id": 10,
    "amount": 50.0,
    "currency": "GBP",
    "status": "pending"
  }
]
```

**Error Responses:**
- **422 Unprocessable Entity**: Invalid parameters (e.g., `status=invalid`, `limit=0`, `limit=1001`)

---

### Customers

#### `GET /customers/{customer_id}/summary`
Get aggregated transaction summary for a specific customer.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `customer_id` | `int` | Yes | Customer ID |

**Example Request:**
```
GET /customers/10/summary
```

**Success Response (200):**
```json
{
  "customer_id": 10,
  "total_transactions": 2,
  "total_amount": 150.0
}
```

**Error Responses:**
- **404 Not Found**: Customer not found or has no transactions
- **422 Unprocessable Entity**: Invalid customer_id (non-integer value)

---

## Example Usage

### Using curl

**Get all transactions:**
```bash
curl http://localhost:8000/transactions
```

**Filter by status:**
```bash
curl "http://localhost:8000/transactions?status=completed"
```

**Filter by customer and limit results:**
```bash
curl "http://localhost:8000/transactions?customer_id=10&limit=5"
```

**Get customer summary:**
```bash
curl http://localhost:8000/customers/10/summary
```

**Test validation (returns 422 error):**
```bash
curl "http://localhost:8000/transactions?status=invalid"
```

### Using Python requests

```python
import requests

# Get all completed transactions
response = requests.get(
    "http://localhost:8000/transactions",
    params={"status": "completed"}
)
transactions = response.json()

# Get customer summary
response = requests.get(
    "http://localhost:8000/customers/10/summary"
)
summary = response.json()
print(f"Total amount: {summary['total_amount']}")
```

---

## Running Tests

The test suite includes 15 comprehensive tests covering all endpoints, validation scenarios, and edge cases.

### Activate Virtual Environment First

```bash
# On Linux/macOS:
source myenv/bin/activate

# On Windows:
myenv\Scripts\activate
```

### Run All Tests

```bash
pytest
```

**Or run without activating the virtual environment:**
```bash
myenv/bin/pytest
```

### Run Tests with Verbose Output

```bash
pytest -v
```

### Run Specific Test File

```bash
pytest tests/test_transactions.py
pytest tests/test_customers.py
```

### Run a Specific Test

```bash
pytest tests/test_transactions.py::test_list_transactions_filter_status -v
```

---

## Test Coverage

### Transaction Tests (10 tests)
✅ Retrieve all transactions without filters  
✅ Filter by status  
✅ Filter by customer ID  
✅ Apply limit parameter  
✅ Limit validation - lower bound (must be > 0)  
✅ Limit validation - upper bound (1000 is valid)  
✅ Limit validation - exceeds maximum (1001 rejected)  
✅ Combined filters (status + customer_id)  
✅ All filters together (status + customer_id + limit)  
✅ Non-existent status returns validation error (422)  

### Customer Tests (5 tests)
✅ Get summary for customer with multiple transactions  
✅ Get summary for non-existent customer (404)  
✅ Get summary for customer with single transaction  
✅ Invalid customer_id (non-integer) returns 422  
✅ Verify all transaction statuses are included in totals  

**Total: 15/15 tests passing**

---

## Data Model

### Transaction

```python
{
  "id": int,                            # Unique transaction identifier
  "customer_id": int,                   # Customer identifier
  "amount": float,                      # Transaction amount
  "currency": str,                      # Currency code (e.g., "GBP", "EUR")
  "status": TransactionStatus           # Enum: "completed", "pending", or "failed"
}
```

**TransactionStatus Enum:**
```python
class TransactionStatus(str, Enum):
    COMPLETED = "completed"
    PENDING = "pending"
    FAILED = "failed"
```

### Summary

```python
{
  "customer_id": int,                   # Customer identifier
  "total_transactions": int,            # Count of all transactions for this customer
  "total_amount": float                 # Sum of transaction amounts (all statuses included)
}
```

**Note:** The summary includes transactions with **all statuses** (completed, pending, and failed).

---

## Production Considerations

For a production deployment, the following enhancements would be essential:

### Infrastructure
- **Database Integration**: Replace mock data with PostgreSQL or MongoDB
  - Add proper schema migrations (Alembic)
  - Implement connection pooling
  - Add database indexes for query optimization

- **Docker & Orchestration**: 
  - Containerize with Docker
  - Use docker-compose for local development
  - Deploy with Kubernetes for scaling

- **CI/CD Pipeline**:
  - Automated testing on pull requests
  - Code coverage reporting (aim for >80%)
  - Automated deployment to staging/production

### Security
- **Authentication & Authorization**: 
  - JWT-based authentication
  - Role-based access control (RBAC)
  - API key management for service-to-service calls

- **Rate Limiting**: Protect endpoints from abuse (e.g., 100 requests/minute per IP)

- **Input Sanitization**: Additional validation layers for security

### Observability
- **Structured Logging**: 
  - JSON-formatted logs with correlation IDs
  - Request/response logging middleware
  - Error tracking with Sentry or similar

- **Monitoring & Metrics**:
  - Prometheus metrics (request count, latency, error rates)
  - Grafana dashboards
  - Health check endpoints for load balancers

- **Distributed Tracing**: OpenTelemetry for request tracing across services

### API Enhancements
- **Pagination**: Cursor-based pagination for large result sets
- **Versioning**: Support multiple API versions (`/v1/transactions`, `/v2/transactions`)
- **CORS Configuration**: Proper CORS headers for web clients
- **Response Compression**: Gzip compression for large payloads
- **Webhooks**: Event-driven notifications for transaction status changes

### Additional Features
- **Transaction Creation**: `POST /transactions` endpoint
- **Transaction Updates**: `PATCH /transactions/{id}` for status updates
- **Transaction Cancellation**: Status transition management
- **Currency Conversion**: Multi-currency support with exchange rates
- **Date Range Filtering**: Filter transactions by date range
- **Advanced Search**: Full-text search capabilities

