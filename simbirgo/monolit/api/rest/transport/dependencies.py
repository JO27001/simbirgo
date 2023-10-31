import uuid

import fastapi

from simbirgo.monolit.api.rest.users.dependencies import auth_user
from simbirgo.monolit.database.models import Transport, User
from simbirgo.monolit.database.service import MonolitDatabaseService


async def get_path_transport(
    request: fastapi.Request,
    transport_id: uuid.UUID = fastapi.Path(),
) -> Transport:
    database: MonolitDatabaseService = request.app.service.database

    async with database.transaction() as session:
        db_transport = await database.get_transport(session=session, transportId=transport_id)

    if db_transport is None:
        raise fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="Transport not found.",
        )

    return db_transport
