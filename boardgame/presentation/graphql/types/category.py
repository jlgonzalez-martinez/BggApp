from enum import Enum
from typing import TYPE_CHECKING

import strawberry

from boardgame.domain.model.category import CategoryEnum
from .domain_type import DomainType

if TYPE_CHECKING:
    from boardgame.domain.model import Category


@strawberry.enum
class CategoryTypeEnum(Enum):
    COMPONENT = "component"
    DOMAIN = "domain"
    THEME = "theme"
    GENRE = "genre"
    GAME_SYSTEM = "game_system"
    DEFAULT = "default"

    @classmethod
    def from_domain(cls, category_type: CategoryEnum) -> "CategoryTypeEnum":
        """Convert a domain category type to a type."""
        if category_type == CategoryEnum.COMPONENT:
            return cls.COMPONENT
        if category_type == CategoryEnum.DOMAIN:
            return cls.DOMAIN
        if category_type == CategoryEnum.THEME:
            return cls.THEME
        if category_type == CategoryEnum.GENRE:
            return cls.GENRE
        if category_type == CategoryEnum.GAME_SYSTEM:
            return cls.GAME_SYSTEM
        return cls.DEFAULT


@strawberry.type
class CategoryType(DomainType):
    """Category type."""

    id: strawberry.ID
    name: str
    description: str
    category_type: CategoryTypeEnum

    @classmethod
    def from_domain(cls, category: "Category") -> "CategoryType":
        """Convert a domain category to a type."""
        return cls(
            id=getattr(category, "id", None),
            name=category.name,
            description=category.description,
            category_type=CategoryTypeEnum.from_domain(category.category_type),
        )
