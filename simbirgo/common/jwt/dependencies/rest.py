import uuid

import fastapi
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from simbirgo.common.api.exceptions import HTTPNotAuthenticated
from simbirgo.common.jwt.methods import JWTMethods

oauth2_scheme = HTTPBearer(auto_error=False)


async def get_request_access_token(
    credentials: HTTPAuthorizationCredentials = fastapi.Security(oauth2_scheme),
) -> str | None:
    access_token = None
    if credentials and credentials.scheme == "Bearer":
        access_token = credentials.credentials
    return access_token


async def get_request_user_id(
    response: fastapi.Response,
    request: fastapi.Request,
    access_token: str = fastapi.Depends(get_request_access_token),
) -> uuid.UUID | None:
    refresh_token = None

    jwt_methods: JWTMethods = request.app.service.jwt_methods

    user_id = None
    if access_token is not None:
        user_id = jwt_methods.decode_access_token(access_token)

    if user_id is None:
        if refresh_token is None:
            return None
        user_id = jwt_methods.decode_refresh_token(refresh_token)
        if user_id is None:
            return None
        # Update access_token and refresh_token
        new_access_token = jwt_methods.issue_access_token(user_id)
        new_refresh_token = jwt_methods.issue_refresh_token(user_id)
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            expires=int(jwt_methods.access_token_expires.total_seconds()),
            path="/",
            secure=True,
            httponly=True,
            samesite="none",
        )
        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            expires=int(jwt_methods.refresh_token_expires.total_seconds()),
            path="/",
            secure=True,
            httponly=True,
            samesite="none",
        )

    return user_id


async def auth_user_id(user_id: uuid.UUID | None = fastapi.Depends(get_request_user_id)):
    if user_id is None:
        raise HTTPNotAuthenticated()

    return user_id
