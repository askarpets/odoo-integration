"""Initial Migration

Revision ID: 6139e7e2d9f3
Revises:
Create Date: 2026-01-15 15:05:59.787816

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6139e7e2d9f3"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "contact",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column("mobile", sa.String(), nullable=True),
        sa.Column("vat", sa.String(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("is_company", sa.Boolean(), nullable=False),
        sa.Column("company_name", sa.String(), nullable=False),
        sa.Column("street", sa.String(), nullable=False),
        sa.Column("city", sa.String(), nullable=True),
        sa.Column("state", sa.String(), nullable=True),
        sa.Column("zip_code", sa.String(), nullable=True),
        sa.Column("country", sa.String(), nullable=True),
        sa.Column("write_date", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "invoice",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("invoice_date", sa.DateTime(), nullable=False),
        sa.Column("invoice_date_due", sa.DateTime(), nullable=True),
        sa.Column("partner", sa.String(), nullable=True),
        sa.Column("currency", sa.String(), nullable=True),
        sa.Column("amount_total", sa.Numeric(), nullable=False),
        sa.Column("amount_untaxed", sa.Numeric(), nullable=True),
        sa.Column("amount_tax", sa.Numeric(), nullable=True),
        sa.Column("amount_residual", sa.Numeric(), nullable=True),
        sa.Column("payment_state", sa.String(), nullable=True),
        sa.Column("write_date", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("invoice")
    op.drop_table("contact")
