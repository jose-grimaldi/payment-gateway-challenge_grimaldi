from payment_gateway_api.models import PaymentStatus


def test_create_authorized_payment(
    client,
    bank_service,
    valid_payment_payload
):
    bank_service.process_payment.return_value = {
        "authorized": True,
        "authorization_code": "code"
    }

    response = client.post("/payments", json=valid_payment_payload)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == PaymentStatus.AUTHORIZED.value
    assert data["last_four_card_digits"] == "3451"
    assert data["currency"] == "USD"
    assert data["amount"] == 100

    assert "id" in data
    assert "card_number" not in data
    assert "cvv" not in data


def test_create_declined_payment(
    client,
    bank_service,
    declined_payment_payload
):
    bank_service.process_payment.return_value = {
        "authorized": False,
        "authorization_code": ""
    }

    response = client.post("/payments", json=declined_payment_payload)

    assert response.status_code == 200
    assert response.json()["status"] == PaymentStatus.DECLINED.value


def test_create_payment_with_missing_field(
    client,
    bank_service,
    valid_payment_payload
):
    payload = valid_payment_payload.copy()
    del payload["card_number"]

    response = client.post("/payments", json=payload)

    assert response.status_code == 400
    bank_service.process_payment.assert_not_called()


def test_create_payment_with_invalid_field(
    client,
    bank_service,
    invalid_payment_payload
):
    response = client.post("/payments", json=invalid_payment_payload)

    assert response.status_code == 400
    bank_service.process_payment.assert_not_called()


def test_create_payment_when_bank_unavailable(
    client,
    bank_service,
    unavailable_payment_payload
):
    response = client.post("/payments", json=unavailable_payment_payload)

    assert response.status_code == 503


def test_get_existing_payment(
    client,
    bank_service,
    valid_payment_payload
):
    bank_service.process_payment.return_value = {
        "authorized": True,
        "authorization_code": "code"
    }

    response = client.post(
        "/payments",
        json=valid_payment_payload
    )

    payment_id = response.json()["id"]

    response_id = client.get(f"/payments/{payment_id}")

    assert response_id.status_code == 200

    data = response_id.json()

    assert data["id"] == payment_id
    assert data["status"] == PaymentStatus.AUTHORIZED.value
    assert data["last_four_card_digits"] == "3451"


def test_get_existing_declined_payment(
    client,
    bank_service,
    declined_payment_payload
):
    bank_service.process_payment.return_value = {
        "authorized": True,
        "authorization_code": "code"
    }

    response = client.post(
        "/payments",
        json=declined_payment_payload
    )

    payment_id = response.json()["id"]

    response_id = client.get(f"/payments/{payment_id}")

    assert response_id.status_code == 200

    data = response_id.json()

    assert data["id"] == payment_id
    assert data["status"] == PaymentStatus.DECLINED.value
    assert data["last_four_card_digits"] == "3452"


def test_get_non_existing_payment(client):
    response = client.get("/payments/unknown-id")

    assert response.status_code == 404


def test_create_payment_with_unexpected_field(client, valid_payment_payload):

    payload = valid_payment_payload.copy()
    payload["unexpected_field"] = "value"

    response = client.post("/payments", json=payload)

    assert response.status_code == 400
    assert "Unexpected fields" in response.json()["detail"]
