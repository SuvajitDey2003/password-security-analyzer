from app.core.patterns import detect_patterns

def test_repeated_characters():
    issues = detect_patterns("aaaBBB")
    assert "Repeated characters detected" in issues

def test_sequential_numbers():
    issues = detect_patterns("test123")
    assert "Sequential numbers detected" in issues

def test_keyboard_pattern():
    issues = detect_patterns("Qwerty!9")
    assert "Keyboard pattern detected" in issues

def test_strong_password_no_patterns():
    issues = detect_patterns("xA9$Lp!2")
    assert issues == []
