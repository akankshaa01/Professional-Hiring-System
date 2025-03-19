"""adding extra details to client and pro tables

Revision ID: 80fd1f91850f
Revises: b26b3db4611f
Create Date: 2024-11-08 17:10:26.387253

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80fd1f91850f'
down_revision = 'b26b3db4611f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bookings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('message', sa.Text(), nullable=True))

    with op.batch_alter_table('client_profile', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_of_birth', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('gender', sa.String(length=10), nullable=True))

    with op.batch_alter_table('professional_profile', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_of_birth', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('gender', sa.String(length=10), nullable=True))
        batch_op.add_column(sa.Column('availability_status', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('professional_profile', schema=None) as batch_op:
        batch_op.drop_column('availability_status')
        batch_op.drop_column('gender')
        batch_op.drop_column('date_of_birth')

    with op.batch_alter_table('client_profile', schema=None) as batch_op:
        batch_op.drop_column('gender')
        batch_op.drop_column('date_of_birth')

    with op.batch_alter_table('bookings', schema=None) as batch_op:
        batch_op.drop_column('message')

    # ### end Alembic commands ###
