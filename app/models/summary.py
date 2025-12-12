from pydantic import BaseModel


class Summary(BaseModel):
    """Customer transaction summary with count and total amount."""
    customer_id: int
    total_transactions: int
    total_amount: float
