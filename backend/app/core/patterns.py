# app/core/patterns.py
import re
from typing import List

KEYBOARD_PATTERNS = [
    "qwerty", "asdf", "zxcv"
]

SEQUENTIAL_NUMBERS = [
    "0123456789",
    "9876543210"
]

SEQUENTIAL_LETTERS = [
    "abcdefghijklmnopqrstuvwxyz",
    "zyxwvutsrqponmlkjihgfedcba"
]


def detect_patterns(password: str) -> List[str]:
    issues = []
    pwd = password.lower()

    # Repeated characters (aaa, 111, !!!)
    if re.search(r"(.)\1{2,}", pwd):
        issues.append("Repeated characters detected")

    # Repeating substring (abab, xyzxyz)
    length = len(pwd)
    for size in range(1, length // 2 + 1):
        substring = pwd[:size]
        if substring * (length // size) == pwd:
            issues.append("Repeated pattern detected")
            break

    # Sequential numbers
    for seq in SEQUENTIAL_NUMBERS:
        for i in range(len(seq) - 2):
            if seq[i:i+3] in pwd:
                issues.append("Sequential numbers detected")
                break

    # Sequential letters
    for seq in SEQUENTIAL_LETTERS:
        for i in range(len(seq) - 2):
            if seq[i:i+3] in pwd:
                issues.append("Sequential letters detected")
                break

    # Keyboard patterns
    for pattern in KEYBOARD_PATTERNS:
        if pattern in pwd:
            issues.append("Keyboard pattern detected")
            break

    return issues
