import uuid
from datetime import datetime
from typing import Type

from pydantic import BaseModel, ConfigDict

from simbirgo.common.utils.empty import Empty
from simbirgo.monolit.database.models import Transport, TransportTypeEnum


class TransportCreateRequest(BaseModel):
    canBeRented: bool
    transportType: TransportTypeEnum
    model: str
    color: str
    identifier: str
    description: str | None
    latitude: float
    longitude: float
    minutePrice: float | None
    dayPrice: float | None


class TransportUpdateRequest(TransportCreateRequest):
    canBeRented: bool | Type[Empty] = Empty
    transportType: str | Type[Empty] = Empty
    model: TransportTypeEnum | Type[Empty] = Empty
    color: str | Type[Empty] = Empty
    identifier: str | Type[Empty] = Empty
    description: str | None | Type[Empty] = Empty
    latitude: float | Type[Empty] = Empty
    longitude: float | Type[Empty] = Empty
    minutePrice: float | None | Type[Empty] = Empty
    dayPrice: float | None | Type[Empty] = Empty


class TransportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    canBeRented: bool
    transportType: TransportTypeEnum
    model: str
    color: str
    identifier: str
    description: str | None
    latitude: float
    longitude: float
    minutePrice: float | None
    dayPrice: float | None
    created_at: datetime
    updated_at: datetime
    userId: uuid.UUID | None

    @classmethod
    def from_db_model(cls, transport: Transport) -> "TransportResponse":
        return cls(
            id=transport.id,
            canBeRented=transport.canBeRented,
            transportType=transport.transportType,
            model=transport.model,
            color=transport.color,
            identifier=transport.identifier,
            description=transport.description,
            latitude=transport.latitude,
            longitude=transport.longitude,
            minutePrice=transport.minutePrice,
            dayPrice=transport.dayPrice,
            created_at=transport.created_at,
            updated_at=transport.updated_at,
            userId=transport.userId,
        )
