# app/core/analyze.py
from typing import Dict, Any

from backend.app.core.entropy import calculate_entropy
from backend.app.core.patterns import detect_patterns
from backend.app.core.dictionary import is_common_password
from backend.app.core.breach_check import check_password_breach


def analyze_password(password: str) -> Dict[str, Any]:
    issues = []

    #Calculate entropy
    entropy = calculate_entropy(password)

    # Pattern detection
    pattern_issues = detect_patterns(password)
    issues.extend(pattern_issues)

    # Dictionary check
    common = is_common_password(password)
    if common:
        issues.append("Common dictionary password")

    # Breach check
    breach_count = check_password_breach(password)
    breached = breach_count and breach_count > 0
    if breached:
        issues.append("Found in known data breaches")

    # Base score from entropy
    score = min(100, int(entropy * 2))

    # Penalize based on security issues
    if entropy < 40:
        score -= 20
        issues.append("Low entropy")

    if pattern_issues:
        score -= 15

    if any("Repeated" in issue for issue in pattern_issues):
        score -= 40

    if common:
        score -= 30

    if breached:
        score -= 40

    # Clamp score
    score = max(0, score)

    # Final strength classification
    if breached or common:
        strength = "Weak"
    elif any("Repeated" in issue for issue in issues):
        strength = "Weak"
    elif score >= 70:
        strength = "Strong"
    elif score >= 40:
        strength = "Moderate"
    else:
        strength = "Weak"

    return {
        "score": score,
        "entropy": entropy,
        "strength": strength,
        "issues": list(set(issues)),
        "breach_count": breach_count or 0
    }
