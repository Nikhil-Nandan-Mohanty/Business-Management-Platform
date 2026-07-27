from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from app.core.config import settings

# Password hasher (Argon2)
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Hash a plain text password.
    """
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its hash.
    """
    return password_hash.verify(password, hashed_password)


def create_access_token(
    subject: str,
    role: str,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a JWT access token.
    """
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    payload = {
        "sub": subject,
        "role": role,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    """
    Decode and validate a JWT.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload

    except InvalidTokenError as exc:
        raise ValueError("Invalid or expired token") from exc