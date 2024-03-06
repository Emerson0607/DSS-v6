"""int to string

Revision ID: 5fd00ffeedc3
Revises: 61fdd7b94e01
Create Date: 2024-03-06 22:13:16.560182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5fd00ffeedc3'
down_revision = '61fdd7b94e01'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('mobile_number',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=100),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('mobile_number',
               existing_type=sa.String(length=100),
               type_=sa.INTEGER(),
               existing_nullable=True)

    # ### end Alembic commands ###
