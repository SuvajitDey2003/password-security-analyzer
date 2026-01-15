# app/core/entropy.py
import math

def calculate_entropy(password: str) -> float:
    """
    Calculates Shannon-style password entropy.
    Returns entropy in bits.
    """
    if not password:
        return 0.0

    charset_size = 0

    if any(c.islower() for c in password):
        charset_size += 26
    if any(c.isupper() for c in password):
        charset_size += 26
    if any(c.isdigit() for c in password):
        charset_size += 10
    if any(not c.isalnum() for c in password):
        charset_size += 32  # common symbols

    entropy = len(password) * math.log2(charset_size)
    return round(entropy, 2)
