import requests
import base64

from app.config import PAYPAL_CLIENT_ID, PAYPAL_SECRET, PAYPAL_BASE_URL


def get_access_token():
    auth = f"{PAYPAL_CLIENT_ID}:{PAYPAL_SECRET}"
    encoded = base64.b64encode(auth.encode()).decode()

    response = requests.post(
        f"{PAYPAL_BASE_URL}/v1/oauth2/token",
        headers={
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={"grant_type": "client_credentials"},
    )

    data = response.json()

    if "access_token" not in data:
        raise Exception(f"PayPal auth failed: {data}")

    return data["access_token"]


def create_order(amount):
    token = get_access_token()

    payload = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": str(amount)
                }
            }
        ],
        "application_context": {
            "return_url": f"http://127.0.0.1:8000/success?amount={amount}",
            "cancel_url": "http://127.0.0.1:8000/cancel"
        }
    }

    response = requests.post(
        f"{PAYPAL_BASE_URL}/v2/checkout/orders",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=payload,
    )

    return response.json()


def capture_order(order_id):
    token = get_access_token()

    response = requests.post(
        f"{PAYPAL_BASE_URL}/v2/checkout/orders/{order_id}/capture",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )

    # Check if response is valid JSON
    try:
        return response.json()
    except Exception:
        # If not JSON, return error details
        return {
            "error": True,
            "status_code": response.status_code,
            "text": response.text
        }