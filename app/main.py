from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from app.api.schemas import JSENDResponseFail
from app.utils import init_app

app = FastAPI(title="Odoo Integration")
init_app(app)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello!"}


@app.exception_handler(HTTPException)
def handle_http_exception(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=JSENDResponseFail(data=exc.detail).model_dump(),
    )
