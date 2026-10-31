"""
Class allowing to handle the bank operations, connection to the simulator
"""
import logging

import requests

from payment_gateway_api.config import BANK_SIMULATOR_URL_BASE
from payment_gateway_api.models import PaymentRequest

logger = logging.getLogger(__name__)


class BankService:

    def __init__(self):
        self.url = f"{BANK_SIMULATOR_URL_BASE}/payments"

    def process_payment(self, payment: PaymentRequest):

        try:
            response = requests.post(
                self.url,
                json=payment.to_dict(),
                timeout=5
            )
        except requests.exceptions.Timeout:
            logger.error("Could not connect to bank: timeout")
            raise ConnectionError('Timeout error')

        if response.status_code == 503:
            logger.error("Could not connect to bank: unavailable")
            raise ConnectionError("Bank simulator unavailable")

        response.raise_for_status()

        return response.json()
