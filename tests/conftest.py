from datetime import datetime

import pytest

from payment_gateway_api.models import PaymentRequest


@pytest.fixture
def valid_payment_payload():
    return {
        "card_number": "0123456789123451",
        "expiry_date": "04/2027",
        "currency": "USD",
        "amount": 100,
        "cvv": "123"
    }


@pytest.fixture
def valid_payment_request():
    return PaymentRequest(
        id="pr1",
        card_number="0123456789123451",
        expiry_date="04/2027",
        currency="USD",
        amount=100,
        cvv="123"
    )


@pytest.fixture
def invalid_payment_request():
    return PaymentRequest(
        id="pr1",
        card_number="0123456789123451",
        expiry_date="04/1900",
        currency="USD",
        amount=100,
        cvv="123"
    )


@pytest.fixture
def declined_payment_request():
    return PaymentRequest(
        id="pr1",
        card_number="0123456789123452",
        expiry_date="04/2027",
        currency="USD",
        amount=100,
        cvv="123"
    )


@pytest.fixture
def unavailable_payment_request():
    return PaymentRequest(
        id="pr1",
        card_number="0123456789123450",
        expiry_date="04/2027",
        currency="USD",
        amount=100,
        cvv="123"
    )


@pytest.fixture
def frozen_datetime(monkeypatch):
    """
    Adding a fixture to freeze the datetime.now() in the PaymentValidator, the idea is to have a deterministic test
    """

    class FrozenDateTime(datetime):
        @classmethod
        def now(cls):
            return cls(2026, 10, 30)

    monkeypatch.setattr(
        "payment_gateway_api.payment_validator.datetime",
        FrozenDateTime
    )
