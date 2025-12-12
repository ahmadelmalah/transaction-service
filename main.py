from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

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


@app.get("/")
def read_root():
    return {"It": "Works!"}


@app.get("/transactions/")
def get_transactions(customer_id: Union[int, None] = None):
    if customer_id is not None:
        filtered_transactions = [
            tx for tx in TRANSACTIONS if tx["customer_id"] == customer_id
        ]
        return {"transactions": filtered_transactions}
    return {"transactions": TRANSACTIONS}
