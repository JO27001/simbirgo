from fastapi import Query
from pydantic import BaseModel, conint


class Pagination(BaseModel):
    start: int
    count: int


async def pagination(
    start: conint(ge=0) = Query(0, description="Start position"),
    count: conint(ge=1) = Query(10, description="Number of items to show"),
) -> Pagination:
    return Pagination(start=start, count=count)
