from demo_service.checkout import calculate_checkout

def test_shipping_below_threshold():
    res = calculate_checkout(400)
    assert res["shipping"] == 49

def test_shipping_at_threshold():
    res = calculate_checkout(500)
    assert res["shipping"] == 0

def test_shipping_above_threshold():
    res = calculate_checkout(600)
    assert res["shipping"] == 0

def test_total_calculation():
    res = calculate_checkout(500)
    assert res["total"] == 500
