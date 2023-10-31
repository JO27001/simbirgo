import fastapi

from simbirgo.common.api.exceptions import HTTPForbidden
from simbirgo.monolit.api.rest.users.dependencies import auth_user
from simbirgo.monolit.database.models import User


async def auth_admin(user: User = fastapi.Depends(auth_user)) -> User:
    if not user.isAdmin:
        raise HTTPForbidden()
    return user
