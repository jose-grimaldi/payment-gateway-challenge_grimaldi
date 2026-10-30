"""
Class allowing to handle the bank operations, connection to the simulator
"""
import requests

from payment_gateway_api.config import BANK_SIMULATOR_URL_BASE
from payment_gateway_api.models import PaymentRequest


class BankService:

    def __init__(self):
        self.url = f"{BANK_SIMULATOR_URL_BASE}/payments"

    def process_payment(self, payment: PaymentRequest):
        response = requests.post(
            self.url,
            json=payment.to_dict(),
            timeout=5
        )

        if response.status_code == 503:
            raise ConnectionError("Bank simulator unavailable")

        response.raise_for_status()

        return response.json()
