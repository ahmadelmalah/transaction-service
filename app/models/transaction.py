from enum import Enum
from pydantic import BaseModel


class TransactionStatus(str, Enum):
    """Enum for valid transaction statuses."""
    COMPLETED = "completed"
    PENDING = "pending"
    FAILED = "failed"


class Transaction(BaseModel):
    id: int
    customer_id: int
    amount: float
    currency: str
    status: TransactionStatus
