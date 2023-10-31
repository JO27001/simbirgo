from pydantic import AnyUrl
from pydantic_settings import SettingsConfigDict

from simbirgo.common.api.settings import BaseAPISettings
from simbirgo.common.database.settings import BaseDatabaseSettings
from simbirgo.common.jwt.settings import JWTSettings
from simbirgo.common.utils.rsa256 import generate_rsa_keys

access_token = generate_rsa_keys()
refresh_token = generate_rsa_keys()


class MonolitSettings(BaseAPISettings, BaseDatabaseSettings, JWTSettings):
    model_config = SettingsConfigDict(secrets_dir="/run/secrets")

    db_dsn: AnyUrl = AnyUrl("postgresql+asyncpg://simbirgo:simbirgo@database:5432/simbirgo")


def get_settings() -> MonolitSettings:
    return MonolitSettings()
