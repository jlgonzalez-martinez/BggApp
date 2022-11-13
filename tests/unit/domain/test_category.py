import pytest

from boardgame.domain.model.category import CategoryEnum


class TestCategory:
    """Unit tests for Category."""

    class TestCategoryEnum:
        """Unit tests for CategoryType."""

        @pytest.mark.unit
        def test_category_type_from_value(self):
            """It returns the correct category type from a value."""
            assert (
                CategoryEnum.from_value(CategoryEnum.COMPONENT.value)
                == CategoryEnum.COMPONENT
            )

        @pytest.mark.unit
        def test_category_type_from_non_existing_value(self):
            """It raises a ValueError when the value is not found."""
            with pytest.raises(ValueError):
                CategoryEnum.from_value(-9999)

        @pytest.mark.unit
        def test_category_type_from_category(self):
            """It returns the correct category type from a category."""
            assert (
                CategoryEnum.from_category("Abstract Strategy") == CategoryEnum.DOMAIN
            )

        @pytest.mark.unit
        def test_category_type_from_category_with_non_existing_category(self):
            """It returns the default category with a non-existing category."""
            assert (
                CategoryEnum.from_category("Non existing category")
                == CategoryEnum.DEFAULT
            )
