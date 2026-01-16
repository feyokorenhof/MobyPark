"""add discount fields to reservations

Revision ID: d12781f686a2
Revises: f8016a0808ea
Create Date: 2026-01-12 21:10:05.042956

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d12781f686a2"
down_revision: Union[str, None] = "f8016a0808ea"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "reservations", sa.Column("discount_code_id", sa.Integer(), nullable=True)
    )
    op.create_index(
        "ix_reservations_discount_code_id", "reservations", ["discount_code_id"]
    )
    op.create_foreign_key(
        "fk_reservations_discount_code_id",
        "reservations",
        "discount_codes",
        ["discount_code_id"],
        ["id"],
        ondelete="SET NULL",
    )

    op.add_column(
        "reservations",
        sa.Column("original_cost", sa.Float(), nullable=False, server_default="0"),
    )
    op.add_column(
        "reservations",
        sa.Column("discount_amount", sa.Float(), nullable=False, server_default="0"),
    )


def downgrade() -> None:
    op.drop_column("reservations", "discount_amount")
    op.drop_column("reservations", "original_cost")

    op.drop_constraint(
        "fk_reservations_discount_code_id", "reservations", type_="foreignkey"
    )
    op.drop_index("ix_reservations_discount_code_id", table_name="reservations")
    op.drop_column("reservations", "discount_code_id")
