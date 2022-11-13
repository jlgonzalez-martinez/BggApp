""" Category type module """
import json
import os
from enum import IntEnum
from dataclasses import dataclass

from boardgame.domain.model.aggregate import Aggregate
from config import DATA_RESOURCES


with open(os.path.join(DATA_RESOURCES, "categories.json")) as json_file:
    REVISED_CATEGORIES = json.load(json_file)


class CategoryEnum(IntEnum):
    """Category type enum class"""

    COMPONENT = 0
    DOMAIN = 1
    THEME = 2
    GENRE = 3
    GAME_SYSTEM = 4
    DEFAULT = 5

    @classmethod
    def from_value(cls, value: int):
        """
        Get a Category type from it's int value
        Args:
            value: int value for the category type
        Returns: Category type for the input value
        """
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f"Input value {value} not found in the category type enum")

    @classmethod
    def from_category(cls, category_name: str):
        """
        From a category name get it's category type
        Args:
            category_name: Input category name
        Returns: Category type corresponding to the input category
        """
        return cls.from_value(REVISED_CATEGORIES.get(category_name, 5))


@dataclass
class Category(Aggregate):
    """Category class"""

    name: str = ""
    description: str = ""
    category_type: CategoryEnum = CategoryEnum.DEFAULT

    def __hash__(self):
        return hash(self.name)
