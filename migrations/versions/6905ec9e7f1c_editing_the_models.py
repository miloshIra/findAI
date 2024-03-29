"""editing the models

Revision ID: 6905ec9e7f1c
Revises: 0601e88d7611
Create Date: 2023-05-14 18:36:38.377040

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6905ec9e7f1c'
down_revision = '0601e88d7611'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('model_idea',
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('category', sa.String(length=32), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('ai_idea')
    op.add_column('company', sa.Column('updated_on', sa.DateTime(), nullable=True))
    op.add_column('entry', sa.Column('updated_on', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('updated_on', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('role', sa.Enum('member', 'subscriber', 'admin', name='role_types', native_enum=False), server_default='member', nullable=False))
    op.add_column('user', sa.Column('is_active', sa.Boolean(), server_default='1', nullable=False))
    op.add_column('user', sa.Column('sign_in_count', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('current_sign_in_ip', sa.String(length=45), nullable=True))
    op.add_column('user', sa.Column('last_sign_in_ip', sa.String(length=45), nullable=True))
    op.alter_column('user', 'password_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.create_index(op.f('ix_user_role'), 'user', ['role'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_role'), table_name='user')
    op.alter_column('user', 'password_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.drop_column('user', 'last_sign_in_ip')
    op.drop_column('user', 'current_sign_in_ip')
    op.drop_column('user', 'sign_in_count')
    op.drop_column('user', 'is_active')
    op.drop_column('user', 'role')
    op.drop_column('user', 'updated_on')
    op.drop_column('entry', 'updated_on')
    op.drop_column('company', 'updated_on')
    op.create_table('ai_idea',
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('user_id', postgresql.UUID(), autoincrement=False, nullable=True),
    sa.Column('category', sa.VARCHAR(length=32), autoincrement=False, nullable=True),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(length=32), autoincrement=False, nullable=True),
    sa.Column('created', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='ai_idea_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='ai_idea_pkey')
    )
    op.drop_table('model_idea')
    # ### end Alembic commands ###
