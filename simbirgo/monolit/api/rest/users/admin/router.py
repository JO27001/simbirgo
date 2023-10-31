import fastapi

from . import handlers

router = fastapi.APIRouter()

router.add_api_route(path="/", methods=["GET"], endpoint=handlers.get_users)
router.add_api_route(path="/{user_id}", methods=["GET"], endpoint=handlers.get_user_by_id)
router.add_api_route(path="/", methods=["POST"], endpoint=handlers.create_user)
router.add_api_route(path="/{user_id}", methods=["PUT"], endpoint=handlers.update_user_by_id)
router.add_api_route(path="/{user_id}", methods=["DELETE"], endpoint=handlers.delete_user_by_id)
