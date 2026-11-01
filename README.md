# Payment Gateway Challenge
Payment gateway API: A merchant sends card payments to the gateway, which validates them, forwards valid ones to an acquiring bank (a simulator), stores the outcome and lets the merchant retrieve it later.

## Features
`POST /payments` validates a payment, sends it to the bank and returns `Authorized` or `Declined`.

`GET /payments/{id}` returns a previously processed payment.
Invalid payments are rejected with a 400 and never sent to the bank.
Only the last four card digits are stored and returned. The full card number and CVV are never stored, returned or logged.

## Requirements
Python

Poetry

Docker (runs the bank simulator)
## How to run
1. Start the bank simulator (leave it running in its own terminal):
```bash
   docker compose up
   ```
It listens on `http://localhost:8080`.
2. Install dependencies and start the API in a second terminal:
```bash
   poetry install
   poetry run python main.py
   ```
The API listens on `http://localhost:8000`.

3. Check the app swagger

Open `http://localhost:8000/docs` to check the swagger and run your queries.

4. Run the tests:
```bash
   poetry run pytest
   ```
The bank URL is set in `payment_gateway_api/config.py` (`BANK_SIMULATOR_URL_BASE`).
## API endpoint description
### `POST /payments`

Request body:
```json
{
  "card_number": "2222405343248871",
  "expiry_date": "04/2030",
  "currency": "USD",
  "amount": 1050,
  "cvv": "123"
}
```
Field	Rules:

`card_number`	String of 14-19 digits

`expiry_date`	`MM/YYYY`: two-digit month 01-12, four-digit year, not in the past (the current month is still valid)

`currency`	One of `EUR`, `USD`, `JPY`

`amount`	Integer greater than 0, in cents

`cvv`	String of 3-4 digits

All five fields are required, and unknown fields are rejected.

Successful response (`200`):
```json
{
  "id": "5f0c2a3e-8f0b-4c0e-9c52-6a1f1c9a7e11",
  "status": "Authorized",
  "last_four_card_digits": "8871",
  "expiry_month": "04",
  "expiry_year": "2030",
  "currency": "USD",
  "amount": 1050
}
```
`status` is `Authorized` or `Declined`

| Status Code | 	Meaning                                                                                                                      |
|-------------|-------------------------------------------------------------------------------------------------------------------------------|
| `200`       | 	Payment processed by the bank (`Authorized` or `Declined`) and stored                                                        |
| `400`       | 	Payment rejected: invalid JSON, missing or unexpected fields in payload, or a failed validation rule. The bank is not called |
| `503`       | 	The bank is unavailable or timed out. Nothing is stored                                                                      |


### `GET /payments/{id}`
Returns the same body as above for a stored payment.

| Status Code | 	Meaning                                                                 |
|-------------|--------------------------------------------------------------------------|
| `200`       | 	Payment processed by the bank (`Authorized` or `Declined`) and stored. Payment found |
|`404`| 	No payment with that id                                                 |


### The bank simulator
The simulator decides the outcome from the last digit of the card number:

| Last digit | 	Result |
|------------|---------|
| 1, 3, 5, 7, 9	|`200`, `authorized: true`|
|2, 4, 6, 8	|`200`, `authorized: false`|
|0|	`503 Service Unavailable`|

It returns `400` if a required field is missing.
A bank `503` and a timeout (5 seconds) are both reported to the merchant as a `503` from the gateway, not as a decline.


## Project structure
```
payment_gateway_api/
  ├──app.py                         FastAPI app and HTTP endpoints
  ├──app_docs.py                    FastAPI app endpoint default body sample for documentation
  ├──models.py                      PaymentRequest, PaymentResponse, PaymentStatus
  ├──payment_validator.py           Validation rules for a payment request
  ├──payment_service.py             Orchestrates validate -> bank -> store
  ├──bank_service.py                Client for the bank simulator
  ├──payment_repository.py          In-memory storage
  ├──exceptions.py                  Domain exceptions
  ├──config.py                      Bank URL, required fields, allowed currencies
tests/                              Unit and integration tests
  ├──conftest.py
  ├──test_payment_validator.py
  ├──test_payment_request.py
  ├──test_payment_service.py
  ├──test_payment_repository.py
  ├──test_bank_service.py
  ├──test_bank_simulator.py
  ├──test_app.py
main.py                             Starts the API
```

## Design decisions

1. `PaymentService` coordinates the flow, and the validator, bank client and repository each have one job. Every module has one responsability and can be tested in isolation.

2. We validate first, then call the bank. An invalid payment is never sent to the bank and never stored. It gets a 400 straight away.

3. All validation rules are in one place. `PaymentValidator` has one small method per rule, so each rule is easy to read and test. Unknown fields are rejected, and values must have the right type

5. The request object cannot be changed. `PaymentRequest` is frozen. A missing field is reported as missing, and a badly formatted expiry_date is built empty so the validator rejects it instead of crashing

6. `PaymentResponse` has no field for the full card number or CVV, so they cannot be stored or returned by accident. Logs only contain the payment id and status.

7. Bank failures are not declines. A declined payment is a valid outcome and is stored.
8. An unavailable bank is an infrastructure problem and is surfaced as a `503`, with nothing stored.

9. Storage: We use an in-memory store. It only has `save` and `get_by_id`, so a real database could replace it later. The cost is that payments are lost when the app restarts.

### Assumptions and known limitations
Currencies: The supported list (`EUR`, `USD`, `JPY`) is an assumption and is easy to change in `config.py`.

Expiry: A card is valid through the end of its expiry month, so the current month is accepted.

Money amount: They must be positive integers in minor units.

Storage is in memory: Payments are lost when the app restarts.

Bank errors: Only a bank `503` and timeouts are handled. Other bank failures are handled with specific exceptions.

Blocking bank calls: The bank client uses the synchronous `requests` library inside async endpoints, which blocks the event loop under load. An async client such as `httpx` would fix this.

