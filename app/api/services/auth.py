from datetime import UTC, datetime
from logging import getLogger
from typing import Any

from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer
from jwt import decode

from app.settings import settings

logger = getLogger(__name__)


def decode_access_token(access_token: str, key: str, algorithms: list[str]) -> dict[str, Any] | None:
    try:
        return decode(access_token, key, algorithms=algorithms)
    except Exception as e:
        logger.warning(f"An error occurred while decoding access token: {str(e)}")
        return None


def is_token_expired(access_token_info: dict[str, Any]) -> bool:
    now = datetime.now(UTC).timestamp()
    return access_token_info.get("exp", 0) <= now


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid authentication scheme.")

            access_token_info = decode_access_token(
                access_token=credentials.credentials,
                key=settings.ACCESS_TOKEN_VERIFICATION_KEY,
                algorithms=[settings.ACCESS_TOKEN_SIGNATURE_ALGORITHM],
            )

            if not access_token_info:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token provided.")

            if is_token_expired(access_token_info=access_token_info):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Expired token provided.")

            return credentials.credentials
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization code.")
