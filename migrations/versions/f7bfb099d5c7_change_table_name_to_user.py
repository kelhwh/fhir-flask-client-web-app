"""change table name to user

Revision ID: f7bfb099d5c7
Revises: a469060ab2e5
Create Date: 2021-01-04 23:48:26.639865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7bfb099d5c7'
down_revision = 'a469060ab2e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('given_name', sa.String(length=64), nullable=True),
    sa.Column('family_name', sa.String(length=64), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('identifier_system', sa.String(), nullable=True),
    sa.Column('identifier_value', sa.String(length=64), nullable=True),
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('given_name', sa.VARCHAR(length=64), nullable=True),
    sa.Column('family_name', sa.VARCHAR(length=64), nullable=True),
    sa.Column('date_of_birth', sa.DATE(), nullable=True),
    sa.Column('identifier_sysyem', sa.VARCHAR(), nullable=True),
    sa.Column('identifier_value', sa.VARCHAR(length=64), nullable=True),
    sa.Column('patient_id', sa.INTEGER(), nullable=True),
    sa.Column('email', sa.VARCHAR(length=64), nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=256), nullable=True),
    sa.Column('identifier_system', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=1)
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
