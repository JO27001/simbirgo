import uuid
from datetime import datetime
from typing import Type

from pydantic import BaseModel

from simbirgo.common.utils.empty import Empty
from simbirgo.monolit.database.models import Rent, RentPriceEnum


class AdminRentCreateRequest(BaseModel):
    transportId: uuid.UUID
    userId: uuid.UUID
    timeStart: datetime
    timeEnd: datetime | None = None
    priceOfUnit: float
    priceType: RentPriceEnum
    finalPrice: float | None = None


class AdminRentUpdateRequest(BaseModel):
    transportId: uuid.UUID | Type[Empty] = Empty
    userId: uuid.UUID | Type[Empty] = Empty
    timeStart: datetime | Type[Empty] = Empty
    timeEnd: datetime | Type[Empty] | None = Empty
    priceOfUnit: float | Type[Empty] = Empty
    priceType: RentPriceEnum | Type[Empty] = Empty
    finalPrice: float | Type[Empty] | None = Empty


class RentResponse(BaseModel):
    id: uuid.UUID
    transportId: uuid.UUID
    userId: uuid.UUID
    timeStart: datetime
    timeEnd: datetime | None
    priceOfUnit: float
    priceType: RentPriceEnum
    finalPrice: float | None
    updated_at: datetime
    created_at: datetime

    @classmethod
    def from_db_model(cls, rent: Rent) -> "RentResponse":
        return cls(
            id=rent.id,
            transportId=rent.transportId,
            userId=rent.userId,
            timeStart=rent.timeStart,
            timeEnd=rent.timeEnd,
            priceOfUnit=rent.priceOfUnit,
            priceType=rent.priceType,
            finalPrice=rent.finalPrice,
            updated_at=rent.updated_at,
            created_at=rent.created_at,
        )
