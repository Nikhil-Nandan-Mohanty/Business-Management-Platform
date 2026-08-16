from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.repositories.base import BaseRepository
from app.modules.companies.models import Company


class CompanyRepository(BaseRepository[Company]):
    """Repository responsible for Company-specific database operations."""

    def __init__(self, db: Session):
        super().__init__(db, Company)

    def get_by_id(self, company_id: UUID) -> Company | None:
        """Retrieve a company by its ID."""
        statement = select(Company).where(Company.id == company_id)
        return self.db.scalar(statement)

    def get_by_name(self, name: str) -> Company | None:
        """Retrieve a company by its name."""
        statement = select(Company).where(Company.name == name)
        return self.db.scalar(statement)

    def get_all(self) -> list[Company]:
        """Retrieve all companies."""
        statement = select(Company).order_by(Company.name)
        return list(self.db.scalars(statement).all())
