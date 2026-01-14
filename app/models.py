from datetime import datetime
from typing import Any

from pydantic import field_validator
from sqlmodel import Field, SQLModel


class Contact(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    email: str
    phone: str | None = Field(default=None)
    mobile: str | None = Field(default=None)
    vat: str | None = Field(default=None)
    active: bool
    is_company: bool
    company_name: str | None = Field(default=None)
    street: str | None = Field(default=None)
    city: str | None = Field(default=None)
    state: str | None = Field(default=None)
    zip_code: str | None = Field(default=None, validation_alias="zip")
    country: str | None = Field(default=None)
    write_date: datetime

    @field_validator("phone", "mobile", "vat", "company_name", "street", "city", "state", "zip_code", mode="before")
    @classmethod
    def false_to_none(cls, v: Any) -> Any:
        return None if not v else v


class Invoice(SQLModel, table=True):
    id: int = Field(primary_key=True)
