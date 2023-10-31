import fastapi

from . import handlers

router = fastapi.APIRouter()

router.add_api_route(
    path="/Transport",
    methods=["GET"],
    endpoint=handlers.get_transports_by_location,
)
router.add_api_route(path="/MyHistory", methods=["GET"], endpoint=handlers.get_my_rents)
router.add_api_route(
    path="/TransportHistory/{transport_id}",
    methods=["GET"],
    endpoint=handlers.get_transport_rents,
)
router.add_api_route(path="/New/{transport_id}", methods=["POST"], endpoint=handlers.create_rent)
router.add_api_route(path="/End/{rent_id}", methods=["POST"], endpoint=handlers.end_rent)
router.add_api_route(path="/{rent_id}", methods=["GET"], endpoint=handlers.get_rent)
