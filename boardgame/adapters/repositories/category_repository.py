from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Set, Optional

from boardgame.domain.model import Category

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class CategoryAbstractRepository(ABC):
    """Boardgame Abstract Repository"""

    def __init__(self):
        self.seen = set()  # type: Set["Category"]

    def add(self, category: "Category"):
        """Add a category to the repository"""
        self._add(category)
        self.seen.add(category)

    def get(self, name: str) -> Optional["Category"]:
        """Get a category by its name"""
        category = self._get(name)
        if category:
            self.seen.add(category)
        return category

    @abstractmethod
    def _add(self, category: "Category"):
        raise NotImplementedError

    @abstractmethod
    def _get(self, name: str) -> "Category":
        raise NotImplementedError


class CategorySqlAlchemyRepository(CategoryAbstractRepository):
    """Category Repository"""

    def __init__(self, session: "Session"):
        super().__init__()
        self._session = session

    def _add(self, category: "Category"):
        self._session.add(category)

    def _get(self, name: str) -> "Category":
        return self._session.query(Category).filter_by(name=name).first()
