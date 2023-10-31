import fastapi

from . import handlers

router = fastapi.APIRouter()

router.add_api_route(path="/", methods=["GET"], endpoint=handlers.get_transports)
router.add_api_route(path="/{transport_id}", methods=["GET"], endpoint=handlers.get_transport)
router.add_api_route(path="/", methods=["POST"], endpoint=handlers.create_transport)
router.add_api_route(path="/{transport_id}", methods=["PUT"], endpoint=handlers.update_transport)
router.add_api_route(path="/{transport_id}", methods=["DELETE"], endpoint=handlers.delete_transport)
