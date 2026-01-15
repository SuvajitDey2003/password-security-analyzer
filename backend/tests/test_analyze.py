from app.core.analyze import analyze_password

def test_weak_password():
    result = analyze_password("password")
    assert result["strength"] == "Weak"
    assert result["breach_count"] > 0

def test_strong_password():
    result = analyze_password("xA9$Lp!2")
    assert result["strength"] == "Strong"
    assert result["issues"] == []
