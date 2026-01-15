# app/core/breach_check.py
import hashlib
import requests
from typing import Optional

HIBP_API_URL = "https://api.pwnedpasswords.com/range/{}"
REQUEST_TIMEOUT = 5  # seconds


def check_password_breach(password: str) -> Optional[int]:
    """
    Checks if a password has appeared in known data breaches
    using k-anonymity.
    
    Returns:
        breach count if found, else 0
        None if API is unavailable
    """
    if not password:
        return 0

    # 1. SHA-1 hash (required by API)
    sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]

    try:
        # 2. Send only prefix
        response = requests.get(
            HIBP_API_URL.format(prefix),
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
    except requests.RequestException:
        # Network/API failure → fail safely
        return None

    # 3. Match suffix locally
    for line in response.text.splitlines():
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            return int(count)

    return 0
