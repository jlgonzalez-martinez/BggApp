import pytest

from boardgame.domain.model.category import CategoryType


class TestCategory:
    """Unit tests for Category."""

    class TestCategoryType:
        """Unit tests for CategoryType."""

        @pytest.mark.unit
        def test_category_type_from_value(self):
            """It returns the correct category type from a value."""
            assert (
                CategoryType.from_value(CategoryType.COMPONENT.value)
                == CategoryType.COMPONENT
            )

        @pytest.mark.unit
        def test_category_type_from_non_existing_value(self):
            """It raises a ValueError when the value is not found."""
            with pytest.raises(ValueError):
                CategoryType.from_value(-9999)

        @pytest.mark.unit
        def test_category_type_from_category(self):
            """It returns the correct category type from a category."""
            assert (
                CategoryType.from_category("Abstract Strategy") == CategoryType.DOMAIN
            )

        @pytest.mark.unit
        def test_category_type_from_category_with_non_existing_category(self):
            """It returns the default category with a non-existing category."""
            assert (
                CategoryType.from_category("Non existing category")
                == CategoryType.DEFAULT
            )
