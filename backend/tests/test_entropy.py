from app.core.entropy import calculate_entropy

def test_empty_password_entropy():
    assert calculate_entropy("") == 0.0

def test_low_entropy_password():
    assert calculate_entropy("abc") < 30

def test_high_entropy_password():
    assert calculate_entropy("xA9$Lp!2") > 40
