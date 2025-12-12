from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

TRANSACTIONS = [
    {
        "id": 1,
        "customer_id": 10,
        "amount": 100.0,
        "currency": "GBP",
        "status": "completed",
    },
    {
        "id": 2,
        "customer_id": 10,
        "amount": 50.0,
        "currency": "GBP",
        "status": "pending",
    },
    {
        "id": 3,
        "customer_id": 20,
        "amount": 200.0,
        "currency": "EUR",
        "status": "completed",
    },
    {"id": 4, "customer_id": 20, "amount": 25.0, "currency": "EUR", "status": "failed"},
    {
        "id": 5,
        "customer_id": 30,
        "amount": 300.0,
        "currency": "GBP",
        "status": "completed",
    },
]


class Transaction(BaseModel):
    id: int
    customer_id: int
    amount: float
    currency: str
    status: str


class CustomerSummary(BaseModel):
    customer_id: int
    total_transactions: int
    total_amount: float


@app.get("/")
def read_root():
    return {"It": "Works!"}


@app.get("/transactions/", response_model=List[Transaction])
def get_transactions(
    status: Optional[str] = None,
    customer_id: Optional[int] = None,
    # Limit cap: enforce sensible bounds (e.g., 1 to 1000)
    limit: int = Query(default=100, gt=0, le=1000),
):
    filtered_transactions = TRANSACTIONS

    # Filter by status if provided
    if status is not None:
        filtered_transactions = [
            transaction
            for transaction in filtered_transactions
            if transaction["status"] == status
        ]

    # Filter by customer_id if provided
    if customer_id is not None:
        filtered_transactions = [
            transaction
            for transaction in filtered_transactions
            if transaction["customer_id"] == customer_id
        ]

    # Apply limit and return results
    return filtered_transactions[:limit]


@app.get("/customers/{customer_id}/summary", response_model=CustomerSummary)
def get_customer_summary(customer_id: int):
    # Find all transactions for the specific customer
    customer_transactions = [
        transaction
        for transaction in TRANSACTIONS
        if transaction["customer_id"] == customer_id
    ]

    # If no transactions exist, return 404
    if not customer_transactions:
        raise HTTPException(
            status_code=404,
            detail=f"Customer {customer_id} not found or has no transactions.",
        )

    # Calculate summary
    total_transactions = len(customer_transactions)
    total_amount = sum(transaction["amount"] for transaction in customer_transactions)

    return CustomerSummary(
        customer_id=customer_id,
        total_transactions=total_transactions,
        total_amount=total_amount,
    )
