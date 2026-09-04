from uuid import UUID

from app.common.exceptions import EmailAlreadyExistsError
from app.modules.users.models import User
from app.modules.users.repository import UserRepository
from app.modules.companies.repository import CompanyRepository

from app.auth.security import (
    create_access_token,
    hash_password,
    verify_password,
)

from app.common.exceptions import InvalidCredentialsError
from app.modules.users.schemas import (
    TokenResponse,
    UserRegistration,
)


class UserService:
    """
    Handles user-related business logic.
    """

    def __init__(
        self, repository: UserRepository, company_repository: CompanyRepository
    ):
        self.repository = repository
        self.company_repository = company_repository

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

    def assign_user_to_company(
        self,
        user_id: UUID,
        company_id: UUID,
    ) -> User:
        """
        Assign a user to a company.
        """
        user = self.repository.get_by_id(user_id)

        if user is None:
            raise ValueError("User not found")

        company = self.company_repository.get_by_id(company_id)

        if company is None:
            raise ValueError("Company not found")

        return self.repository.assign_company(
            user,
            company_id,
        )

    def get_users_by_company(self, company_id: UUID) -> list[User]:
        """
        Retrieve all users belonging to a company.
        """
        return self.repository.get_by_company_id(company_id)