import fastapi

from . import handlers

router = fastapi.APIRouter()


router.add_api_route(
    path="/UserHistory/{user_id}", methods=["GET"], endpoint=handlers.get_user_rents
)
router.add_api_route(
    path="/TransportHistory/{transport_id}",
    methods=["GET"],
    endpoint=handlers.get_transport_rents,
)
router.add_api_route(path="/New", methods=["POST"], endpoint=handlers.create_rent)
router.add_api_route(path="/End/{rent_id}", methods=["POST"], endpoint=handlers.end_rent)
router.add_api_route(path="/{rent_id}", methods=["GET"], endpoint=handlers.get_rent)
router.add_api_route(path="/{rent_id}", methods=["PUT"], endpoint=handlers.update_rent)
router.add_api_route(path="/{rent_id}", methods=["DELETE"], endpoint=handlers.delete_rent)
