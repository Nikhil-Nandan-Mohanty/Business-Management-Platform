from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Base repository containing common CRUD operations.
    """

    def __init__(self, db: Session, model: type[ModelType]):
        self.db = db
        self.model = model

    def get_by_id(self, obj_id: UUID) -> ModelType | None:
        """
        Retrieve a record by its primary key.
        """
        statement = select(self.model).where(self.model.id == obj_id)
        return self.db.scalar(statement)

    def create(self, obj: ModelType) -> ModelType:
        """
        Persist a new record.
        """
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj: ModelType) -> ModelType:
        """
        Persist changes to an existing record.
        """
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: ModelType) -> None:
        """
        Delete a record.
        """
        self.db.delete(obj)
        self.db.commit()