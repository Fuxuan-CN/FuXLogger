
from datetime import datetime , timezone

def getUTCDateTime() -> float:
    """
    Returns the current UTC datetime in seconds since epoch.
    """
    return datetime.now(timezone.utc).timestamp()

def getLocalDateTime() -> float:
    """
    Returns the current local datetime in seconds since epoch.
    """
    return datetime.now().timestamp()