"""empty message

Revision ID: 544cbd9383f6
Revises: 04f28ea26ed5
Create Date: 2021-07-10 17:27:51.461946

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '544cbd9383f6'
down_revision = '04f28ea26ed5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('characters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('diameter', sa.Integer(), nullable=True),
    sa.Column('rotation_planet', sa.Integer(), nullable=True),
    sa.Column('orbital_period', sa.Integer(), nullable=True),
    sa.Column('gravity', sa.Integer(), nullable=True),
    sa.Column('population', sa.Integer(), nullable=True),
    sa.Column('climate', sa.String(length=45), nullable=True),
    sa.Column('terrain', sa.String(length=45), nullable=True),
    sa.Column('surface_water', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=250), nullable=True),
    sa.Column('url', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('diameter', sa.Integer(), nullable=True),
    sa.Column('rotation_planet', sa.Integer(), nullable=True),
    sa.Column('orbital_period', sa.Integer(), nullable=True),
    sa.Column('gravity', sa.Integer(), nullable=True),
    sa.Column('population', sa.Integer(), nullable=True),
    sa.Column('climate', sa.String(length=45), nullable=True),
    sa.Column('terrain', sa.String(length=45), nullable=True),
    sa.Column('surface_water', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=250), nullable=True),
    sa.Column('url', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('planet')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planet',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('diameter', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('rotation_planet', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('orbital_period', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('gravity', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('population', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('climate', mysql.VARCHAR(length=45), nullable=True),
    sa.Column('terrain', mysql.VARCHAR(length=45), nullable=True),
    sa.Column('surface_water', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created', mysql.DATETIME(), nullable=True),
    sa.Column('name', mysql.VARCHAR(length=250), nullable=True),
    sa.Column('url', mysql.VARCHAR(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('planets')
    op.drop_table('characters')
    # ### end Alembic commands ###
