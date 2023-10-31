import fastapi

from simbirgo.common.api.exceptions import HTTPForbidden
from simbirgo.monolit.api.rest.transport.schemas import TransportResponse
from simbirgo.monolit.api.rest.users.dependencies import auth_user, get_path_user
from simbirgo.monolit.api.rest.users.schemas import UserResponse
from simbirgo.monolit.database.models import User
from simbirgo.monolit.database.service import MonolitDatabaseService


async def hesoyam(
    request: fastapi.Request,
    user: User = fastapi.Depends(auth_user),
    path_user: User = fastapi.Depends(get_path_user),
) -> UserResponse:
    database_service: MonolitDatabaseService = request.app.service.database

    if not user.isAdmin and user.id != path_user.id:
        raise HTTPForbidden()

    async with database_service.transaction() as session:
        db_user = await database_service.update_user(
            session=session, user=path_user, balance=path_user.balance + 250_000
        )

    return UserResponse.from_db_model(db_user)
