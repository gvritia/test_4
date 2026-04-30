"""create products table

Revision ID: 0001_create_products
Revises:
Create Date: 2026-04-25 16:30:00
"""

from decimal import Decimal

from alembic import op
import sqlalchemy as sa

revision = "0001_create_products"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("count", sa.Integer(), nullable=False),
    )
    op.create_index(op.f("ix_products_id"), "products", ["id"], unique=False)

    products_table = sa.table(
        "products",
        sa.column("id", sa.Integer()),
        sa.column("title", sa.String(length=150)),
        sa.column("price", sa.Numeric(10, 2)),
        sa.column("count", sa.Integer()),
    )

    op.bulk_insert(
        products_table,
        [
            {
                "id": 1,
                "title": "Keyboard",
                "price": Decimal("1299.99"),
                "count": 10,
            },
            {
                "id": 2,
                "title": "Mouse",
                "price": Decimal("799.50"),
                "count": 25,
            },
        ],
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_products_id"), table_name="products")
    op.drop_table("products")
