from pydantic import BaseModel


class PaginationMeta(BaseModel):
    """Pagination metadata."""
    limit: int
    offset: int
    total: int


def normalize_limit(limit: int | None, max_limit: int = 100) -> int:
    """Normalize limit parameter."""
    if limit is None:
        return 20
    return min(int(limit), max_limit)


def build_pagination_meta(total: int, limit: int, offset: int) -> PaginationMeta:
    """Build pagination metadata."""
    return PaginationMeta(limit=limit, offset=offset, total=total)
