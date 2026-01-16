from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import PaginatedResponse
from app.api.services.contacts import contacts_service
from app.db import get_session
from app.models import Contact

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("", summary="Get all contacts", response_model=PaginatedResponse[Contact])
async def get_contacts(
    limit: Annotated[int, Query(gt=0)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
    session: AsyncSession = Depends(get_session),
) -> PaginatedResponse[Contact]:
    return await contacts_service.get_contacts(session, limit, offset)


@router.get("/{contact_id}", summary="Get a contact by ID", response_model=Contact)
async def get_contact(contact_id: int, session: AsyncSession = Depends(get_session)) -> Contact:
    return await contacts_service.get_contact(session, contact_id)
