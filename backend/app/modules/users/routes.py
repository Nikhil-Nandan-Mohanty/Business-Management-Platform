from sqlalchemy.orm import Session

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.common.exceptions import EmailAlreadyExistsError
from app.db.session import get_db
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import (
    UserRegistration,
    UserResponse,
)
from app.modules.users.service import UserService

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
    service = UserService(repository)

    try:
        created_user = service.register_user(user)

    except EmailAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return created_user