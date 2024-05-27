"""Initial

Revision ID: e1bbf7a86e1f
Revises: 7d528ce8788c
Create Date: 2024-05-03 15:18:35.808246

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'e1bbf7a86e1f'
down_revision: Union[str, None] = '7d528ce8788c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('image_src', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.drop_column('user', 'imagePath')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('imagePath', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('user', 'image_src')
    # ### end Alembic commands ###
