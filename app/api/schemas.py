from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict


class ResponseStatus(StrEnum):
    success = "success"
    fail = "fail"
    error = "error"


class JSENDResponse(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    status: ResponseStatus = ResponseStatus.success
    data: Any | None


class JSENDResponseFail(JSENDResponse):
    status: ResponseStatus = ResponseStatus.fail


class JSENDResponseError(JSENDResponse):
    status: ResponseStatus = ResponseStatus.error
