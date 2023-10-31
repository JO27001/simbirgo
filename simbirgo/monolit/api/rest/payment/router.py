import fastapi

from . import handlers

router = fastapi.APIRouter()

router.add_api_route(path="/Hesoyam/{user_id}", methods=["POST"], endpoint=handlers.hesoyam)
