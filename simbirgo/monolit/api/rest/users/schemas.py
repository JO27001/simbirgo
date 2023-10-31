import uuid
from datetime import datetime
from typing import Type

from pydantic import BaseModel, ConfigDict, Field

from simbirgo.common.utils.empty import Empty
from simbirgo.monolit.database.models import User


class JWTTokensResponse(BaseModel):
    access_token: str
    refresh_token: str


class UserCreateRequest(BaseModel):
    username: str
    password: str


class UserUpdateRequest(UserCreateRequest):
    username: str | Type[Empty] = Field(Empty)
    password: str | Type[Empty] = Field(Empty)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    username: str | None
    password: str | None
    isAdmin: bool | None
    balance: float | None
    updated_at: datetime
    created_at: datetime

    @classmethod
    def from_db_model(
        cls, user: User, with_hash_password: bool = False, with_is_admin: bool = False
    ) -> "UserResponse":
        return cls(
            id=user.id,
            username=user.username,
            password=user.password if with_hash_password else None,
            isAdmin=user.isAdmin if with_is_admin else None,
            balance=user.balance,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
