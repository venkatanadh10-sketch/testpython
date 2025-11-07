from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import random

app = FastAPI(title="Payment API Example")

# Request model
class PaymentRequest(BaseModel):
    card_number: str
    expiry_date: str
    cvv: str
    amount: float
    currency: str = "USD"

# Response model
class PaymentResponse(BaseModel):
    transaction_id: str
    status: str
    message: str

@app.post("/api/payment", response_model=PaymentResponse)
def process_payment(payment: PaymentRequest):
    # Dummy card validation
    if len(payment.card_number) != 16:
        raise HTTPException(status_code=400, detail="Invalid card number")
    if payment.amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid payment amount")

    # Simulate random payment success/failure
    success = random.choice([True, False])
    transaction_id = str(uuid.uuid4())

    if success:
        return PaymentResponse(
            transaction_id=transaction_id,
            status="Success",
            message=f"Payment of {payment.amount} {payment.currency} processed successfully."
        )
    else:
        return PaymentResponse(
            transaction_id=transaction_id,
            status="Failed",
            message="Payment declined by bank."
        )

# To run:
# uvicorn filename:app --reload

