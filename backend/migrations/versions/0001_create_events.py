"""Create the initial events table.

Revision ID: 0001_create_events
Revises:
Create Date: 2026-10-29
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_create_events"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("event_name", sa.String(length=80), nullable=False),
        sa.Column("user_id", sa.String(length=120), nullable=False),
        sa.Column("session_id", sa.String(length=120), nullable=False),
        sa.Column("country", sa.String(length=80), server_default="Unknown", nullable=False),
        sa.Column("device", sa.String(length=40), server_default="desktop", nullable=False),
        sa.Column("value", sa.Float(), server_default="0", nullable=False),
        sa.Column("occurred_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_events_event_name", "events", ["event_name"])
    op.create_index("ix_events_user_id", "events", ["user_id"])
    op.create_index("ix_events_session_id", "events", ["session_id"])
    op.create_index("ix_events_country", "events", ["country"])
    op.create_index("ix_events_occurred_at", "events", ["occurred_at"])
    op.create_index("ix_events_time_name", "events", ["occurred_at", "event_name"])


def downgrade() -> None:
    op.drop_index("ix_events_time_name", table_name="events")
    op.drop_index("ix_events_occurred_at", table_name="events")
    op.drop_index("ix_events_country", table_name="events")
    op.drop_index("ix_events_session_id", table_name="events")
    op.drop_index("ix_events_user_id", table_name="events")
    op.drop_index("ix_events_event_name", table_name="events")
    op.drop_table("events")
