import fastapi

from simbirgo.common.api.dependencies.pagination import Pagination, pagination
from simbirgo.common.utils.empty import Empty
from simbirgo.monolit.api.rest.transport.schemas import TransportResponse
from simbirgo.monolit.api.rest.users.dependencies import auth_admin
from simbirgo.monolit.database.models import Transport, TransportTypeEnum, User
from simbirgo.monolit.database.service import MonolitDatabaseService

from .dependencies import get_path_transport_admin
from .schemas import AdminTransportCreateRequest, AdminTransportUpdateRequest


async def get_transports(
    request: fastapi.Request,
    pagination: Pagination = fastapi.Depends(pagination),
    transportType: TransportTypeEnum = fastapi.Query(Empty),
    _: User = fastapi.Depends(auth_admin),
) -> list[TransportResponse]:
    database_service: MonolitDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        db_transports = await database_service.get_transports(
            session=session,
            start=pagination.start,
            count=pagination.count,
            transportType=transportType,
        )

    return [TransportResponse.from_db_model(i) for i in db_transports]


async def get_transport(
    path_transport: Transport = fastapi.Depends(get_path_transport_admin),
) -> TransportResponse:
    return TransportResponse.from_db_model(path_transport)


async def create_transport(
    request: fastapi.Request,
    data: AdminTransportCreateRequest = fastapi.Body(embed=False),
    _: User = fastapi.Depends(auth_admin),
) -> TransportResponse:
    database_service: MonolitDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        db_transport = await database_service.create_transport(session=session, **data.model_dump())

    return TransportResponse.from_db_model(db_transport)


async def update_transport(
    request: fastapi.Request,
    _: User = fastapi.Depends(auth_admin),
    path_transport: Transport = fastapi.Depends(get_path_transport_admin),
    data: AdminTransportUpdateRequest = fastapi.Body(embed=False),
) -> TransportResponse:
    database_service: MonolitDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        db_transport = await database_service.update_transport(
            session=session, transport=path_transport, **data.model_dump()
        )

    return TransportResponse.from_db_model(db_transport)


async def delete_transport(
    request: fastapi.Request,
    _: User = fastapi.Depends(auth_admin),
    path_transport: Transport = fastapi.Depends(get_path_transport_admin),
):
    database_service: MonolitDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        await database_service.delete_transport(session=session, transport_id=path_transport.id)
