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
    state: str | None = Field(default=None, validation_alias="state_id")
    zip_code: str | None = Field(default=None, validation_alias="zip")
    country: str | None = Field(default=None, validation_alias="country_id")
    write_date: datetime

    @field_validator(
        "phone",
        "mobile",
        "vat",
        "company_name",
        "street",
        "city",
        "state",
        "zip_code",
        "country",
        mode="before",
    )
    @classmethod
    def false_to_none(cls, v: Any) -> Any:
        return None if not v else v

    @field_validator("state", "country", mode="before")
    @classmethod
    def list_to_str(cls, v: Any) -> Any:
        return v[-1] if isinstance(v, list) else v


class Invoice(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    invoice_date: datetime
    invoice_date_due: datetime | None = Field(default=None)
    partner: str | None = Field(default=None, validation_alias="partner_id")
    currency: str | None = Field(default=None, validation_alias="currency_id")
    amount_total: float
    amount_untaxed: float | None = Field(default=None)
    amount_tax: float | None = Field(default=None)
    amount_residual: float | None = Field(default=None)
    payment_state: str | None = Field(default=None)
    write_date: datetime

    @field_validator(
        "invoice_date_due",
        "partner",
        "currency",
        "amount_untaxed",
        "amount_tax",
        "amount_residual",
        "payment_state",
        mode="before",
    )
    @classmethod
    def false_to_none(cls, v: Any) -> Any:
        return None if not v else v

    @field_validator("partner", "currency", mode="before")
    @classmethod
    def list_to_str(cls, v: Any) -> Any:
        return v[-1] if isinstance(v, list) else v
