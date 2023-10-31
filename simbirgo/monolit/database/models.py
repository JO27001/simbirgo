import enum
import uuid
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    isAdmin: Mapped[bool] = mapped_column(server_default="false")
    balance: Mapped[float] = mapped_column(server_default="0.0")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)


class TransportTypeEnum(str, enum.Enum):
    CAR = "Car"
    BIKE = "Bike"
    SCOOTER = "Scooter"


class Transport(Base):
    __tablename__ = "transports"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    canBeRented: Mapped[bool] = mapped_column(server_default="false")
    transportType: Mapped[TransportTypeEnum] = mapped_column()
    model: Mapped[str] = mapped_column()
    color: Mapped[str] = mapped_column()
    identifier: Mapped[str] = mapped_column()
    description: Mapped[str | None] = mapped_column(nullable=True)
    latitude: Mapped[float] = mapped_column(server_default="0.0")
    longitude: Mapped[float] = mapped_column(server_default="0.0")
    minutePrice: Mapped[float] = mapped_column(server_default="0.0", nullable=True)
    dayPrice: Mapped[float] = mapped_column(server_default="0.0", nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)

    userId: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))


class RentPriceEnum(str, enum.Enum):
    MINUTES = "Minutes"
    DAYS = "Days"


class Rent(Base):
    __tablename__ = "rents"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    transportId: Mapped[uuid.UUID] = mapped_column(ForeignKey("transports.id"))
    userId: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    timeStart: Mapped[datetime] = mapped_column()
    timeEnd: Mapped[datetime] = mapped_column(nullable=True)
    priceOfUnit: Mapped[float] = mapped_column()
    priceType: Mapped[RentPriceEnum] = mapped_column()
    finalPrice: Mapped[float] = mapped_column(nullable=True)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
