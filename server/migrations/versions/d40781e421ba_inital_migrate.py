"""inital migrate

Revision ID: d40781e421ba
Revises: 
Create Date: 2024-01-29 20:44:43.183426

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.types import Text


# revision identifiers, used by Alembic.
revision = 'd40781e421ba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('username', sa.String(), nullable=True),
                    sa.Column('password', sa.String(), nullable=True),
                    sa.Column('first_year', sa.DateTime(), server_default=sa.text(
                        '(CURRENT_TIMESTAMP)'), nullable=True),
                    sa.PrimaryKeyConstraint('user_id')
                    )
    op.create_table('user_games',
                    sa.Column('gamePk', sa.Integer(), nullable=False),
                    sa.Column('user_ids', postgresql.JSON(
                        astext_type=Text()), nullable=False),
                    sa.Column('game_data', postgresql.JSON(
                        astext_type=Text()), nullable=True),
                    sa.ForeignKeyConstraint(['user_ids'], ['users.user_id'], ),
                    sa.PrimaryKeyConstraint('gamePk')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_games')
    op.drop_table('users')
    # ### end Alembic commands ###
