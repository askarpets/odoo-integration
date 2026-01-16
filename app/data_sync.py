import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.services.contacts import contacts_service
from app.api.services.invoices import invoices_service
from app.api.services.odoo import odoo_service
from app.db import data_sync_session_local
from app.settings import settings

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()


async def sync_contacts(session: AsyncSession) -> None:
    logger.info("Syncing Odoo contacts")
    contacts = await odoo_service.get_contacts()
    await contacts_service.refresh_contacts(session, contacts)


async def sync_invoices(session: AsyncSession) -> None:
    logger.info("Syncing Odoo invoices")
    invoices = await odoo_service.get_invoices()
    await invoices_service.refresh_invoices(session, invoices)


async def sync() -> None:
    async with data_sync_session_local() as session:
        await sync_contacts(session)
        await sync_invoices(session)


def start_data_sync() -> None:
    logger.info("Starting data sync")
    scheduler.add_job(
        sync,
        trigger=IntervalTrigger(minutes=settings.SYNC_INTERVAL_MINUTES),
        id="odoo_sync",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
        misfire_grace_time=60,
    )
    scheduler.start()
