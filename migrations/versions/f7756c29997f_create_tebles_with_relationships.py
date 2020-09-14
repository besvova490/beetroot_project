"""create tebles with relationships

Revision ID: f7756c29997f
Revises: 
Create Date: 2020-09-14 23:04:27.920075

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7756c29997f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subjects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('telegram_id', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('is_teacher', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('association_users_roles',
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['users.id'], )
    )
    op.create_table('schedulings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('confirmation', sa.Boolean(), nullable=True),
    sa.Column('lesson_time', sa.DateTime(), nullable=True),
    sa.Column('subject_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subjects_mtm',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('subjects_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['subjects_id'], ['subjects.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'subjects_id')
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
    op.drop_table('subjects_mtm')
    op.drop_table('schedulings')
    op.drop_table('association_users_roles')
    op.drop_table('users')
    op.drop_table('subjects')
    # ### end Alembic commands ###