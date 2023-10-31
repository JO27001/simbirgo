import math
from datetime import datetime, timedelta


def minutes_difference(dt1: datetime, dt2: datetime) -> int:
    if dt1 > dt2:
        dt1, dt2 = dt2, dt1

    diff: timedelta = dt2 - dt1
    total_seconds: float = diff.total_seconds()
    total_minutes: float = total_seconds / 60
    rounded_minutes: int = math.ceil(total_minutes)

    return rounded_minutes


def days_difference(dt1: datetime, dt2: datetime) -> float:
    return (dt2 - dt1).total_seconds() / (60 * 60 * 24)
