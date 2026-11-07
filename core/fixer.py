from pathlib import Path

BUGGY = (
    'def calculate_checkout(subtotal: int) -> dict:\n'
    '    """Return the checkout breakdown. Amounts are in INR."""\n'
    '    shipping = 49 if subtotal < 500 else 49  # BUG: free-shipping threshold is ignored\n'
    '    return {\n'
    '        "subtotal": subtotal,\n'
    '        "shipping": shipping,\n'
    '        "total": subtotal + shipping,\n'
    '    }\n'
)
FIXED = (
    'def calculate_checkout(subtotal: int) -> dict:\n'
    '    """Return the checkout breakdown. Amounts are in INR."""\n'
    '    shipping = 0 if subtotal >= 500 else 49\n'
    '    return {\n'
    '        "subtotal": subtotal,\n'
    '        "shipping": shipping,\n'
    '        "total": subtotal + shipping,\n'
    '    }\n'
)
def reset_code(base):
    (Path(base)/"demo_service"/"checkout.py").write_text(BUGGY, encoding="utf-8")
def apply_fix(base):
    path=Path(base)/"demo_service"/"checkout.py"
    current=path.read_text(encoding="utf-8")
    if "shipping = 0 if subtotal >= 500 else 49" in current: return False, "Already fixed."
    if "shipping = 49 if subtotal < 500 else 49" not in current:
        return False, "Expected buggy line not found; refusing to overwrite unknown code."
    path.write_text(FIXED, encoding="utf-8")
    return True, "Safe patch applied to isolated sample service."
