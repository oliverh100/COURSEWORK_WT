"""empty message

Revision ID: ea3c9e24794b
Revises: 
Create Date: 2020-11-22 15:54:05.480449

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea3c9e24794b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('room',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('r_name', sa.String(length=64), nullable=True),
    sa.Column('building', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teacher',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('f_name', sa.String(length=64), nullable=True),
    sa.Column('s_name', sa.String(length=64), nullable=True),
    sa.Column('initials', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('activity',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('a_name', sa.String(length=64), nullable=True),
    sa.Column('r_id', sa.Integer(), nullable=True),
    sa.Column('date_time', sa.String(length=64), nullable=True),
    sa.Column('max_attendees', sa.String(length=64), nullable=True),
    sa.Column('food_supplied', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['r_id'], ['room.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teacher_activity_link',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('a_id', sa.Integer(), nullable=True),
    sa.Column('t_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['a_id'], ['activity.id'], ),
    sa.ForeignKeyConstraint(['t_id'], ['teacher.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('teacher_activity_link')
    op.drop_table('activity')
    op.drop_table('user')
    op.drop_table('teacher')
    op.drop_table('room')
    # ### end Alembic commands ###
