from fastapi import APIRouter

from app.api.schemas import JSENDResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=JSENDResponse, summary="App health check")
async def health() -> dict[str, str]:
    return {"data": "ok"}
