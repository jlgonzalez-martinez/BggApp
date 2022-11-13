import base64
from typing import List, Generic, TypeVar, Optional, Any, Type

import strawberry

GenericType = TypeVar("GenericType")


@strawberry.type
class Connection(Generic[GenericType]):
    """Represents a paginated relationship between two entities

    This pattern is used when the relationship itself has attributes.
    In a Facebook-based domain example, a friendship between two people
    would be a connection that might have a `friendshipStartTime`
    """

    page_info: "PageInfo"
    edges: List["Edge[GenericType]"]


@strawberry.type
class PageInfo:
    """Pagination context to navigate objects with cursor-based pagination

    Instead of classic offset pagination via `page` and `limit` parameters,
    here we have a cursor of the last object and we fetch items starting from that one

    Read more at:
        - https://graphql.org/learn/pagination/#pagination-and-edges
        - https://relay.dev/graphql/connections.htm
    """

    has_next_page: bool
    has_previous_page: bool
    start_cursor: Optional[str]
    end_cursor: Optional[str]


@strawberry.type
class Edge(Generic[GenericType]):
    """An edge may contain additional information of the relationship. This is the trivial case"""

    node: GenericType
    cursor: str


def build_cursor(item_id: int) -> str:
    """Build a cursor from an item id."""
    return base64.b64encode(str(item_id).encode()).decode()


def decode_cursor(cursor: str) -> int:
    """Decode a cursor to an item id."""
    return int(base64.b64decode(cursor.encode()).decode())


def get_paginated_response(
    entities: List[Any], graphql_type: Type[GenericType], first: int = 20
) -> Connection:
    """Get a paginated response from a list of entities."""
    edges = [
        Edge(
            node=graphql_type.from_domain(entity),
            cursor=build_cursor(entity.id),
        )
        for entity in entities
    ]

    return Connection(
        page_info=PageInfo(
            has_previous_page=False,
            has_next_page=len(edges) >= first,
            start_cursor=edges[0].cursor if edges else None,
            end_cursor=edges[-1].cursor if edges else None,
        ),
        edges=edges,
    )
