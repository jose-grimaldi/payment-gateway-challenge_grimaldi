from dataclasses import asdict

from fastapi import FastAPI, HTTPException, Request

from payment_gateway_api.bank_service import BankService
from payment_gateway_api.exceptions import (PaymentNotFoundError, MissingPaymentRequestParameterError,
                                            InvalidPaymentParameterError)
from payment_gateway_api.models import PaymentRequest
from payment_gateway_api.payment_repository import PaymentRepository
from payment_gateway_api.payment_service import PaymentService

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


@app.post("/payments")
async def create_payment(request: Request):
    """
    Endpoint allowing to create a payment and to execute it
    """
    try:
        payload = await request.json()

        payload.update({"expiry_month": payload['expiry_date'].split('/')[0],
                        "expiry_year": payload['expiry_date'].split('/')[1]})
        payload.pop('expiry_date')

        payment = PaymentRequest(**payload)

        response = payment_service.process_payment(payment)

        return asdict(response)

    except (TypeError, MissingPaymentRequestParameterError) as error:
        raise HTTPException(status_code=400, detail=str(error))

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
