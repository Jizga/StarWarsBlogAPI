"""empty message

Revision ID: 3ec66e73b46f
Revises: 0dad482280ab
Create Date: 2021-07-10 17:04:01.653956

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3ec66e73b46f'
down_revision = '0dad482280ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_ibfk_1', 'user', type_='foreignkey')
    op.drop_constraint('user_ibfk_2', 'user', type_='foreignkey')
    op.drop_column('user', 'favorite_characters')
    op.drop_column('user', 'favorite_planets')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('favorite_planets', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('favorite_characters', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('user_ibfk_2', 'user', 'favoritePlanets', ['favorite_planets'], ['id'])
    op.create_foreign_key('user_ibfk_1', 'user', 'favoriteCharacters', ['favorite_characters'], ['id'])
    # ### end Alembic commands ###
