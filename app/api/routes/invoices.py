from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import PaginatedResponse
from app.api.services.invoices import invoices_service
from app.db import get_session
from app.models import Invoice

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.get("", summary="Get all invoices", response_model=PaginatedResponse[Invoice])
async def get_invoices(
    limit: Annotated[int, Query(gt=0)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
    session: AsyncSession = Depends(get_session),
) -> PaginatedResponse[Invoice]:
    return await invoices_service.get_invoices(session, limit, offset)


@router.get("/{invoice_id}", summary="Get an invoice by ID", response_model=Invoice)
async def get_invoice(invoice_id: int, session: AsyncSession = Depends(get_session)) -> Invoice:
    return await invoices_service.get_invoice(session, invoice_id)
