"""empty message

Revision ID: c105bfcd6e51
Revises: 0681866638cf
Create Date: 2020-03-27 16:08:11.934275

"""

# revision identifiers, used by Alembic.
revision = "c105bfcd6e51"
down_revision = "0681866638cf"

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users", "email", existing_type=sa.VARCHAR(length=255), nullable=True
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users", "email", existing_type=sa.VARCHAR(length=255), nullable=False
    )
    # ### end Alembic commands ###