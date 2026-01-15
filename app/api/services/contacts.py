from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select

from app.api.schemas import PaginatedResponse
from app.models import Contact


class ContactsService:
    async def get_contacts(self, session: AsyncSession, limit: int, offset: int) -> PaginatedResponse[Contact]:
        items_query = select(Contact)
        count_query = items_query.with_only_columns(func.count(col(Contact.id)))

        total = await session.scalar(count_query)
        items = (await session.execute(items_query.limit(limit).offset(offset))).scalars().all()

        return PaginatedResponse(items=items, total=total or 0)

    async def get_contact(self, session: AsyncSession, contact_id: int) -> Contact:
        contact = await session.get(Contact, contact_id)
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")

        return contact


contacts_service = ContactsService()
