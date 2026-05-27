from app.paypal import create_order, capture_order


def initiate_payment(amount):
    order = create_order(amount)

    approve_link = None

    for link in order.get("links", []):
        if link["rel"] == "approve":
            approve_link = link["href"]

    return {
        "order_id": order["id"],
        "approve_link": approve_link,
        "amount": str(amount)
    }


def confirm_payment(order_id):
    result = capture_order(order_id)

    # Handle error response from PayPal
    if result.get("error"):
        return {
            "status": "ERROR",
            "order_id": order_id,
            "message": f"PayPal API Error: {result.get('text', 'Unknown error')}",
            "status_code": result.get("status_code")
        }

    # Handle case where order is already captured
    if "status" not in result:
        return {
            "status": "ALREADY_CAPTURED",
            "order_id": order_id,
            "message": "Order has already been captured"
        }

    # Extract amount from purchase_units if available
    amount = "10.00"
    try:
        if "purchase_units" in result and len(result["purchase_units"]) > 0:
            if "amount" in result["purchase_units"][0]:
                amount = result["purchase_units"][0]["amount"].get("value", "10.00")
    except Exception as e:
        # If amount extraction fails, use default
        print(f"Error extracting amount: {e}")
        print(f"PayPal response: {result}")

    return {
        "status": result["status"],
        "order_id": result["id"],
        "amount": amount
    }