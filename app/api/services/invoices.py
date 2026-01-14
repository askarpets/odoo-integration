from typing import Sequence

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models import Invoice


class InvoicesService:
    async def get_invoices(self, session: AsyncSession, limit: int, offset: int) -> Sequence[Invoice]:
        return (await session.execute(select(Invoice).limit(limit).offset(offset))).scalars().all()

    async def get_invoice(self, session: AsyncSession, invoice_id: str) -> Invoice:
        invoice = await session.get(Invoice, invoice_id)
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")

        return invoice


invoices_service = InvoicesService()
