from payment_gateway_api.config import REQUIRED_FIELDS_PAYLOAD, CURRENCIES

CREATE_PAYMENT_OPENAPI = {
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": sorted(REQUIRED_FIELDS_PAYLOAD),
                    "additionalProperties": False,
                    "properties": {
                        "card_number": {"type": "string", "description": "14-19 digits", "example": "2222405343248871"},
                        "expiry_date": {"type": "string", "description": "MM/YYYY, not in the past",
                                        "example": "04/2030"},
                        "currency": {"type": "string", "enum": CURRENCIES, "example": "USD"},
                        "amount": {"type": "integer", "description": "Minor currency unit, greater than 0",
                                   "example": 1050},
                        "cvv": {"type": "string", "description": "3-4 digits", "example": "123"},
                    },
                }
            }
        },
    }
}
