from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from app.api.schemas import JSENDResponseFail
from app.data_sync import start_data_sync
from app.utils import init_app

app = FastAPI(
    title="Odoo Integration",
    docs_url="/api/docs",
)
init_app(app)


@app.on_event("startup")
def on_startup() -> None:
    start_data_sync()


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello!"}


@app.exception_handler(HTTPException)
def handle_http_exception(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=JSENDResponseFail(data=exc.detail).model_dump(),
    )
