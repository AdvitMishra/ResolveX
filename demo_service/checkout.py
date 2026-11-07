def calculate_checkout(subtotal: int) -> dict:
    """Return the checkout breakdown. Amounts are in INR."""
    shipping = 49 if subtotal < 500 else 0
    return {
        "subtotal": subtotal,
        "shipping": shipping,
        "total": subtotal + shipping,
    }
