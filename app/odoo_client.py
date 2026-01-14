import ssl
from datetime import datetime, timezone
from typing import Any
from xmlrpc.client import ServerProxy

from app.models import Contact
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
CONTACT_MODEL = "res.partner"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class OdooClient:
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

    def _get_contacts_sync(self, updated_at: datetime | None = None) -> tuple[list[Contact], datetime]:
        updated_at = updated_at or datetime(1970, 1, 1)
        updated_at = updated_at.astimezone(timezone.utc)
        domain = [["write_date", ">", updated_at.astimezone(timezone.utc).strftime(DATETIME_FORMAT)]]
        offset = 0
        out: list[Contact] = []

        while True:
            contacts: Any = self._models.execute_kw(
                self._database,
                self._uid,
                self._password,
                CONTACT_MODEL,
                "search_read",
                [domain],
                {
                    "fields": CONTACT_FIELDS,
                    "limit": settings.ODOO_FETCH_LIMIT,
                    "offset": offset,
                    "order": "write_date asc",
                },
            )
            if not contacts:
                break

            for contact in contacts:
                contact = Contact.model_validate(contact)
                contact.write_date = contact.write_date.astimezone(timezone.utc)
                if contact.write_date > updated_at:
                    updated_at = contact.write_date

                out.append(contact)

            offset += len(contacts)

        return out, updated_at
