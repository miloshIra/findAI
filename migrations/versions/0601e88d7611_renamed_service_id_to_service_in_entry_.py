"""renamed service_id to service in Entry model

Revision ID: 0601e88d7611
Revises: ab5c6a90adcd
Create Date: 2023-03-28 16:14:23.194171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0601e88d7611'
down_revision = 'ab5c6a90adcd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('entry', sa.Column('service', sa.String(length=32), nullable=True))
    op.drop_index('ix_entry_service_id', table_name='entry')
    op.create_index(op.f('ix_entry_service'), 'entry', ['service'], unique=False)
    op.drop_column('entry', 'service_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('entry', sa.Column('service_id', sa.VARCHAR(length=32), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_entry_service'), table_name='entry')
    op.create_index('ix_entry_service_id', 'entry', ['service_id'], unique=False)
    op.drop_column('entry', 'service')
    # ### end Alembic commands ###
