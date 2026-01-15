from unittest.mock import patch
from app.core.breach_check import check_password_breach

@patch("app.core.breach_check.requests.get")
def test_breached_password(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "ABCDEF:10\n123456:5"

    # Force suffix match
    with patch("hashlib.sha1") as mock_hash:
        mock_hash.return_value.hexdigest.return_value = "00000ABCDEF"
        assert check_password_breach("password") == 10
