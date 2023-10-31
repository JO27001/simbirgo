import pathlib
from typing import Iterable

import fastapi
from facet import ServiceMixin

from simbirgo.common.api.service import BaseAPIService
from simbirgo.common.jwt import JWTMethods
from simbirgo.common.utils.package import get_version
from simbirgo.monolit.database.service import MonolitDatabaseService
from simbirgo.monolit.settings import MonolitSettings

from . import health, router


class MonolitAPIService(BaseAPIService):
    def __init__(
        self,
        database: MonolitDatabaseService,
        jwt_methods: JWTMethods,
        media_dir_path: pathlib.Path = pathlib.Path("/media"),
        load_file_chunk_size: int = 1024 * 1024,
        version: str = "0.0.0",
        root_url: str = "http://localhost",
        root_path: str = "",
        allowed_origins: Iterable[str] = (),
        port: int = 8000,
    ):
        self._database = database
        self._jwt_methods = jwt_methods
        self._media_dir_path = media_dir_path
        self._load_file_chunk_size = load_file_chunk_size

        super().__init__(
            title="API",
            version=version,
            root_url=root_url,
            root_path=root_path,
            allowed_origins=allowed_origins,
            port=port,
        )

    def setup_app(self, app: fastapi.FastAPI):
        app.add_api_route(path="/health", endpoint=health.health)
        app.include_router(router.router, prefix="/api")

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._database,
        ]

    @property
    def database(self) -> MonolitDatabaseService:
        return self._database

    @property
    def jwt_methods(self) -> JWTMethods:
        return self._jwt_methods

    @property
    def media_dir_path(self) -> pathlib.Path:
        return self._media_dir_path

    @property
    def load_file_chunk_size(self) -> int:
        return self._load_file_chunk_size


def get_service(
    database: MonolitDatabaseService,
    jwt_methods: JWTMethods,
    settings: MonolitSettings,
) -> MonolitAPIService:
    return MonolitAPIService(
        database=database,
        jwt_methods=jwt_methods,
        version=get_version() or "0.0.0",
        root_url=str(settings.root_url),
        root_path=settings.root_path,
        allowed_origins=settings.allowed_origins,
        port=settings.port,
    )
