import logging
from typing import Callable

from fastapi import FastAPI, Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

from app.api.routers import api_router
from app.api.schemas import JSENDResponseError

logger = logging.getLogger(__name__)


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)
        except Exception as exc:
            logger.exception(f"Unhandled {exc} error on {request.url}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=JSENDResponseError(data="Unexpected exception occurred").model_dump(),
            )


def init_app(app: FastAPI) -> None:
    app.add_middleware(ExceptionHandlerMiddleware)
    app.include_router(api_router)
