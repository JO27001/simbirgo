import fastapi

from simbirgo.common.jwt import JWTMethods
from simbirgo.monolit.database.models import User

from .schemas import JWTTokensResponse


def prepare_jwt(
    request: fastapi.Request, response: fastapi.Response, db_user: User
) -> JWTTokensResponse:
    jwt_methods: JWTMethods = request.app.service.jwt_methods
    access_token = jwt_methods.issue_access_token(db_user.id)
    refresh_token = jwt_methods.issue_refresh_token(db_user.id)

    add_to_cookies = [
        ("access_token", access_token, jwt_methods.access_token_expires),
        ("refresh_token", refresh_token, jwt_methods.refresh_token_expires),
    ]
    for name, token, expires in add_to_cookies:
        response.set_cookie(
            key=name,
            value=token,
            expires=expires,
            path="/",
            secure=True,
            httponly=True,
            samesite="none",
        )

    return JWTTokensResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )
