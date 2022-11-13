class DomainType:
    """Domain type."""

    @classmethod
    def from_domain(cls, instance):
        """Convert a domain object to a type."""
        raise NotImplementedError
