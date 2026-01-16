from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import func, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, delete, select

from app.api.schemas import PaginatedResponse
from app.models import Contact

CHUNK_SIZE = 2000
INSERT_QUERY_TEMPLATE = text(
    """
    INSERT INTO contact (
        id, name, email, phone, mobile, vat, active, is_company, company_name,
        street, city, state, zip_code, country, write_date
    )
    VALUES (
        :id, :name, :email, :phone, :mobile, :vat, :active, :is_company, :company_name,
        :street, :city, :state, :zip_code, :country, :write_date
    )
    """
)


class ContactsService:
    async def get_contacts(self, session: AsyncSession, limit: int, offset: int) -> PaginatedResponse[Contact]:
        items_query = select(Contact)
        count_query = items_query.with_only_columns(func.count(col(Contact.id)))

        total = await session.scalar(count_query)
        items = (
            (await session.execute(items_query.order_by(col(Contact.id)).limit(limit).offset(offset))).scalars().all()
        )

        return PaginatedResponse(items=items, total=total or 0)

    async def get_contact(self, session: AsyncSession, contact_id: int) -> Contact:
        contact = await session.get(Contact, contact_id)
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")

        return contact

    async def refresh_contacts(self, session: AsyncSession, contacts: Sequence[Contact]) -> None:
        contacts_mapping = [contact.model_dump() for contact in contacts]
        async with session.begin():
            await session.execute(delete(Contact))
            for i in range(0, len(contacts), CHUNK_SIZE):
                await session.execute(INSERT_QUERY_TEMPLATE, contacts_mapping[i : i + CHUNK_SIZE])


contacts_service = ContactsService()
