class MissingPaymentRequestParameterError(Exception):

    def __init__(self, missing_parameters):
        self.missing_parameters = missing_parameters
        message = f"Missing required payment parameters: {', '.join(missing_parameters)}"
        super().__init__(message)


class InvalidPaymentParameterError(Exception):

    def __init__(self):
        message = f"Payment information is invalid, payment Rejected"
        super().__init__(message)


class PaymentNotFoundError(Exception):

    def __init__(self, payment_id: str):
        self.payment_id = payment_id

        super().__init__(f"Payment with ID '{payment_id}' was not found")
