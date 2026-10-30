import pytest

from payment_gateway_api.bank_service import BankService


def test_bank_authorizes_payment(valid_payment_request):
    response = BankService().process_payment(valid_payment_request)
    assert response["authorized"] is True


def test_bank_declines_payment(declined_payment_request):
    response = BankService().process_payment(declined_payment_request)
    assert response["authorized"] is False


def test_bank_unavailable(unavailable_payment_request):
    with pytest.raises(ConnectionError):
        BankService().process_payment(unavailable_payment_request)
