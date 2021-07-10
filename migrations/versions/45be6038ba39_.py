"""empty message

Revision ID: 45be6038ba39
Revises: a817a152251e
Create Date: 2021-07-10 14:16:22.578097

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '45be6038ba39'
down_revision = 'a817a152251e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'last_name',
               existing_type=mysql.VARCHAR(length=250),
               nullable=False)
    op.drop_index('id', table_name='user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('id', 'user', ['id'], unique=False)
    op.alter_column('user', 'last_name',
               existing_type=mysql.VARCHAR(length=250),
               nullable=True)
    # ### end Alembic commands ###
