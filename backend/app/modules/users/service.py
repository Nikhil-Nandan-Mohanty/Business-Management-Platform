from app.auth.security import hash_password
from fastapi import HTTPException, status

from app.common.exceptions import EmailAlreadyExistsError
from app.modules.users.models import User
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserRegistration


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
             raise EmailAlreadyExistsError(
                "Email already registered."
            )

        hashed_password = hash_password(user_data.password)

        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            password_hash=hashed_password,
        )

        return self.repository.create(user)