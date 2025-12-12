from pydantic import BaseModel


class Summary(BaseModel):
    customer_id: int
    total_transactions: int
    total_amount: float
