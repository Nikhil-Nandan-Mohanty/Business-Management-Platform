from app.auth.security import create_access_token, decode_access_token


def test_create_and_decode_access_token():
    token = create_access_token(
        subject="12345",
        role="admin",
    )

    payload = decode_access_token(token)

    assert payload["sub"] == "12345"
    assert payload["role"] == "admin"
    assert "exp" in payload
