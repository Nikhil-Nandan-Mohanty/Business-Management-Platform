from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.auth.security import decode_access_token
from app.db.session import get_db
from app.modules.users.models import User
from app.modules.users.repository import UserRepository


bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Retrieve the currently authenticated user from the JWT.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials

    try:
        payload = decode_access_token(token)

        subject = payload.get("sub")

        if subject is None:
            raise credentials_exception

        user_id = UUID(subject)

    except (ValueError, TypeError):
        raise credentials_exception from None

    repository = UserRepository(db)

    user = repository.get_by_id(user_id)

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive.",
        )

    if user.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account has been deleted.",
        )

    return user
