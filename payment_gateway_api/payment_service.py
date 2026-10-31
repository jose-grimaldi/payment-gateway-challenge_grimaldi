import logging
from uuid import uuid4

from payment_gateway_api.bank_service import BankService
from payment_gateway_api.exceptions import InvalidPaymentParameterError, PaymentNotFoundError
from payment_gateway_api.models import PaymentResponse, PaymentRequest
from payment_gateway_api.models import PaymentStatus
from payment_gateway_api.payment_repository import PaymentRepository
from payment_gateway_api.payment_validator import PaymentValidator

logger = logging.getLogger(__name__)


class PaymentService:

    def __init__(self, bank_service: BankService, payment_repository: PaymentRepository):
        self.bank_service = bank_service
        self.payment_repository = payment_repository

    def process_payment(self, payment: PaymentRequest) -> PaymentResponse:
        """
        Main function allowing to create a PaymentRequest from a payload and then process the payment calling the
        BankService. Create a PaymentResponse with the status based on the response of the BankService
        """

        logger.info("Starting processing payment")

        if not PaymentValidator().validate_payment(payment):
            logger.error("Payment invalid, unable to execute")
            raise InvalidPaymentParameterError()

        logger.info("Payment validated")

        bank_response = self.bank_service.process_payment(payment)

        status = PaymentStatus.AUTHORIZED.value if bank_response["authorized"] else PaymentStatus.DECLINED.value

        payment_response = PaymentResponse(
            id=str(uuid4()),
            status=status,
            last_four_card_digits=payment.card_number[-4:],
            expiry_month=payment.expiry_month,
            expiry_year=payment.expiry_year,
            currency=payment.currency,
            amount=payment.amount
        )

        logger.info("Payment processed by bank: id=%s, status=%s", payment_response.id,
                    payment_response.status)

        self.payment_repository.save(payment_response)

        logger.info("Payment saved in repo")

        return payment_response

    def get_payment(self, payment_id: str) -> PaymentResponse:

        payment = self.payment_repository.get_by_id(payment_id)

        if payment is None:
            logger.error("Payment was not found in Repo")
            raise PaymentNotFoundError(payment_id)

        return payment
