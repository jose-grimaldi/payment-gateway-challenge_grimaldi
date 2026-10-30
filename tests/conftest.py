from datetime import datetime
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from payment_gateway_api.app import app
from payment_gateway_api.bank_service import BankService
from payment_gateway_api.models import PaymentRequest
from payment_gateway_api.payment_repository import PaymentRepository
from payment_gateway_api.payment_service import PaymentService


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def payment_repository():
    return MagicMock(spec=PaymentRepository)


@pytest.fixture
def bank_service():
    return MagicMock(spec=BankService)


@pytest.fixture
def payment_service(bank_service, payment_repository):
    return PaymentService(bank_service, payment_repository)


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
def declined_payment_payload():
    return {
        "card_number": "0123456789123452",
        "expiry_date": "04/2027",
        "currency": "USD",
        "amount": 100,
        "cvv": "123"
    }


@pytest.fixture
def unavailable_payment_payload():
    return {
        "card_number": "0123456789123450",
        "expiry_date": "04/2027",
        "currency": "USD",
        "amount": 100,
        "cvv": "123"
    }


@pytest.fixture
def invalid_payment_payload():
    return {
        "card_number": "012",
        "expiry_date": "04/2027",
        "currency": "USD",
        "amount": 100,
        "cvv": "123"
    }


@pytest.fixture
def valid_payment_request():
    return PaymentRequest(
        card_number="0123456789123451",
        expiry_date="04/2027",
        currency="USD",
        amount=100,
        cvv="123"
    )


@pytest.fixture
def invalid_payment_request():
    return PaymentRequest(
        card_number="0123456789123451",
        expiry_date="04/1900",
        currency="USD",
        amount=100,
        cvv="123"
    )


@pytest.fixture
def declined_payment_request():
    return PaymentRequest(
        card_number="0123456789123452",
        expiry_date="04/2027",
        currency="USD",
        amount=100,
        cvv="123"
    )


@pytest.fixture
def unavailable_payment_request():
    return PaymentRequest(
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
