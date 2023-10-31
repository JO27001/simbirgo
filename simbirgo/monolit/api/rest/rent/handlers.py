from datetime import datetime

import fastapi

from simbirgo.common.api.dependencies.pagination import Pagination, pagination
from simbirgo.common.api.exceptions import HTTPBadRequest, HTTPForbidden
from simbirgo.monolit.api.rest.rent.dependencies import get_path_rent, get_path_rent_transport
from simbirgo.monolit.api.rest.rent.utils import days_difference, minutes_difference
from simbirgo.monolit.api.rest.transport.dependencies import get_path_transport
from simbirgo.monolit.api.rest.transport.schemas import TransportResponse
from simbirgo.monolit.api.rest.users.dependencies import auth_user
from simbirgo.monolit.database.models import Rent, RentPriceEnum, Transport, TransportTypeEnum, User
from simbirgo.monolit.database.service import MonolitDatabaseService

from .schemas import RentResponse


async def get_transports_by_location(
    request: fastapi.Request,
    lat: float = fastapi.Query(),
    long: float = fastapi.Query(),
    radius: float = fastapi.Query(),
    pagination: Pagination = fastapi.Depends(pagination),
    transportType: TransportTypeEnum = fastapi.Query(),
) -> list[TransportResponse]:
    database_service: MonolitDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        db_transports = await database_service.get_transports_by_location(
            session=session,
            start=pagination.start,
            count=pagination.count,
            latitude=lat,
            longitude=long,
            radius=radius,
            transportType=transportType,
        )

    return [TransportResponse.from_db_model(i) for i in db_transports]


async def get_rent(
    user: User = fastapi.Depends(auth_user),
    path_rent: Rent = fastapi.Depends(get_path_rent),
    path_rent_transport: Transport = fastapi.Depends(get_path_rent_transport),
) -> RentResponse:
    if not (user.id == path_rent.userId or user.id == path_rent_transport.userId):
        raise HTTPForbidden()

    return RentResponse.from_db_model(path_rent)


async def get_my_rents(
    request: fastapi.Request,
    user: User = fastapi.Depends(auth_user),
    pagination: Pagination = fastapi.Depends(pagination),
) -> list[RentResponse]:
    database_service: MonolitDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        db_transports = await database_service.get_rents(
            session=session,
            start=pagination.start,
            count=pagination.count,
            userId=user.id,
        )

    return [RentResponse.from_db_model(i) for i in db_transports]


async def get_transport_rents(
    request: fastapi.Request,
    user: User = fastapi.Depends(auth_user),
    transport: Transport = fastapi.Depends(get_path_transport),
    pagination: Pagination = fastapi.Depends(pagination),
) -> list[RentResponse]:
    if user.id != transport.userId:
        raise HTTPForbidden()

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
    user: User = fastapi.Depends(auth_user),
    priceType: RentPriceEnum = fastapi.Query(),
) -> RentResponse:
    database_service: MonolitDatabaseService = request.app.service.database

    if user.id == transport.userId:
        raise HTTPBadRequest("Can't rent your own transport")

    if transport.canBeRented is False:
        raise HTTPBadRequest("Transportation is already on the rental")

    if priceType == RentPriceEnum.MINUTES:
        price_of_unit = transport.minutePrice
    elif priceType == RentPriceEnum.DAYS:
        price_of_unit = transport.dayPrice
    else:
        raise HTTPBadRequest()

    time_start = datetime.now()

    async with database_service.transaction() as session:
        db_rent = await database_service.create_rent(
            session=session,
            userId=user.id,
            transportId=transport.id,
            time_start=time_start,
            price_of_unit=price_of_unit,
            price_type=priceType,
        )

        await database_service.update_transport(
            session=session,
            transport=transport,
            canBeRented=False,
        )
    return RentResponse.from_db_model(db_rent)


async def end_rent(
    request: fastapi.Request,
    user: User = fastapi.Depends(auth_user),
    path_rent: Rent = fastapi.Depends(get_path_rent),
    path_rent_transport: Transport = fastapi.Depends(get_path_rent_transport),
    lat: float = fastapi.Query(),
    long: float = fastapi.Query(),
) -> RentResponse:
    if path_rent.userId != user.id:
        raise HTTPForbidden()

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
