"""
Class allowing to check all validation criterion for a payment request
"""
from datetime import datetime

from payment_gateway_api.config import CURRENCIES
from payment_gateway_api.models import PaymentRequest


class PaymentValidator:

    @staticmethod
    def validate_card_number(card_number: str) -> bool:
        """
        Function allowing to check if a card number is between 14-19 characters long and only numeric
        """
        if not isinstance(card_number, str):
            return False

        return card_number.isdigit() and (14 <= len(card_number) <= 19)

    @staticmethod
    def validate_expiry_date(expiry_date: str) -> bool:
        """
        Function allowing to check if an expiry date is in the future and if the month and year format are correct
        """
        if not isinstance(expiry_date, str):
            return False

        parts = expiry_date.split("/")
        if len(parts) != 2:
            return False

        expiry_month, expiry_year = parts

        if len(expiry_month) != 2 or len(expiry_year) != 4:
            return False
        if not expiry_month.isdigit() or not expiry_year.isdigit():
            return False

        expiry_month = int(expiry_month)
        expiry_year = int(expiry_year)

        if expiry_month < 1 or expiry_month > 12:
            return False

        current_date = datetime.now()

        return ((expiry_year > current_date.year) or
                (expiry_year == current_date.year and expiry_month >= current_date.month))

    @staticmethod
    def validate_currency(currency: str) -> bool:
        """
        Function allowing to check if a currency is allowed
        """
        return isinstance(currency, str) and (currency in CURRENCIES)

    @staticmethod
    def validate_amount(amount: int) -> bool:
        """
        Function allowing to check if an amount is an int and not negative
        """
        return isinstance(amount, int) and (amount > 0)

    @staticmethod
    def validate_cvv(cvv: str) -> bool:
        """
        Function allowing to check if the CVV is numeric only and 3-4 characters long
        """
        if not isinstance(cvv, str):
            return False

        return cvv.isdigit() and (3 <= len(cvv) <= 4)

    def validate_payment(self, payload: PaymentRequest) -> bool:
        """
        Main function checking that the payload is valid
        """
        if not isinstance(payload, PaymentRequest):
            return False

        return (
            self.validate_card_number(payload.card_number)
            and self.validate_expiry_date(payload.expiry_date)
            and self.validate_currency(payload.currency)
            and self.validate_amount(payload.amount)
            and self.validate_cvv(payload.cvv)
        )
