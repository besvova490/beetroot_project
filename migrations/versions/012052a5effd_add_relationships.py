"""add relationships

Revision ID: 012052a5effd
Revises: 7205c2e664a1
Create Date: 2020-09-06 22:46:08.655584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '012052a5effd'
down_revision = '7205c2e664a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('association_users',
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['users.id'], )
    )
    op.create_table('subjects_mtm',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('subjects_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['subjects_id'], ['subjects.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'subjects_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subjects_mtm')
    op.drop_table('association_users')
    # ### end Alembic commands ###