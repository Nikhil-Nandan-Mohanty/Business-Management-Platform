from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.repositories.base import BaseRepository
from app.modules.users.models import User
from uuid import UUID


class UserRepository(BaseRepository[User]):
    """
    Repository responsible for User-specific database operations.
    """

    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by email address.
        """
        statement = select(User).where(User.email == email)
        return self.db.scalar(statement)

    def get_by_id(self, user_id: UUID) -> User | None:
        """
        Retrieve a user by UUID.
        """
        statement = select(User).where(User.id == user_id)
        return self.db.scalar(statement)
