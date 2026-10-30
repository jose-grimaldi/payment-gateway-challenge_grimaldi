from dataclasses import dataclass, asdict

from payment_gateway_api.exceptions import MissingPaymentRequestParameterError


@dataclass(frozen=True)
class PaymentRequest:
    id: str
    card_number: str
    expiry_date: str
    currency: str
    amount: int
    cvv: str

    def __init__(
        self,
        id=None,
        card_number=None,
        expiry_date=None,
        currency=None,
        amount=None,
        cvv=None
    ):
        parameters = {
            "id": id,
            "card_number": card_number,
            "expiry_date": expiry_date,
            "currency": currency,
            "amount": amount,
            "cvv": cvv
        }

        missing_parameters = [
            name for name, value in parameters.items()
            if value is None
        ]

        if missing_parameters:
            raise MissingPaymentRequestParameterError(missing_parameters)

        for name, value in parameters.items():
            object.__setattr__(self, name, value)

    def to_dict(self):
        return asdict(self)
