import fastapi

from . import handlers

router = fastapi.APIRouter()

router.add_api_route(path="/Me", methods=["GET"], endpoint=handlers.get_me)
router.add_api_route(path="/SignIn", methods=["POST"], endpoint=handlers.sign_in)
router.add_api_route(path="/SignUp", methods=["POST"], endpoint=handlers.sign_up)
router.add_api_route(path="/SignOut", methods=["POST"], endpoint=handlers.sign_out)
router.add_api_route(path="/Update", methods=["PUT"], endpoint=handlers.update_me)
