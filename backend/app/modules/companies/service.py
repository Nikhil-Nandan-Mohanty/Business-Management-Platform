from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.companies.models import Company
from app.modules.companies.repository import CompanyRepository
from app.modules.companies.schemas import CompanyCreate, CompanyUpdate


class CompanyService:
    """Service responsible for Company business logic."""

    def __init__(self, db: Session):
        self.repository = CompanyRepository(db)

    def create_company(self, data: CompanyCreate) -> Company:
        """Create a new company."""
        existing_company = self.repository.get_by_name(data.name)

        if existing_company:
            raise ValueError("Company with this name already exists")

        company = Company(**data.model_dump())

        self.repository.create(company)

        return company

    def get_company(self, company_id: UUID) -> Company:
        """Retrieve a company by ID."""
        company = self.repository.get_by_id(company_id)

        if not company:
            raise ValueError("Company not found")

        return company

    def get_companies(self) -> list[Company]:
        """Retrieve all companies."""
        return self.repository.get_all()

    def update_company(
        self,
        company_id: UUID,
        data: CompanyUpdate,
    ) -> Company:
        """Update an existing company."""
        company = self.get_company(company_id)

        update_data = data.model_dump(exclude_unset=True)

        if "name" in update_data and update_data["name"] != company.name:
            existing_company = self.repository.get_by_name(update_data["name"])

            if existing_company:
                raise ValueError("Company with this name already exists")

        for field, value in update_data.items():
            setattr(company, field, value)

        self.repository.update(company)

        return company

    def delete_company(self, company_id: UUID) -> None:
        """Delete a company."""
        company = self.get_company(company_id)

        self.repository.delete(company)
