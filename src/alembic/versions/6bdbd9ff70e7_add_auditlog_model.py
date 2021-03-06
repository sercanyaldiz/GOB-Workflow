"""Add AuditLog model

Revision ID: 6bdbd9ff70e7
Revises: c1d70cbb93f4
Create Date: 2019-09-25 11:49:30.741402

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bdbd9ff70e7'
down_revision = 'c1d70cbb93f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('audit_logs',
    sa.Column('logid', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('source', sa.String(), nullable=True),
    sa.Column('destination', sa.String(), nullable=True),
    sa.Column('data', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('logid')
    )
    op.create_index(op.f('ix_audit_logs_logid'), 'audit_logs', ['logid'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_audit_logs_logid'), table_name='audit_logs')
    op.drop_table('audit_logs')
    # ### end Alembic commands ###
