# app/routes/transactions.py
import logging
from fastapi import APIRouter, Query
from typing import List, Optional
from app.models.transaction import Transaction, TransactionStatus
from app.data.mock_data import TRANSACTIONS

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=List[Transaction])
def get_transactions(
    status: Optional[TransactionStatus] = None,
    customer_id: Optional[int] = None,
    limit: int = Query(default=100, gt=0, le=1000),
):
    """Retrieve transactions with optional filtering by status, customer_id, and limit."""
    logger.info(f"Fetching transactions: status={status}, customer_id={customer_id}, limit={limit}")
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
