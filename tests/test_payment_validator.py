import pytest

from payment_gateway_api.config import CURRENCIES
from payment_gateway_api.payment_validator import PaymentValidator


@pytest.mark.parametrize("card_number", [
    "12345678901234",  # 14 digits
    "1234567890123456789"  # 19 digits
])
def test_valid_card_numbers(card_number):
    assert PaymentValidator.validate_card_number(card_number) is True


@pytest.mark.parametrize("card_number", [
    "123",  # too short
    "12345678901234567890",  # 20 digits
    "12345678901234AB",  # letters
    12345678901234  # not string
])
def test_invalid_card_numbers(card_number):
    assert PaymentValidator.validate_card_number(card_number) is False


@pytest.mark.parametrize("expiry_date", [
    "10/2026",
    "11/2026",
])
def test_valid_expiry_dates(expiry_date, frozen_datetime):
    assert PaymentValidator.validate_expiry_date(expiry_date) is True


@pytest.mark.parametrize("expiry_date", [
    "09/2026",  # past date
    "13/2027",  # invalid month
    "00/2027",  # invalid month
    "4/2027",  # invalid month format
    "invalid"  # invalid string

])
def test_invalid_expiry_dates(expiry_date, frozen_datetime):
    assert PaymentValidator.validate_expiry_date(expiry_date) is False


@pytest.mark.parametrize("currency", CURRENCIES)
def test_valid_currencies(currency):
    assert PaymentValidator.validate_currency(currency) is True


@pytest.mark.parametrize("currency", ["CAD", 123])
def test_invalid_currencies(currency):
    assert PaymentValidator.validate_currency(currency) is False


@pytest.mark.parametrize("amount", [1, 100])
def test_valid_amounts(amount):
    assert PaymentValidator.validate_amount(amount) is True


@pytest.mark.parametrize("amount", [0, -1, 1.5, "100"])
def test_invalid_amounts(amount):
    assert PaymentValidator.validate_amount(amount) is False


@pytest.mark.parametrize("cvv", ["123", "1234"])
def test_valid_cvv(cvv):
    assert PaymentValidator.validate_cvv(cvv) is True


@pytest.mark.parametrize("cvv", ["12", "12345", "ABC", 123])
def test_invalid_cvv(cvv):
    assert PaymentValidator.validate_cvv(cvv) is False


def test_valid_payment(valid_payment_request):
    assert PaymentValidator().validate_payment(valid_payment_request) is True


def test_missing_required_field(invalid_payment_request):
    assert PaymentValidator().validate_payment(invalid_payment_request) is False
