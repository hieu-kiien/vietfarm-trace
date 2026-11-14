"""Allow scoped DELETE on temperature_readings only during telemetry compaction.

Revision ID: 20261114_46
Revises: 20261025_45
Create Date: 2026-11-14 23:00:00.000000

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20261114_46"
down_revision: str | Sequence[str] | None = "20261025_45"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION trg_temperature_readings_append_only()
        RETURNS TRIGGER AS $$
        BEGIN
            IF TG_OP = 'DELETE' AND current_setting('app.telemetry_compaction', true) = 'on' THEN
                RETURN OLD;
            END IF;
            RAISE EXCEPTION 'Dữ liệu đo nhiệt độ chuỗi lạnh là bất biến (append-only), không được phép sửa hoặc xóa.';
        END;
        $$ LANGUAGE plpgsql;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION trg_temperature_readings_append_only()
        RETURNS TRIGGER AS $$
        BEGIN
            RAISE EXCEPTION 'Dữ liệu đo nhiệt độ chuỗi lạnh là bất biến (append-only), không được phép sửa hoặc xóa.';
        END;
        $$ LANGUAGE plpgsql;
        """
    )
