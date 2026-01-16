"""add discount codes

Revision ID: f8016a0808ea
Revises: 125f58dd922e
Create Date: 2026-01-12 21:04:07.519864

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f8016a0808ea"
down_revision: Union[str, None] = "125f58dd922e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1) discount_codes
    op.create_table(
        "discount_codes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("percent", sa.Integer(), nullable=False),
        sa.Column(
            "enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")
        ),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column(
            "single_use", sa.Boolean(), nullable=False, server_default=sa.text("false")
        ),
        sa.Column("max_uses", sa.Integer(), nullable=True),
        sa.Column("uses_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("valid_from", sa.DateTime(timezone=True), nullable=True),
        sa.Column("valid_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.create_index("ix_discount_codes_code", "discount_codes", ["code"], unique=True)

    # 2) discount_redemptions
    op.create_table(
        "discount_redemptions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "discount_code_id",
            sa.Integer(),
            sa.ForeignKey("discount_codes.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "reservation_id",
            sa.Integer(),
            sa.ForeignKey("reservations.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.create_index(
        "ix_discount_redemptions_discount_code_id",
        "discount_redemptions",
        ["discount_code_id"],
    )
    op.create_index(
        "ix_discount_redemptions_user_id",
        "discount_redemptions",
        ["user_id"],
    )
    op.create_index(
        "ix_discount_redemptions_reservation_id",
        "discount_redemptions",
        ["reservation_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_discount_redemptions_reservation_id", table_name="discount_redemptions"
    )
    op.drop_index("ix_discount_redemptions_user_id", table_name="discount_redemptions")
    op.drop_index(
        "ix_discount_redemptions_discount_code_id", table_name="discount_redemptions"
    )
    op.drop_table("discount_redemptions")

    op.drop_index("ix_discount_codes_code", table_name="discount_codes")
    op.drop_table("discount_codes")
