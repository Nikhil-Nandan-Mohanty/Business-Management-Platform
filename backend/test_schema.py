from pydantic import ValidationError
import pytest

from app.modules.users.schemas import UserRegistration


def test_user_registration_valid_data():
    user = UserRegistration(
        full_name="Raghu Ram",
        email="raghu@gmail.com",
        password="Raghu@1234",
    )

    assert user.full_name == "Raghu Ram"
    assert user.email == "raghu@gmail.com"
    assert user.password == "Raghu@1234"


def test_user_registration_rejects_short_password():
    with pytest.raises(ValidationError):
        UserRegistration(
            full_name="Raghu Ram",
            email="raghu@gmail.com",
            password="short",
        )


def test_user_registration_rejects_invalid_email():
    with pytest.raises(ValidationError):
        UserRegistration(
            full_name="Raghu Ram",
            email="invalid-email",
            password="Raghu@1234",
        )
