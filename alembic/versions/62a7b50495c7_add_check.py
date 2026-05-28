"""add check

Revision ID: 62a7b50495c7
Revises: 0002_add_product_description
Create Date: 2026-05-23 14:38:10.357263

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62a7b50495c7'
down_revision: Union[str, Sequence[str], None] = '0002_add_product_description'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("products") as batch_op:
        batch_op.add_column(
            sa.Column(
                "check",
                sa.Boolean(),
                nullable=False,
                server_default=sa.sql.expression.true()
            )
        )

    # "check" - зарезервированное слово SQL, поэтому в raw SQL имя колонки
    # нужно обязательно брать в кавычки.
    op.execute(
        sa.text(
            'UPDATE products '
            'SET "check" = CASE '
            "WHEN title = 'Keyboard' THEN 1 "
            "WHEN title = 'Mouse' THEN 1 "
            "ELSE 0 END"
        )
    )

    with op.batch_alter_table("products") as batch_op:
        batch_op.alter_column("check", server_default=None)


def downgrade() -> None:
    with op.batch_alter_table("products") as batch_op:
        batch_op.drop_column("check")
