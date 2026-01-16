from fastapi import APIRouter, status

from app.api.routes.contacts import router as contacts_router
from app.api.routes.health import router as health_router
from app.api.routes.invoices import router as invoices_router
from app.api.schemas import JSENDResponseError

api_router = APIRouter(prefix="/api")
v1_router = APIRouter(
    prefix="/v1",
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": JSENDResponseError}},
)

v1_router.include_router(contacts_router)
v1_router.include_router(invoices_router)

api_router.include_router(health_router)
api_router.include_router(v1_router)
