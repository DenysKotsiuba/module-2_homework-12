"""add user_id ForeignKey to contact

Revision ID: 276f04c64cff
Revises: 58aec2851445
Create Date: 2023-07-07 16:32:24.481510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '276f04c64cff'
down_revision = '58aec2851445'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Contacts', sa.Column('user_id', sa.Integer(), server_default=sa.text('4'), nullable=False))
    op.create_foreign_key(None, 'Contacts', 'Users', ['user_id'], ['id'], ondelete='CASCADE')
    op.alter_column('Users', 'username',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('Users', 'password',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Users', 'password',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('Users', 'username',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.drop_constraint(None, 'Contacts', type_='foreignkey')
    op.drop_column('Contacts', 'user_id')
    # ### end Alembic commands ###