from typing import Sequence

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models import Contact


class ContactsService:
    async def get_contacts(self, session: AsyncSession, limit: int, offset: int) -> Sequence[Contact]:
        return (await session.execute(select(Contact).limit(limit).offset(offset))).scalars().all()

    async def get_contact(self, session: AsyncSession, contact_id: str) -> Contact:
        contact = await session.get(Contact, contact_id)
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")

        return contact


contacts_service = ContactsService()
