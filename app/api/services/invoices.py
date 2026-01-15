from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select

from app.api.schemas import PaginatedResponse
from app.models import Invoice


class InvoicesService:
    async def get_invoices(self, session: AsyncSession, limit: int, offset: int) -> PaginatedResponse[Invoice]:
        items_query = select(Invoice)
        count_query = items_query.with_only_columns(func.count(col(Invoice.id)))

        total = await session.scalar(count_query)
        items = (await session.execute(items_query.limit(limit).offset(offset))).scalars().all()

        return PaginatedResponse(items=items, total=total or 0)

    async def get_invoice(self, session: AsyncSession, invoice_id: int) -> Invoice:
        invoice = await session.get(Invoice, invoice_id)
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")

        return invoice


invoices_service = InvoicesService()
