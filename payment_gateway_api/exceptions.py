import logging


class MissingPaymentRequestParameterError(Exception):

    def __init__(self, missing_parameters):
        self.missing_parameters = missing_parameters
        message = f"Missing required payment parameters: {', '.join(missing_parameters)}"
        super().__init__(message)
