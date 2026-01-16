from enum import StrEnum
from typing import Any, Generic, Sequence, TypeVar

from pydantic import BaseModel, ConfigDict

RecordType = TypeVar("RecordType")


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


class PaginatedResponse(BaseModel, Generic[RecordType]):
    items: Sequence[RecordType]
    total: int
