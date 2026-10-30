from dataclasses import dataclass, asdict

from payment_gateway_api.exceptions import MissingPaymentRequestParameterError


@dataclass(frozen=True)
class PaymentRequest:
    card_number: str
    expiry_month: str
    expiry_year: str
    currency: str
    amount: int
    cvv: str

    def __init__(
        self,
        card_number=None,
        expiry_month=None,
        expiry_year=None,
        currency=None,
        amount=None,
        cvv=None
    ):
        parameters = {
            "card_number": card_number,
            "expiry_month": expiry_month,
            "expiry_year": expiry_year,
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
        d = asdict(self)
        d.update({"expiry_date": self.expiry_month + '/' + self.expiry_year})
        return d


@dataclass(frozen=True)
class PaymentResponse:
    id: str
    status: str
    last_four_card_digits: str
    expiry_month: str
    expiry_year: str
    currency: str
    amount: int
