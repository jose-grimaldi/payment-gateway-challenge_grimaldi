from payment_gateway_api.models import PaymentResponse
from payment_gateway_api.payment_repository import PaymentRepository


def test_save_payment():
    repository = PaymentRepository()

    payment = PaymentResponse(
        id="p1",
        status="Authorized",
        last_four_card_digits="8871",
        expiry_month="04",
        expiry_year="2027",
        currency="USD",
        amount=100
    )

    repository.save(payment)

    assert repository.get_by_id("p1") == payment


def test_get_non_existing_payment():
    repository = PaymentRepository()

    assert repository.get_by_id("unknown-id") is None
