
from datetime import datetime , timezone

def get_utc_timestamp() -> float:
    """
    Returns the current UTC datetime in seconds since epoch.
    """
    return datetime.now(timezone.utc).timestamp()

def get_local_timestamp() -> float:
    """
    Returns the current local datetime in seconds since epoch.
    """
    return datetime.now().timestamp()