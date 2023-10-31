import fastapi
import sqlalchemy.exc

from simbirgo.common.api.exceptions import HTTPForbidden
from simbirgo.common.jwt.dependencies.rest import get_request_access_token
from simbirgo.common.jwt.methods import JWTMethods
from simbirgo.common.utils.empty import Empty
from simbirgo.monolit.database.models import User
from simbirgo.monolit.database.service import MonolitDatabaseService

from .dependencies import auth_user
from .schemas import JWTTokensResponse, UserCreateRequest, UserResponse, UserUpdateRequest
from .utils import prepare_jwt


async def get_me(user: User = fastapi.Depends(auth_user)) -> UserResponse:
    return UserResponse.from_db_model(user)


async def sign_in(
    request: fastapi.Request,
    response: fastapi.Response,
    data: UserUpdateRequest = fastapi.Body(embed=False),
) -> JWTTokensResponse:
    database_service: MonolitDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        db_user = await database_service.get_user(
            session=session, username=data.username, password=data.password
        )

    if db_user is None:
        raise HTTPForbidden()

    return prepare_jwt(request=request, response=response, db_user=db_user)


async def sign_up(
    request: fastapi.Request,
    response: fastapi.Response,
    data: UserCreateRequest = fastapi.Body(embed=False),
) -> JWTTokensResponse:
    database_service: MonolitDatabaseService = request.app.service.database

    try:
        async with database_service.transaction() as session:
            db_user = await database_service.create_user(
                session=session, username=data.username, password=data.password
            )
    except sqlalchemy.exc.IntegrityError:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Username alrady exist.",
        )

    return prepare_jwt(request=request, response=response, db_user=db_user)


def sign_out(
    request: fastapi.Request,
    response: fastapi.Response,
    token: str = fastapi.Depends(get_request_access_token),
):
    jwt_methods: JWTMethods = request.app.service.jwt_methods
    jwt_methods.add_to_blacklist(token=token)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")


async def update_me(
    request: fastapi.Request,
    user: User = fastapi.Depends(auth_user),
    data: UserUpdateRequest = fastapi.Body(embed=False),
) -> UserResponse:
    database_service: MonolitDatabaseService = request.app.service.database
    async with database_service.transaction() as session:
        user = await database_service.update_user(
            user=user,
            session=session,
            username=data.username or Empty,
            password=data.password or Empty,
        )

    return UserResponse.from_db_model(user)
