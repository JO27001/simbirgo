import uuid
from datetime import datetime

import fastapi

from simbirgo.common.api.dependencies.pagination import Pagination, pagination
from simbirgo.common.api.exceptions import HTTPBadRequest, HTTPForbidden
from simbirgo.monolit.api.rest.rent.dependencies import get_path_rent, get_path_rent_transport
from simbirgo.monolit.api.rest.rent.schemas import (
    AdminRentCreateRequest,
    AdminRentUpdateRequest,
    RentResponse,
)
from simbirgo.monolit.api.rest.rent.utils import days_difference, minutes_difference
from simbirgo.monolit.api.rest.transport.dependencies import get_path_transport
from simbirgo.monolit.api.rest.transport.schemas import TransportResponse
from simbirgo.monolit.api.rest.users.admin.dependencies import auth_admin
from simbirgo.monolit.database.models import Rent, RentPriceEnum, Transport, TransportTypeEnum, User
from simbirgo.monolit.database.service import MonolitDatabaseService


async def get_rent(
    _: User = fastapi.Depends(auth_admin),
    path_rent: Rent = fastapi.Depends(get_path_rent),
) -> RentResponse:
    return RentResponse.from_db_model(path_rent)


async def get_user_rents(
    request: fastapi.Request,
    user_id: uuid.UUID = fastapi.Path(),
    _: User = fastapi.Depends(auth_admin),
    pagination: Pagination = fastapi.Depends(pagination),
) -> list[RentResponse]:
    database_service: MonolitDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        db_transports = await database_service.get_rents(
            session=session,
            start=pagination.start,
            count=pagination.count,
            userId=user_id,
        )

    return [RentResponse.from_db_model(i) for i in db_transports]


async def get_transport_rents(
    request: fastapi.Request,
    _: User = fastapi.Depends(auth_admin),
    transport: Transport = fastapi.Depends(get_path_transport),
    pagination: Pagination = fastapi.Depends(pagination),
) -> list[RentResponse]:
    database_service: MonolitDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        db_transports = await database_service.get_rents(
            session=session,
            start=pagination.start,
            count=pagination.count,
            transportId=transport.id,
        )

    return [RentResponse.from_db_model(i) for i in db_transports]


async def create_rent(
    request: fastapi.Request,
    transport: Transport = fastapi.Depends(get_path_transport),
    _: User = fastapi.Depends(auth_admin),
    data: AdminRentCreateRequest = fastapi.Body(embed=False),
) -> RentResponse:
    database_service: MonolitDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        db_rent = await database_service.create_rent(session=session, **data.model_dump())

        await database_service.update_transport(
            session=session,
            transport=transport,
            canBeRented=False,
        )

    return RentResponse.from_db_model(db_rent)


async def end_rent(
    request: fastapi.Request,
    _: User = fastapi.Depends(auth_admin),
    path_rent: Rent = fastapi.Depends(get_path_rent),
    path_rent_transport: Transport = fastapi.Depends(get_path_rent_transport),
    lat: float = fastapi.Query(),
    long: float = fastapi.Query(),
) -> RentResponse:
    database_service: MonolitDatabaseService = request.app.service.database

    time_end = datetime.now()

    if path_rent.priceType == RentPriceEnum.MINUTES:
        time_use = minutes_difference(path_rent.timeStart, time_end)
        final_price = time_use * path_rent.priceOfUnit
    elif path_rent.priceType == RentPriceEnum.DAYS:
        time_use = days_difference(path_rent.timeStart, time_end)
        final_price = time_use * path_rent.priceOfUnit
    else:
        raise HTTPBadRequest()

    async with database_service.transaction() as session:
        user = await database_service.get_user(
            session=session,
            userId=path_rent.userId,
        )

        if user is None:
            raise

        db_rent = await database_service.update_rent(
            session=session,
            rent=path_rent,
            timeEnd=time_end,
            final_price=final_price,
        )

        await database_service.update_transport(
            session=session,
            transport=path_rent_transport,
            latitude=lat,
            longitude=long,
            canBeRented=True,
        )

        await database_service.update_user(
            session=session, user=user, balance=user.balance - final_price
        )
    return RentResponse.from_db_model(db_rent)


async def update_rent(
    request: fastapi.Request,
    path_rent: Rent = fastapi.Depends(get_path_rent),
    _: User = fastapi.Depends(auth_admin),
    data: AdminRentUpdateRequest = fastapi.Body(embed=False),
) -> RentResponse:
    database_service: MonolitDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        db_rent = await database_service.update_rent(
            session=session, rent=path_rent, **data.model_dump()
        )

    return RentResponse.from_db_model(db_rent)


async def delete_rent(request: fastapi.Request, rent_id: uuid.UUID = fastapi.Path()):
    database_service: MonolitDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        await database_service.delete_rent(session=session, rentId=rent_id)
