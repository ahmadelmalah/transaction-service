from fastapi import FastAPI, HTTPException, Query
from app.models.transaction import Transaction
from app.models.summary import Summary
from typing import List, Optional
from app.data.mock_data import TRANSACTIONS


app = FastAPI()


# Basic health check endpoint
@app.get("/")
def read_root():
    return {"It": "Works!"}


# Endpoint to get transactions with optional filtering
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


# Endpoint to get summary for a specific customer
@app.get("/customers/{customer_id}/summary", response_model=Summary)
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

    return Summary(
        customer_id=customer_id,
        total_transactions=total_transactions,
        total_amount=total_amount,
    )
