from facet import ServiceMixin

from .api.service import MonolitAPIService


class UsersService(ServiceMixin):
    def __init__(self, api: MonolitAPIService):
        self._api = api

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._api,
        ]

    @property
    def api(self) -> MonolitAPIService:
        return self._api


def get_service(api: MonolitAPIService) -> UsersService:
    return UsersService(api=api)
