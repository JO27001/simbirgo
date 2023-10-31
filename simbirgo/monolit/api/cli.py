import asyncio

import typer
from loguru import logger

from simbirgo.common import jwt
from simbirgo.monolit import database
from simbirgo.monolit.settings import MonolitSettings

from .service import get_service


@logger.catch
def run(ctx: typer.Context):
    settings: MonolitSettings = ctx.obj["settings"]

    jwt_methods = jwt.get_jwt_methods(settings=settings)
    database_service = database.get_service(settings=settings)
    api_service = get_service(
        database=database_service,
        jwt_methods=jwt_methods,
        settings=settings,
    )

    asyncio.run(api_service.run())


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.command(name="run")(run)

    return cli
