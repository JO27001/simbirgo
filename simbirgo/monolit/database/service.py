import pathlib
import uuid
from datetime import datetime
from typing import Sequence, Type

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from simbirgo.common.database.service import BaseDatabaseService
from simbirgo.common.utils import md5
from simbirgo.common.utils.empty import Empty
from simbirgo.monolit.database.models import (
    Base,
    Rent,
    RentPriceEnum,
    Transport,
    TransportTypeEnum,
    User,
)
from simbirgo.monolit.settings import MonolitSettings


class MonolitDatabaseService(BaseDatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"

    def get_fixtures_directory_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "fixtures"

    def get_models(self) -> list[Type[Base]]:
        return [User]

    async def delete_user(
        self,
        session: AsyncSession,
        userId: uuid.UUID | Type[Empty] = Empty,
    ) -> None:
        stmt = delete(User).where(User.id == userId)
        await session.execute(stmt)

    async def get_user(
        self,
        session: AsyncSession,
        userId: uuid.UUID | Type[Empty] = Empty,
        username: str | Type[Empty] = Empty,
        password: str | Type[Empty] = Empty,
    ) -> User | None:
        filters = []
        if userId is not Empty:
            filters.append(User.id == userId)
        if username is not Empty:
            filters.append(User.username == username)
        if username is not Empty:
            filters.append(User.password == md5.hash_string(password))

        stmt = select(User).where(*filters)
        result = await session.execute(stmt)
        user = result.unique().scalar_one_or_none()

        return user

    async def get_users(
        self,
        session: AsyncSession,
        count: int | None,
        start: int = 0,
    ) -> Sequence[User]:
        stmt = select(User).order_by(User.created_at)

        if count is not None:
            offset = start
            stmt = stmt.limit(count).offset(offset)

        result = await session.execute(stmt)
        users = result.scalars().all()

        return users

    async def update_user(
        self,
        session: AsyncSession,
        user: User,
        username: str | Type[Empty] = Empty,
        password: str | Type[Empty] = Empty,
        balance: float | Type[Empty] = Empty,
        isAdmin: bool | Type[Empty] = Empty,
    ) -> User:
        if username is not Empty:
            user.username = username
        if password is not Empty:
            user.password = md5.hash_string(password)
        if balance is not Empty:
            user.balance = balance
        if isAdmin is not Empty:
            user.isAdmin = isAdmin

        session.add_all([user])

        return user

    async def create_user(
        self,
        session: AsyncSession,
        username: str,
        password: str,
        balance: float = 0,
        isAdmin: bool = True,
    ) -> User:
        user = User(
            username=username,
            password=md5.hash_string(password),
            balance=balance,
            isAdmin=isAdmin,
        )
        session.add_all([user])

        return user

    async def delete_transport(self, session: AsyncSession, transportId: uuid.UUID) -> None:
        stmt = delete(Transport).where(Transport.id == transportId)
        await session.execute(stmt)

    async def get_transport(
        self,
        session: AsyncSession,
        transportId: uuid.UUID | Type[Empty] = Empty,
        canBeRented: bool | Type[Empty] = Empty,
        transportType: str | Type[Empty] = Empty,
        model: TransportTypeEnum | Type[Empty] = Empty,
        color: str | Type[Empty] = Empty,
        identifier: str | Type[Empty] = Empty,
        description: str | None | Type[Empty] = Empty,
        latitude: float | None | Type[Empty] = Empty,
        longitude: float | Type[Empty] = Empty,
        minutePrice: float | Type[Empty] = Empty,
        dayPrice: float | None | Type[Empty] = Empty,
        userId: uuid.UUID | Type[Empty] = Empty,
    ) -> Transport | None:
        filters = []
        if transportId is not Empty:
            filters.append(Transport.id == transportId)
        if canBeRented is not Empty:
            filters.append(Transport.canBeRented == canBeRented)
        if transportType is not Empty:
            filters.append(Transport.transportType == transportType)
        if model is not Empty:
            filters.append(Transport.model == model)
        if color is not Empty:
            filters.append(Transport.color == color)
        if identifier is not Empty:
            filters.append(Transport.identifier == identifier)
        if description is not Empty:
            filters.append(Transport.description == description)
        if latitude is not Empty:
            filters.append(Transport.latitude == latitude)
        if longitude is not Empty:
            filters.append(Transport.longitude == longitude)
        if minutePrice is not Empty:
            filters.append(Transport.minutePrice == minutePrice)
        if dayPrice is not Empty:
            filters.append(Transport.dayPrice == dayPrice)
        if userId is not Empty:
            filters.append(Transport.userId == userId)

        stmt = select(Transport).where(*filters)
        result = await session.execute(stmt)
        transport = result.unique().scalar_one_or_none()

        return transport

    async def get_transports(
        self,
        session: AsyncSession,
        count: int | None,
        start: int = 0,
        transportType: TransportTypeEnum | Type[Empty] = Empty,
        userId: uuid.UUID | Type[Empty] = Empty,
    ) -> Sequence[Transport]:
        stmt = select(Transport).order_by(Transport.created_at)

        if count is not None:
            offset = start
            stmt = stmt.limit(count).offset(offset)

        filters = []

        if transportType is not Empty:
            filters.append(Transport.transportType == transportType)
        if userId is not Empty:
            filters.append(Transport.userId == userId)

        stmt = stmt.where(*filters)

        result = await session.execute(stmt)
        transports = result.scalars().all()

        return transports

    async def get_transports_by_location(
        self,
        session: AsyncSession,
        latitude: float,
        longitude: float,
        radius: float,
        count: int | None,
        start: int = 0,
        transportType: TransportTypeEnum | Type[Empty] = Empty,
    ) -> Sequence[Transport]:
        stmt = select(Transport).order_by(Transport.created_at)

        if count is not None:
            offset = start
            stmt = stmt.limit(count).offset(offset)

        filters = []

        if transportType is not Empty:
            filters.append(Transport.transportType == transportType)

        filters.append(
            func.sqrt(
                func.pow(Transport.latitude - latitude, 2)
                + func.pow(Transport.longitude - longitude, 2)
            )
            <= radius
        )

        stmt = stmt.where(*filters)

        result = await session.execute(stmt)
        transports = result.scalars().all()

        return transports

    async def update_transport(
        self,
        session: AsyncSession,
        transport: Transport,
        canBeRented: bool | Type[Empty] = Empty,
        transportType: TransportTypeEnum | Type[Empty] = Empty,
        model: str | Type[Empty] = Empty,
        color: str | Type[Empty] = Empty,
        identifier: str | Type[Empty] = Empty,
        description: str | None | Type[Empty] = Empty,
        latitude: float | None | Type[Empty] = Empty,
        longitude: float | Type[Empty] = Empty,
        minutePrice: float | Type[Empty] = Empty,
        dayPrice: float | None | Type[Empty] = Empty,
        userId: int | Type[Empty] = Empty,
    ) -> Transport:
        if canBeRented is not Empty:
            transport.canBeRented = canBeRented
        if transportType is not Empty:
            transport.transportType = transportType
        if model is not Empty:
            transport.model = model
        if color is not Empty:
            transport.color = color
        if identifier is not Empty:
            transport.identifier = identifier
        if description is not Empty:
            transport.description = description
        if latitude is not Empty:
            transport.latitude = latitude
        if longitude is not Empty:
            transport.longitude = longitude
        if minutePrice is not Empty:
            transport.minutePrice = minutePrice
        if dayPrice is not Empty:
            transport.dayPrice = dayPrice
        if userId is not Empty:
            transport.userId = userId

        session.add_all([transport])

        return transport

    async def create_transport(
        self,
        session: AsyncSession,
        canBeRented: bool,
        transportType: str,
        model: TransportTypeEnum,
        color: str,
        identifier: str,
        latitude: float,
        longitude: float,
        userId: uuid.UUID,
        description: str | None = None,
        minutePrice: float | None = None,
        dayPrice: float | None = None,
    ):
        transport = Transport(
            canBeRented=canBeRented,
            transportType=transportType,
            model=model,
            color=color,
            identifier=identifier,
            description=description,
            latitude=latitude,
            longitude=longitude,
            minutePrice=minutePrice,
            dayPrice=dayPrice,
            userId=userId,
        )
        session.add_all([transport])

        return transport

    async def delete_rent(self, session: AsyncSession, rentId: uuid.UUID) -> None:
        stmt = delete(Rent).where(Rent.id == rentId)
        await session.execute(stmt)

    async def get_rent(
        self,
        session: AsyncSession,
        userId: uuid.UUID | Type[Empty] = Empty,
        rentId: uuid.UUID | Type[Empty] = Empty,
        transportId: uuid.UUID | Type[Empty] = Empty,
        timeStart: datetime | Type[Empty] = Empty,
        timeEnd: datetime | Type[Empty] = Empty,
        priceOfUnit: float | Type[Empty] = Empty,
        priceType: RentPriceEnum | Type[Empty] = Empty,
        final_price: float | Type[Empty] = Empty,
    ) -> Rent | None:
        filters = []
        if userId is not Empty:
            filters.append(Rent.id == userId)
        if rentId is not Empty:
            filters.append(Rent.id == rentId)
        if transportId is not Empty:
            filters.append(Rent.transportId == transportId)
        if timeStart is not Empty:
            filters.append(Rent.timeStart == timeStart)
        if timeEnd is not Empty:
            filters.append(Rent.timeEnd == timeEnd)
        if priceOfUnit is not Empty:
            filters.append(Rent.priceOfUnit == priceOfUnit)
        if priceType is not Empty:
            filters.append(Rent.priceType == priceType)
        if final_price is not Empty:
            filters.append(Rent.finalPrice == final_price)

        stmt = select(Rent).where(*filters)
        result = await session.execute(stmt)
        rent = result.unique().scalar_one_or_none()

        return rent

    async def get_rents(
        self,
        session: AsyncSession,
        count: int | None,
        start: int = 0,
        userId: uuid.UUID | Type[Empty] = Empty,
        rentId: uuid.UUID | Type[Empty] = Empty,
        transportId: uuid.UUID | Type[Empty] = Empty,
        timeStart: datetime | Type[Empty] = Empty,
        timeEnd: datetime | Type[Empty] = Empty,
        priceOfUnit: float | Type[Empty] = Empty,
        priceType: RentPriceEnum | Type[Empty] = Empty,
        final_price: float | Type[Empty] = Empty,
    ) -> Sequence[Rent]:
        stmt = select(Rent).order_by(Rent.created_at)

        if count is not None:
            offset = start
            stmt = stmt.limit(count).offset(offset)

        filters = []
        if userId is not Empty:
            filters.append(Rent.userId == userId)
        if rentId is not Empty:
            filters.append(Rent.id == rentId)
        if transportId is not Empty:
            filters.append(Rent.transportId == transportId)
        if timeStart is not Empty:
            filters.append(Rent.timeStart == timeStart)
        if timeEnd is not Empty:
            filters.append(Rent.timeEnd == timeEnd)
        if priceOfUnit is not Empty:
            filters.append(Rent.priceOfUnit == priceOfUnit)
        if priceType is not Empty:
            filters.append(Rent.priceType == priceType)
        if final_price is not Empty:
            filters.append(Rent.finalPrice == final_price)

        stmt = stmt.where(*filters)
        print(stmt)

        result = await session.execute(stmt)
        rents = result.scalars().all()

        return rents

    async def create_rent(
        self,
        session: AsyncSession,
        transportId: uuid.UUID,
        userId: uuid.UUID,
        time_start: datetime,
        price_of_unit: float,
        price_type: RentPriceEnum,
        final_price: float | None = None,
        time_end: datetime | None = None,
    ) -> Rent:
        rent = Rent(
            transportId=transportId,
            userId=userId,
            timeStart=time_start,
            timeEnd=time_end,
            priceOfUnit=price_of_unit,
            priceType=price_type,
            finalPrice=final_price,
        )
        session.add_all([rent])

        return rent

    async def update_rent(
        self,
        session: AsyncSession,
        rent: Rent,
        userId: uuid.UUID | Type[Empty] = Empty,
        transportId: uuid.UUID | Type[Empty] = Empty,
        timeStart: datetime | Type[Empty] = Empty,
        timeEnd: datetime | Type[Empty] = Empty,
        priceOfUnit: float | Type[Empty] = Empty,
        priceType: RentPriceEnum | Type[Empty] = Empty,
        final_price: float | Type[Empty] = Empty,
    ) -> Rent:
        if userId is not Empty:
            rent.userId = userId
        if transportId is not Empty:
            rent.transportId = transportId
        if timeStart is not Empty:
            rent.timeStart = timeStart
        if timeEnd is not Empty:
            rent.timeEnd = timeEnd
        if priceOfUnit is not Empty:
            rent.priceOfUnit = priceOfUnit
        if priceType is not Empty:
            rent.priceType = priceType
        if final_price is not Empty:
            rent.finalPrice = final_price

        session.add_all([rent])

        return rent


def get_service(settings: MonolitSettings) -> MonolitDatabaseService:
    return MonolitDatabaseService(dsn=str(settings.db_dsn))
