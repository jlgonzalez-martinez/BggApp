""" Language dependence class module"""
from dataclasses import dataclass
from enum import Enum


class LanguageDependenceGrade(Enum):
    """Language dependence grade enum class"""

    LOW = "Independence from the language"
    MEDIUM = "Partial dependence from the language"
    HIGH = "High dependence from the language"

    @classmethod
    def from_name(cls, name: str):
        """
        Get the language dependence grade enum from its name
        Args:
            name: name to search in the enum
        Returns:
            Language dependence grade enum that correspond with the input name
        Raises:
            - ValueError: When the name it's not found
        """
        for item in cls:
            if item.name == name:
                return item
        raise ValueError("Value not found")


@dataclass
class LanguageDependence:
    """Language dependence class"""

    very_low: int = 0
    low: int = 0
    medium: int = 0
    high: int = 0
    very_high: int = 0

    @property
    def total_votes(self) -> int:
        """
        Total votes in the language dependence poll
        Returns: Total votes
        """
        return self.very_low + self.low + self.medium + self.high + self.very_high

    @property
    def grade(self) -> LanguageDependenceGrade:
        """
        Get the specific grade based on the language dependence votes
        Returns: Grade based on the results
        """
        low_votes = self.very_low + self.low
        medium_votes = self.medium
        high_votes = self.high + self.very_high
        max_grade = max([low_votes, medium_votes, high_votes])
        if low_votes == max_grade:
            return LanguageDependenceGrade.LOW
        elif medium_votes == max_grade:
            return LanguageDependenceGrade.MEDIUM
        else:
            return LanguageDependenceGrade.HIGH
