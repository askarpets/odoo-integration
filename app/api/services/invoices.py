from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import func, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, delete, select

from app.api.schemas import PaginatedResponse
from app.models import Invoice

CHUNK_SIZE = 2000
INSERT_QUERY_TEMPLATE = text(
    """
    INSERT INTO invoice (
        id, name, invoice_date, invoice_date_due, partner, currency,
        amount_total, amount_untaxed, amount_tax, amount_residual, payment_state, write_date
    )
    VALUES (
        :id, :name, :invoice_date, :invoice_date_due, :partner, :currency,
        :amount_total, :amount_untaxed, :amount_tax, :amount_residual, :payment_state, :write_date
    )
    """
)


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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")

        return invoice

    async def refresh_invoices(self, session: AsyncSession, invoices: Sequence[Invoice]) -> None:
        invoices_mapping = [invoice.model_dump() for invoice in invoices]
        async with session.begin():
            await session.execute(delete(Invoice))
            for i in range(0, len(invoices), CHUNK_SIZE):
                await session.execute(INSERT_QUERY_TEMPLATE, invoices_mapping[i : i + CHUNK_SIZE])


invoices_service = InvoicesService()
