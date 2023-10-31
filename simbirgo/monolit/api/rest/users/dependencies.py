import uuid

import fastapi

from simbirgo.common.api.exceptions import HTTPForbidden, HTTPNotAuthenticated
from simbirgo.common.jwt.dependencies.rest import auth_user_id, get_request_user_id
from simbirgo.monolit.database.models import User
from simbirgo.monolit.database.service import MonolitDatabaseService


async def get_path_user(
    request: fastapi.Request,
    user_id: uuid.UUID = fastapi.Path(),
) -> User:
    database: MonolitDatabaseService = request.app.service.database

    async with database.transaction() as session:
        db_user = await database.get_user(session=session, userId=user_id)
    if db_user is None:
        raise fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return db_user


async def get_request_user(
    request: fastapi.Request,
    request_user_id: uuid.UUID | None = fastapi.Depends(get_request_user_id),
) -> User | None:
    if request_user_id is None:
        return None

    database: MonolitDatabaseService = request.app.service.database
    async with database.transaction() as session:
        return await database.get_user(session=session, userId=request_user_id)


async def auth_user(
    request: fastapi.Request,
    request_user_id: uuid.UUID = fastapi.Depends(auth_user_id),
) -> User:
    database: MonolitDatabaseService = request.app.service.database

    async with database.transaction() as session:
        user = await database.get_user(session=session, userId=request_user_id)
    if user is None:
        raise HTTPNotAuthenticated()

    return user


async def auth_admin(user: User = fastapi.Depends(auth_user)) -> User:
    if not user.isAdmin:
        raise HTTPForbidden()
    return user
