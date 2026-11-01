import logging
from dataclasses import asdict

from fastapi import FastAPI, HTTPException, Request

from payment_gateway_api.api_docs import CREATE_PAYMENT_OPENAPI
from payment_gateway_api.bank_service import BankService
from payment_gateway_api.config import REQUIRED_FIELDS_PAYLOAD
from payment_gateway_api.exceptions import (PaymentNotFoundError, MissingPaymentRequestParameterError,
                                            InvalidPaymentParameterError)
from payment_gateway_api.models import PaymentRequest
from payment_gateway_api.payment_repository import PaymentRepository
from payment_gateway_api.payment_service import PaymentService

logging.basicConfig(level=logging.INFO)
app = FastAPI()

bank_service = BankService()
payment_repository = PaymentRepository()

payment_service = PaymentService(
    bank_service,
    payment_repository
)


@app.get("/")
async def ping() -> dict[str, str]:
    return {"app": "payment-gateway-api"}


@app.post("/payments", openapi_extra=CREATE_PAYMENT_OPENAPI)
async def create_payment(request: Request):
    """
    Endpoint allowing to create a payment and to execute it
    """
    try:
        payload = await request.json()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid JSON request")

    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Request body must be a JSON object")

    unexpected_fields = set(payload.keys()) - REQUIRED_FIELDS_PAYLOAD
    if unexpected_fields:
        raise HTTPException(status_code=400, detail=f"Unexpected fields: {', '.join(sorted(unexpected_fields))}")

    try:
        payment = PaymentRequest(**payload)
    except (TypeError, MissingPaymentRequestParameterError) as error:
        raise HTTPException(status_code=400, detail=str(error))

    try:
        response = payment_service.process_payment(payment)
        return asdict(response)

    except InvalidPaymentParameterError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except ConnectionError as error:
        raise HTTPException(status_code=503, detail=str(error))


@app.get("/payments/{payment_id}")
async def get_payment(payment_id: str):
    """
    Endpoint allowing to get the response of a payment based on its id
    """
    try:
        payment = payment_service.get_payment(payment_id)
        return asdict(payment)

    except PaymentNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
