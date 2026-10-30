"""
Module allowing to test the different responses from the Bank Service Simulator
"""
import json

import pytest
import requests

from payment_gateway_api.config import (BANK_SIMULATOR_REQUIRED_FIELDS,
                                        BANK_SIMULATOR_URL_BASE)


def test_bank_authorizes_payment():
    """
    If card number ends on an odd number, then the simulator returns an 200 OK, authorized True
    """
    payload = {
        "card_number": "0123456789123451",
        "expiry_date": "04/2025",
        "currency": "GBP",
        "amount": 100,
        "cvv": "123"
    }

    response = requests.post(
        f"{BANK_SIMULATOR_URL_BASE}/payments",
        json=payload,
        timeout=5
    )

    response_dict = json.loads(response.text)

    assert response.status_code == 200
    assert response_dict['authorized'] is True


def test_bank_declines_payment():
    """
    If card number ends on an even number, then the simulator returns an 200 OK, authorized False
    """
    payload = {
        "card_number": "0123456789123452",
        "expiry_date": "04/2025",
        "currency": "GBP",
        "amount": 100,
        "cvv": "123"
    }

    response = requests.post(
        f"{BANK_SIMULATOR_URL_BASE}/payments",
        json=payload,
        timeout=5
    )

    response_dict = json.loads(response.text)

    assert response.status_code == 200
    assert response_dict['authorized'] is False


def test_bank_returns_service_unavailable():
    """
    If card number ends on a zero, then the simulator returns an 503 Service Unavailable
    """
    payload = {
        "card_number": "0123456789123450",
        "expiry_date": "04/2025",
        "currency": "GBP",
        "amount": 100,
        "cvv": "123"
    }

    response = requests.post(
        f"{BANK_SIMULATOR_URL_BASE}/payments",
        json=payload,
        timeout=5
    )

    assert response.status_code == 503


@pytest.mark.parametrize(
    "missing_field",
    BANK_SIMULATOR_REQUIRED_FIELDS,
    ids=lambda field: f"missing_{field}"
)
def test_bank_rejects_invalid_request(missing_field, valid_payment_simulator_payload):
    """
    If the payload is missing a required field, then the simulator returns an 400 Bad Request with error message
    We parametrize all possible parameters fields and get rid of each one to check if simulator responds correctly
    """
    payload = valid_payment_simulator_payload.copy()
    payload.pop(missing_field)

    response = requests.post(
        f"{BANK_SIMULATOR_URL_BASE}/payments",
        json=payload,
        timeout=5
    )

    response_dict = json.loads(response.text)

    assert response.status_code == 400
    assert response_dict['error_message'] == 'Not all required properties were sent in the request'
