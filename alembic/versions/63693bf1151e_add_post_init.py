"""add-post-init

Revision ID: 63693bf1151e
Revises: 
Create Date: 2022-02-28 00:50:18.191646

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63693bf1151e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',
     sa.Column('id', sa.Integer(), nullable=False,primary_key=True))
    pass


def downgrade():
    op.drop_table('posts')
    pass
