"""add description to products

Revision ID: 0002_add_product_description
Revises: 0001_create_products
Create Date: 2026-04-25 16:40:00
"""

from alembic import op
import sqlalchemy as sa

revision = "0002_add_product_description"
down_revision = "0001_create_products"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("products") as batch_op:
        batch_op.add_column(
            sa.Column(
                "description",
                sa.Text(),
                nullable=False,
                server_default="Описание отсутствует",
            )
        )

    op.execute(
        sa.text(
            "UPDATE products "
            "SET description = CASE "
            "WHEN title = 'Keyboard' THEN 'Механическая клавиатура для повседневной работы.' "
            "WHEN title = 'Mouse' THEN 'Оптическая мышь для офисных задач.' "
            "ELSE description END"
        )
    )

    with op.batch_alter_table("products") as batch_op:
        batch_op.alter_column("description", server_default=None)


def downgrade() -> None:
    with op.batch_alter_table("products") as batch_op:
        batch_op.drop_column("description")
