import pytest

from boardgame.domain.model import LanguageDependence
from boardgame.domain.model.language_dependence import LanguageDependenceGrade


class TestLanguageDependence:
    @pytest.mark.unit
    def test_language_dependence_low_grade(self):
        language_dependence = LanguageDependence(
            very_low=1, low=1, medium=0, high=0, very_high=0
        )
        assert language_dependence.grade == LanguageDependenceGrade.LOW
        assert language_dependence.total_votes == 2

    @pytest.mark.unit
    def test_language_dependence_medium_grade(self):
        language_dependence = LanguageDependence(
            very_low=0, low=0, medium=5, high=0, very_high=0
        )
        assert language_dependence.grade == LanguageDependenceGrade.MEDIUM
        assert language_dependence.total_votes == 5

    @pytest.mark.unit
    def test_language_dependence_high_grade(self):
        language_dependence = LanguageDependence(
            very_low=0, low=3, medium=0, high=2, very_high=2
        )
        assert language_dependence.grade == LanguageDependenceGrade.HIGH
        assert language_dependence.total_votes == 7

    @pytest.mark.unit
    def test_language_dependence_grade_from_name(self):
        assert (
            LanguageDependenceGrade.from_name(LanguageDependenceGrade.LOW.name)
            == LanguageDependenceGrade.LOW
        )

    @pytest.mark.unit
    def test_language_dependence_grade_from_non_existing_name(self):
        with pytest.raises(ValueError):
            LanguageDependenceGrade.from_name("non_existing_name")
