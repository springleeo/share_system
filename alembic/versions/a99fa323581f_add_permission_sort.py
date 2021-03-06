"""add permission sort 

Revision ID: a99fa323581f
Revises: f1d4ee6c4b55
Create Date: 2022-06-12 21:26:49.541956

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a99fa323581f'
down_revision = 'f1d4ee6c4b55'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_index('name', table_name='department')
    op.drop_table('department')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('department',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('leader', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('desc', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('create_time', mysql.DATETIME(), nullable=True),
    sa.Column('create_date', sa.DATE(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_index('name', 'department', ['name'], unique=False)
    op.create_table('user',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('pwd', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('dep_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('avatar', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('addr', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('state', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('last_login_date', sa.DATE(), nullable=True),
    sa.Column('ip', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('create_time', mysql.DATETIME(), nullable=True),
    sa.Column('create_date', sa.DATE(), nullable=True),
    sa.ForeignKeyConstraint(['dep_id'], ['department.id'], name='user_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
