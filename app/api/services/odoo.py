import asyncio
import ssl
from datetime import timezone
from typing import Any, Type
from xmlrpc.client import ServerProxy

from pydantic import BaseModel

from app.models import Contact, Invoice
from app.settings import settings

CONTACT_FIELDS = [
    "id",
    "name",
    "email",
    "phone",
    "company_name",
    "is_company",
    "active",
    "vat",
    "street",
    "street2",
    "city",
    "state_id",
    "zip",
    "country_id",
    "write_date",
]
INVOICE_FIELDS = [
    "id",
    "name",
    "invoice_date",
    "invoice_date_due",
    "partner_id",
    "currency_id",
    "amount_untaxed",
    "amount_tax",
    "amount_total",
    "amount_residual",
    "payment_state",
    "write_date",
]
CONTACT_MODEL = "res.partner"
INVOICE_MODEL = "account.move"


class OdooService:
    def __init__(self, url: str, database: str, user: str, password: str) -> None:
        self._url = url
        self._database = database
        self._user = user
        self._password = password

        ssl_context = ssl.create_default_context()
        common = ServerProxy(f"{url}/xmlrpc/2/common", context=ssl_context, allow_none=True)
        self._uid = common.authenticate(database, user, password, {})
        if not self._uid:
            raise RuntimeError("Odoo authentication failed")

        self._models = ServerProxy(f"{url}/xmlrpc/2/object", context=ssl_context, allow_none=True)

    def _get_items_sync(
        self,
        model_type: Type[BaseModel],
        model_name: str,
        fields: list[str],
        limit: int = settings.ODOO_FETCH_LIMIT,
    ) -> list[BaseModel]:
        offset = 0
        output: list[BaseModel] = []

        while True:
            items: Any = self._models.execute_kw(
                self._database,
                self._uid,
                self._password,
                model_name,
                "search_read",
                [],
                {"fields": fields, "limit": limit, "offset": offset, "order": "write_date asc"},
            )
            if not items:
                break

            for item in items:
                item = model_type.model_validate(item)
                item.write_date = item.write_date.astimezone(timezone.utc)  # type: ignore

                output.append(item)

            offset += len(items)

        return output

    async def get_contacts(self) -> list[Contact]:
        return await asyncio.to_thread(self._get_items_sync, Contact, CONTACT_MODEL, CONTACT_FIELDS)  # type: ignore

    async def get_invoices(self) -> list[Invoice]:
        return await asyncio.to_thread(self._get_items_sync, Invoice, INVOICE_MODEL, INVOICE_FIELDS)  # type: ignore


odoo_service = OdooService(
    url=settings.ODOO_URL,
    database=settings.ODOO_DATABASE,
    user=settings.ODOO_USER,
    password=settings.ODOO_PASSWORD,
)
