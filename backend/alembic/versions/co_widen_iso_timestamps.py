"""Widen change-order ISO timestamp columns from String(20) to String(40)

The ``submitted_at`` / ``approved_at`` / ``rejected_at`` /
``contractor_submission_date`` columns on ``oe_changeorders_order`` store
ISO-8601 timestamps stamped by the service via ``datetime.isoformat()``,
e.g. ``2026-05-30T09:58:00.688302+00:00`` (32 chars). They were declared
``String(20)``, which SQLite silently tolerates but PostgreSQL rejects with
``StringDataRightTruncationError: value too long for type character
varying(20)`` — breaking demo seeding and any real change-order
submit/approve/reject on PostgreSQL deployments.

40 matches the convention already used for ISO timestamp strings elsewhere
in the schema (e.g. ``v3019_bid_management``, ``v3020_variations``) and
leaves margin for microseconds and non-UTC offsets.

Revision ID: co_widen_iso_ts
Revises: v3082_changeorders_approval_chain
Create Date: 2026-05-30
"""

import sqlalchemy as sa
from alembic import op

revision = "co_widen_iso_ts"
down_revision = "v3082_changeorders_approval_chain"
branch_labels = None
depends_on = None

TABLE = "oe_changeorders_order"
COLUMNS = (
    "submitted_at",
    "approved_at",
    "rejected_at",
    "contractor_submission_date",
)


def upgrade() -> None:
    with op.batch_alter_table(TABLE) as batch:
        for col in COLUMNS:
            batch.alter_column(
                col,
                existing_type=sa.String(length=20),
                type_=sa.String(length=40),
                existing_nullable=True,
            )


def downgrade() -> None:
    with op.batch_alter_table(TABLE) as batch:
        for col in COLUMNS:
            batch.alter_column(
                col,
                existing_type=sa.String(length=40),
                type_=sa.String(length=20),
                existing_nullable=True,
            )
