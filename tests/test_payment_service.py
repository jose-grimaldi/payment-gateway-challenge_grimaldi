import pytest

from payment_gateway_api.exceptions import InvalidPaymentParameterError


def test_process_authorized_payment(
    payment_service,
    bank_service,
    payment_repository,
    authorized_payment_payload
):
    bank_service.process_payment.return_value = {
        "authorized": True,
        "authorization_code": "code"
    }

    response = payment_service.process_payment(authorized_payment_payload)

    assert response.status == "Authorized"
    assert response.last_four_card_digits == "3451"


def test_process_declined_payment(
    payment_service,
    bank_service,
    payment_repository,
    unauthorized_payment_payload
):
    bank_service.process_payment.return_value = {
        "authorized": False,
        "authorization_code": ""
    }

    response = payment_service.process_payment(unauthorized_payment_payload)

    assert response.status == "Declined"


def test_invalid_payment(
    payment_service,
    bank_service,
    invalid_payment_payload
):
    with pytest.raises(InvalidPaymentParameterError):
        payment_service.process_payment(invalid_payment_payload)

    bank_service.process_payment.assert_not_called()
