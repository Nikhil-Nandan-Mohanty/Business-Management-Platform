from uuid import UUID
from sqlalchemy.orm import Session

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.common.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
)
from app.db.session import get_db
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import (
    UserRegistration,
    UserResponse,
    TokenResponse,
    UserLogin,
)
from app.modules.users.service import UserService
from app.auth.dependencies import get_current_user
from app.modules.users.models import User
from app.modules.companies.repository import CompanyRepository


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user: UserRegistration,
    db: Session = Depends(get_db),
):
    """
    Register a new user.
    """

    repository = UserRepository(db)
    company_repository = CompanyRepository(db)

    service = UserService(
        repository,
        company_repository,
    )

    try:
        created_user = service.register_user(user)

    except EmailAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return created_user


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db),
):
    """
    Authenticate a user.
    """

    repository = UserRepository(db)
    company_repository = CompanyRepository(db)

    service = UserService(
        repository,
        company_repository,
    )

    try:
        return service.login_user(
            credentials.email,
            credentials.password,
        )

    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def get_me(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Return the currently authenticated user.
    """
    return current_user


@router.patch(
    "/users/{user_id}/company/{company_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def assign_user_to_company(
    user_id: UUID,
    company_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Assign a user to a company.
    """
    repository = UserRepository(db)
    company_repository = CompanyRepository(db)

    service = UserService(
        repository,
        company_repository,
    )

    try:
        return service.assign_user_to_company(
            user_id,
            company_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/companies/{company_id}/users",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
)
def get_users_by_company(
    company_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[User]:
    """
    Retrieve all users belonging to a company.
    """
    repository = UserRepository(db)
    company_repository = CompanyRepository(db)

    service = UserService(
        repository,
        company_repository,
    )

    return service.get_users_by_company(company_id)
