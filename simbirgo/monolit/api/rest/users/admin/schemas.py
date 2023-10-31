from typing import Type

from pydantic import BaseModel, Field

from simbirgo.common.utils.empty import Empty


class AdminCreateRequest(BaseModel):
    username: str
    password: str
    isAdmin: bool | Type[Empty] = Field(Empty)
    balance: float | Type[Empty] = Field(Empty)


class AdminUpdateRequest(BaseModel):
    username: str | Type[Empty] = Field(Empty)
    password: str | Type[Empty] = Field(Empty)
    isAdmin: bool | Type[Empty] = Field(Empty)
    balance: float | Type[Empty] = Field(Empty)
