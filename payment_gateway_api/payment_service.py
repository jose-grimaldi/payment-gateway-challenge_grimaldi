from uuid import uuid4

from payment_gateway_api.bank_service import BankService
from payment_gateway_api.exceptions import InvalidPaymentParameterError
from payment_gateway_api.models import PaymentResponse, PaymentRequest
from payment_gateway_api.payment_repository import PaymentRepository
from payment_gateway_api.payment_validator import PaymentValidator


class PaymentService:

    def __init__(self, bank_service: BankService, payment_repository: PaymentRepository):
        self.bank_service = bank_service
        self.payment_repository = payment_repository

    @staticmethod
    def create_payment_request(payload: dict) -> PaymentRequest:
        """
        Function allowing to take a payload dict and transform it to a PaymentRequest object
        If there are missing fields the object will not be created and an exception will be raised
        """

        payment = PaymentRequest(
            card_number=payload["card_number"],
            expiry_month=payload["expiry_month"],
            expiry_year=payload["expiry_year"],
            currency=payload["currency"],
            amount=payload["amount"],
            cvv=payload["cvv"]
        )

        return payment

    def process_payment(self, payload: dict):
        payment = self.create_payment_request(payload)

        if not PaymentValidator().validate_payment(payment):
            raise InvalidPaymentParameterError()

        bank_response = self.bank_service.process_payment(payment)

        status = "Authorized" if bank_response["authorized"] else "Declined"

        payment_response = PaymentResponse(
            id=str(uuid4()),
            status=status,
            last_four_card_digits=payment.card_number[-4:],
            expiry_month=payment.expiry_month,
            expiry_year=payment.expiry_year,
            currency=payment.currency,
            amount=payment.amount
        )

        self.payment_repository.save(payment_response)

        return payment_response
