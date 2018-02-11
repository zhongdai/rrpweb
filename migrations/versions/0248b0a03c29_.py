"""empty message

Revision ID: 0248b0a03c29
Revises: 
Create Date: 2018-02-11 14:52:00.719217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0248b0a03c29'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
