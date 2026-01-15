from app.core.dictionary import load_password_files, is_common_password

def test_common_password_detection(tmp_path):
    file = tmp_path / "pw.txt"
    file.write_text("password\nadmin\n")

    load_password_files([str(file)])

    assert is_common_password("password") is True
    assert is_common_password("Admin") is True
    assert is_common_password("xA9$Lp!2") is False
