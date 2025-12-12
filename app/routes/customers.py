# app/routes/customers.py
from fastapi import APIRouter, HTTPException
from app.models.summary import Summary
from app.data.mock_data import TRANSACTIONS

router = APIRouter()


@router.get("/{customer_id}/summary", response_model=Summary)
def get_customer_summary(customer_id: int):
    """Get transaction count and total amount for a customer."""
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
