from pydantic import BaseModel


class Transaction(BaseModel):
    id: int
    customer_id: int
    amount: float
    currency: str
    status: str
