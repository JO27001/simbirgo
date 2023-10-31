import uuid
from typing import Type

from simbirgo.common.utils.empty import Empty
from simbirgo.monolit.api.rest.transport.schemas import (
    TransportCreateRequest,
    TransportUpdateRequest,
)


class AdminTransportCreateRequest(TransportCreateRequest):
    userId: uuid.UUID


class AdminTransportUpdateRequest(TransportUpdateRequest):
    userId: uuid.UUID | Type[Empty] = Empty
