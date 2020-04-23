"""Initilize the database and prepare the data

Revision ID: 00000001
Revises: None
Create Date: 2020-04-23 19:48:48.084856

"""

# revision identifiers, used by Alembic.
revision = '00000001'
down_revision = None

from smorest_sfs.extensions import db
from migrations import initial_data

def upgrade():
    db.create_all()
    initial_data.init_permission()
    initial_data.init_email_templates()


def downgrade():
    db.drop_all()
