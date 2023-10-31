import fastapi

import simbirgo.monolit.api.rest.payment as payment
import simbirgo.monolit.api.rest.rent as rent
import simbirgo.monolit.api.rest.rent.admin as rent_admin
import simbirgo.monolit.api.rest.transport as transport
import simbirgo.monolit.api.rest.transport.admin as transport_admin
import simbirgo.monolit.api.rest.users as users
import simbirgo.monolit.api.rest.users.admin as users_admin

router = fastapi.APIRouter()

router.include_router(users_admin.router, prefix="/Account/Admin", tags=["Users admin"])
router.include_router(users.router, prefix="/Account", tags=["Users"])
router.include_router(transport_admin.router, prefix="/Transport/Admin", tags=["Transport admin"])
router.include_router(transport.router, prefix="/Transport", tags=["Transport"])
router.include_router(rent.router, prefix="/Rent", tags=["Rent"])
router.include_router(rent_admin.router, prefix="/Rent/Admin", tags=["Rent admin"])
router.include_router(payment.router, prefix="/Payment", tags=["Payment"])
