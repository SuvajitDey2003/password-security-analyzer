# app/core/dictionary.py
from typing import Set, List
from pathlib import Path

COMMON_PASSWORDS: Set[str] = set()


def load_password_files(paths: List[str]) -> None:
    """
    Load multiple password dictionary files into memory.
    Handles non-UTF8 characters safely.
    """
    global COMMON_PASSWORDS

    for path in paths:
        file_path = Path(path)
        if not file_path.exists():
            continue

        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                pwd = line.strip().lower()
                if pwd:
                    COMMON_PASSWORDS.add(pwd)


def is_common_password(password: str) -> bool:
    return password.lower() in COMMON_PASSWORDS
