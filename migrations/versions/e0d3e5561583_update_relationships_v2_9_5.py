"""update relationships v2.9.5

Revision ID: e0d3e5561583
Revises: c83dfe127856
Create Date: 2020-09-12 22:02:18.929402

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0d3e5561583'
down_revision = 'c83dfe127856'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_scheduling_mtm',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('scheduling_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['scheduling_id'], ['schedulings.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'scheduling_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_scheduling_mtm')
    # ### end Alembic commands ###
