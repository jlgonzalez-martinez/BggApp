from dataclasses import dataclass


@dataclass
class Player:
    """Num players class"""

    number: int = 0
    best: int = 0
    recommended: int = 0
    not_recommended: int = 0

    @property
    def positive_votes(self) -> int:
        """
        Returns the number of positive votes for a current number of players
        Returns: Number of positive votes
        """
        return self.best + self.recommended

    @property
    def total_votes(self) -> int:
        """
        Get the total votes from players instance
        Returns: Total votes
        """
        return self.best + self.recommended + self.not_recommended
