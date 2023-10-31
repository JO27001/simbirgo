import fastapi

from simbirgo.common.api.dependencies.pagination import Pagination, pagination
from simbirgo.common.utils.empty import Empty
from simbirgo.monolit.api.rest.transport.dependencies import get_path_transport
from simbirgo.monolit.api.rest.users.dependencies import auth_user
from simbirgo.monolit.database.models import Transport, TransportTypeEnum, User
from simbirgo.monolit.database.service import MonolitDatabaseService

from .schemas import TransportCreateRequest, TransportResponse


async def get_my_transports(
    request: fastapi.Request,
    pagination: Pagination = fastapi.Depends(pagination),
    transportType: TransportTypeEnum = fastapi.Query(Empty),
    user: User = fastapi.Depends(auth_user),
) -> list[TransportResponse]:
    database_service: MonolitDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        db_transports = await database_service.get_transports(
            session=session,
            start=pagination.start,
            count=pagination.count,
            transportType=transportType,
            userId=user.id,
        )

    return [TransportResponse.from_db_model(i) for i in db_transports]


async def get_transport(
    path_transport: Transport = fastapi.Depends(get_path_transport),
) -> TransportResponse:
    return TransportResponse.from_db_model(path_transport)


async def create_transport(
    request: fastapi.Request,
    user: User = fastapi.Depends(auth_user),
    data: TransportCreateRequest = fastapi.Body(embed=False),
) -> TransportResponse:
    database_service: MonolitDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        db_transport = await database_service.create_transport(
            session=session, **data.model_dump(), userId=user.id
        )

    return TransportResponse.from_db_model(db_transport)


async def update_transport(
    request: fastapi.Request,
    path_transport: Transport = fastapi.Depends(get_path_transport),
    data: TransportCreateRequest = fastapi.Body(embed=False),
) -> TransportResponse:
    database_service: MonolitDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        db_transport = await database_service.update_transport(
            session=session, transport=path_transport, **data.model_dump()
        )

    return TransportResponse.from_db_model(db_transport)


async def delete_transport(
    request: fastapi.Request,
    path_transport: Transport = fastapi.Depends(get_path_transport),
):
    database_service: MonolitDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        await database_service.delete_transport(session=session, transportId=path_transport.id)
