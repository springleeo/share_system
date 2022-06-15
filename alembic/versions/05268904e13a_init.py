"""init

Revision ID: 05268904e13a
Revises: 8994b316d7ac
Create Date: 2022-06-15 10:51:33.373934

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05268904e13a'
down_revision = '8994b316d7ac'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('permission', sa.Column('icon', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('permission', 'icon')
    # ### end Alembic commands ###