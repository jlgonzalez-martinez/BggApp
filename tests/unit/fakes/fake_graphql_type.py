from dataclasses import dataclass

import strawberry

from boardgame.presentation.graphql.types.domain_type import DomainType


@dataclass
class FakeDomain:
    id: int
    name: str


@strawberry.type
class FakeGraphQLType(DomainType):
    """Category type."""

    id: strawberry.ID
    name: str

    @classmethod
    def from_domain(cls, fake_domain: "FakeDomain") -> "FakeGraphQLType":
        """Convert a domain category to a type."""
        return cls(
            id=fake_domain.id,
            name=fake_domain.name,
        )
