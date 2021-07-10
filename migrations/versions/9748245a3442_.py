"""empty message

Revision ID: 9748245a3442
Revises: d028dea4afc8
Create Date: 2021-07-10 17:44:43.538672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9748245a3442'
down_revision = 'd028dea4afc8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('favoriteCharacters', sa.Column('user_id', sa.Integer(), nullable=True))
    op.add_column('favoriteCharacters', sa.Column('character_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'favoriteCharacters', 'user', ['user_id'], ['id'])
    op.create_foreign_key(None, 'favoriteCharacters', 'characters', ['character_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'favoriteCharacters', type_='foreignkey')
    op.drop_constraint(None, 'favoriteCharacters', type_='foreignkey')
    op.drop_column('favoriteCharacters', 'character_id')
    op.drop_column('favoriteCharacters', 'user_id')
    # ### end Alembic commands ###