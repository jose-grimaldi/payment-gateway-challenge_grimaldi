"""
Class simulating a Repository/DB
"""

from payment_gateway_api.models import PaymentResponse


class PaymentRepository:

    def __init__(self):
        self.payments = {}

    def save(self, payment: PaymentResponse):
        self.payments[payment.id] = payment

    def get_by_id(self, payment_id: str) -> PaymentResponse | None:
        return self.payments.get(payment_id, None)
