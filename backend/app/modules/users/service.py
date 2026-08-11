from app.auth.security import hash_password

from app.common.exceptions import EmailAlreadyExistsError
from app.modules.users.models import User
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserRegistration

from app.auth.security import (
    create_access_token,
    verify_password,
)

from app.common.exceptions import InvalidCredentialsError
from app.modules.users.schemas import TokenResponse


class UserService:
    """
    Handles user-related business logic.
    """

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register_user(self, user_data: UserRegistration) -> User:
        """
        Register a new user.
        """
        existing_user = self.repository.get_by_email(user_data.email)

        if existing_user:
            raise EmailAlreadyExistsError("Email already registered.")

        hashed_password = hash_password(user_data.password)

        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            password_hash=hashed_password,
        )

        return self.repository.create(user)

    def login_user(self, email: str, password: str) -> TokenResponse:
        """
        Authenticate a user and return a JWT access token.
        """

        user = self.repository.get_by_email(email)

        if user is None:
            raise InvalidCredentialsError("Invalid email or password.")

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise InvalidCredentialsError("Invalid email or password.")

        access_token = create_access_token(
            subject=str(user.id),
            role=user.role.value,
        )

        return TokenResponse(
            access_token=access_token,
        )
