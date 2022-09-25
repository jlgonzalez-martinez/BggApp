import pytest

from boardgame.domain.model import Player


class TestPlayer:
    @pytest.mark.unit
    def test_positive_votes(self):
        player = Player(best=1, recommended=2, not_recommended=3)
        assert player.positive_votes == 3

    @pytest.mark.unit
    def test_total_votes(self):
        player = Player(best=1, recommended=2, not_recommended=3)
        assert player.total_votes == 6
