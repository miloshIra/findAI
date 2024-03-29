"""empty message

Revision ID: 9f1ef09d46bc
Revises: 9928d08b53ca
Create Date: 2023-03-02 23:10:56.514879

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9f1ef09d46bc'
down_revision = '9928d08b53ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('company', sa.String(length=128), nullable=True))
    op.add_column('user', sa.Column('services', postgresql.ARRAY(sa.String(length=256)), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'services')
    op.drop_column('user', 'company')
    # ### end Alembic commands ###
