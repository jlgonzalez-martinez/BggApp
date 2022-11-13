import pytest

from boardgame.presentation.graphql.pagination import (
    get_paginated_response,
    build_cursor,
    decode_cursor,
    Connection,
    PageInfo,
    Edge,
)
from tests.unit.fakes.fake_graphql_type import FakeDomain, FakeGraphQLType


@pytest.mark.unit
class TestGraphQLPagination:
    """Graphql pagination tests"""

    @pytest.fixture(scope="class")
    def cursor(self) -> str:
        """Cursor fixture."""
        return "MQ=="

    @pytest.fixture(scope="class")
    def cursor_id(self) -> int:
        """Cursor id fixture."""
        return 1

    def test_build_cursor(self, cursor_id, cursor):
        """Test build cursor."""
        assert build_cursor(cursor_id) == cursor

    def test_decode_cursor(self, cursor_id, cursor):
        """Test decode cursor."""
        assert decode_cursor(cursor) == cursor_id

    def test_get_paginated_response(self):
        """Test get paginated response."""
        domain_list = [FakeDomain(id=1, name="test"), FakeDomain(id=2, name="test2")]
        paginated_response = get_paginated_response(
            domain_list, FakeGraphQLType, first=5
        )

        expected_page_info = PageInfo(
            has_next_page=False,
            has_previous_page=False,
            start_cursor=build_cursor(1),
            end_cursor=build_cursor(2),
        )
        expected_edges = [
            Edge(node=FakeGraphQLType(id=1, name="test"), cursor=build_cursor(1)),
            Edge(node=FakeGraphQLType(id=2, name="test2"), cursor=build_cursor(2)),
        ]
        expected_connection = Connection(
            page_info=expected_page_info, edges=expected_edges
        )
        assert expected_connection == paginated_response
