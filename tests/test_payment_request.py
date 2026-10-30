import pytest

from payment_gateway_api.exceptions import MissingPaymentRequestParameterError
from payment_gateway_api.models import PaymentRequest


def test_payment_request_to_dict():
    payment = PaymentRequest(
        card_number="0123456789123451",
        expiry_date="04/2027",
        currency="USD",
        amount="100",
        cvv="123"
    )

    assert payment.to_dict() == {
        "card_number": "0123456789123451",
        "expiry_month": "04",
        "expiry_year": "2027",
        "expiry_date": "04/2027",
        "currency": "USD",
        "amount": "100",
        "cvv": "123"
    }


def test_missing_payment_parameter():
    with pytest.raises(MissingPaymentRequestParameterError):
        PaymentRequest(
            card_number="0123456789123451",
            expiry_date="04/2027",
            currency="USD",
            amount="100"
        )
