"""add description to products

Revision ID: 0002_add_product_description
Revises: 0001_create_products
Create Date: 2026-04-25 16:40:00
"""

"""Вторая миграция для задания 9.1.

Что делает:
- добавляет обязательное поле description;
- временно ставит server_default, чтобы не сломать старые записи;
- заполняет description у уже существующих товаров;
- затем убирает server_default.
"""

from alembic import op
import sqlalchemy as sa

revision = "0002_add_product_description"
down_revision = "0001_create_products"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # batch_alter_table особенно полезен для SQLite, где ALTER TABLE ограничен.
    with op.batch_alter_table("products") as batch_op:
        batch_op.add_column(
            sa.Column(
                "description",
                sa.Text(),
                nullable=False,
                server_default="Описание отсутствует",
            )
        )

    # Обновляем уже существующие записи осмысленными описаниями.
    op.execute(
        sa.text(
            "UPDATE products "
            "SET description = CASE "
            "WHEN title = 'Keyboard' THEN 'Механическая клавиатура для повседневной работы.' "
            "WHEN title = 'Mouse' THEN 'Оптическая мышь для офисных задач.' "
            "ELSE description END"
        )
    )

    # После заполнения старых данных убираем дефолт:
    # поле остается обязательным, но без автоматической подстановки на уровне БД.
    with op.batch_alter_table("products") as batch_op:
        batch_op.alter_column("description", server_default=None)


def downgrade() -> None:
    # Откат убирает добавленную колонку.
    with op.batch_alter_table("products") as batch_op:
        batch_op.drop_column("description")
