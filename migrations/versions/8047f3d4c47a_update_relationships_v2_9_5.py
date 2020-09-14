"""update relationships v2.9.5

Revision ID: 8047f3d4c47a
Revises: 3bc2b2972514
Create Date: 2020-09-12 22:16:19.923627

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8047f3d4c47a'
down_revision = 'c83dfe127856'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('schedulings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('confirmation', sa.Boolean(), nullable=True),
    sa.Column('lesson_time', sa.DateTime(), nullable=True),
    sa.Column('subject', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['subject'], ['subjects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
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
    op.drop_table('schedulings')
    # ### end Alembic commands ###
