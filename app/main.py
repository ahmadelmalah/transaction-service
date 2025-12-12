from fastapi import FastAPI
from app.routes import transactions, customers

app = FastAPI()


# Basic health check endpoint
@app.get("/")
def read_root():
    """Health check endpoint"""
    return {"message": "It Works!"}


# Include transaction routes
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])

# Include customer routes
app.include_router(customers.router, prefix="/customers", tags=["customers"])
