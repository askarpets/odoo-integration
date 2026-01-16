from fastapi import APIRouter, Depends, status

from app.api.routes.contacts import router as contacts_router
from app.api.routes.health import router as health_router
from app.api.routes.invoices import router as invoices_router
from app.api.schemas import JSENDResponseError, JSENDResponseFail
from app.api.services.auth import JWTBearer

api_router = APIRouter(prefix="/api")
v1_router = APIRouter(
    prefix="/v1",
    dependencies=[Depends(JWTBearer())],
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": JSENDResponseFail},
        status.HTTP_401_UNAUTHORIZED: {"model": JSENDResponseFail},
        status.HTTP_403_FORBIDDEN: {"model": JSENDResponseFail},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": JSENDResponseError},
    },
)

v1_router.include_router(contacts_router)
v1_router.include_router(invoices_router)

api_router.include_router(health_router)
api_router.include_router(v1_router)
