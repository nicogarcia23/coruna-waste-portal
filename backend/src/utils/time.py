from datetime import datetime, timedelta
from typing import Tuple


def parse_iso8601(s: str) -> datetime:
    """Parse ISO8601 datetime string to datetime."""
    # Handle basic ISO8601 with or without Z
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return datetime.fromisoformat(s)


def default_window(days: int = 7) -> Tuple[datetime, datetime]:
    """Get default time window ending now, going back specified days."""
    end = datetime.utcnow()
    start = end - timedelta(days=days)
    return start, end


def granularity_to_interval(granularity: str) -> str:
    """Map granularity string to SQL time_bucket interval."""
    mapping = {
        "1h": "1 hour",
        "6h": "6 hours",
        "1d": "1 day"
    }
    return mapping.get(granularity, "1 hour")
