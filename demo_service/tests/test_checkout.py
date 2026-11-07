from checkout import calculate_checkout

def test_shipping_below_threshold():
    r=calculate_checkout(250)
    assert r["shipping"] == 49 and r["total"] == 299

def test_shipping_at_threshold():
    r=calculate_checkout(500)
    assert r["shipping"] == 0 and r["total"] == 500

def test_shipping_above_threshold():
    r=calculate_checkout(850)
    assert r["shipping"] == 0 and r["total"] == 850

def test_zero_subtotal():
    r=calculate_checkout(0)
    assert r["shipping"] == 49 and r["total"] == 49
