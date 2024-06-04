from typing import Optional
from datetime import datetime
from pytz import utc


async def just_throw(anything: Optional[any] = None):
    return anything


def utc_now() -> datetime:
    return datetime.now(utc)