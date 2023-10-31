import uuid

import fastapi

from simbirgo.common.api.exceptions import HTTPForbidden, HTTPNotAuthenticated
from simbirgo.common.jwt.dependencies.rest import auth_user_id, get_request_user_id
from simbirgo.monolit.api.rest.users.dependencies import auth_user
from simbirgo.monolit.database.models import Rent, Transport, User
from simbirgo.monolit.database.service import MonolitDatabaseService


async def get_path_rent(
    request: fastapi.Request,
    rent_id: uuid.UUID = fastapi.Path(),
) -> Rent:
    database: MonolitDatabaseService = request.app.service.database

    async with database.transaction() as session:
        db_rent = await database.get_rent(session=session, rentId=rent_id)

    if db_rent is None:
        raise fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="Rent not found.",
        )

    return db_rent


async def get_path_rent_transport(
    request: fastapi.Request,
    path_rent: Rent = fastapi.Depends(get_path_rent),
) -> Transport:
    database: MonolitDatabaseService = request.app.service.database

    async with database.transaction() as session:
        db_transport = await database.get_transport(
            session=session, transportId=path_rent.transportId
        )

    if db_transport is None:
        raise fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="Transport not found.",
        )

    return db_transport
