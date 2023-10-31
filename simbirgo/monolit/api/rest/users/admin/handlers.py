import fastapi
import sqlalchemy.exc

from simbirgo.common.api.dependencies.pagination import Pagination, pagination
from simbirgo.common.utils.empty import Empty
from simbirgo.monolit.api.rest.users.dependencies import auth_admin, get_path_user
from simbirgo.monolit.api.rest.users.schemas import UserResponse
from simbirgo.monolit.database.models import User
from simbirgo.monolit.database.service import MonolitDatabaseService

from .schemas import AdminCreateRequest, AdminUpdateRequest


async def get_users(
    request: fastapi.Request,
    pagination: Pagination = fastapi.Depends(pagination),
    _: User = fastapi.Depends(auth_admin),
) -> list[UserResponse]:
    database_service: MonolitDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        db_users = await database_service.get_users(
            session=session, start=pagination.start, count=pagination.count
        )

    return [
        UserResponse.from_db_model(i, with_hash_password=True, with_is_admin=True) for i in db_users
    ]


async def get_user_by_id(
    path_user: User = fastapi.Depends(get_path_user),
    _: User = fastapi.Depends(auth_admin),
) -> UserResponse:
    return UserResponse.from_db_model(path_user, with_hash_password=True, with_is_admin=True)


async def create_user(
    request: fastapi.Request,
    data: AdminCreateRequest = fastapi.Body(embed=False),
    _: User = fastapi.Depends(auth_admin),
) -> UserResponse:
    database_service: MonolitDatabaseService = request.app.service.database

    try:
        async with database_service.transaction() as session:
            db_user = await database_service.create_user(
                session=session,
                username=data.username,
                password=data.password,
                balance=data.balance,
                isAdmin=data.isAdmin,
            )
    except sqlalchemy.exc.IntegrityError:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Username alrady exist.",
        )

    return UserResponse.from_db_model(db_user, with_hash_password=True, with_is_admin=True)


async def update_user_by_id(
    request: fastapi.Request,
    path_user: User = fastapi.Depends(get_path_user),
    data: AdminUpdateRequest = fastapi.Body(embed=False),
    _: User = fastapi.Depends(auth_admin),
) -> UserResponse:
    database_service: MonolitDatabaseService = request.app.service.database

    try:
        async with database_service.transaction() as session:
            db_user = await database_service.update_user(
                session=session,
                user=path_user,
                username=data.username,
                password=data.password,
                balance=data.balance,
                isAdmin=data.isAdmin,
            )
    except sqlalchemy.exc.IntegrityError:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Username alrady exist.",
        )

    return UserResponse.from_db_model(db_user, with_hash_password=True, with_is_admin=True)


async def delete_user_by_id(
    request: fastapi.Request,
    path_user: User = fastapi.Depends(get_path_user),
    _: User = fastapi.Depends(auth_admin),
):
    database_service: MonolitDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        await database_service.delete_user(session=session, userId=path_user.id)
