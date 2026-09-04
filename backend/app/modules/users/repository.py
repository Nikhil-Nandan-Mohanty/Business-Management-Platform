from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.repositories.base import BaseRepository
from app.modules.users.models import User


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

    def assign_company(
        self,
        user: User,
        company_id: UUID,
    ) -> User:
        """
        Assign a user to a company.
        """
        user.company_id = company_id
        return self.update(user)

    def get_by_company_id(self, company_id: UUID) -> list[User]:
        """
        Retrieve all users belonging to a company.
        """
        statement = select(User).where(User.company_id == company_id)
        return list(self.db.scalars(statement).all())
