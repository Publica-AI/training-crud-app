"""alter user table

Revision ID: 180d36c9b537
Revises: 
Create Date: 2025-10-23 11:18:12.463535

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '180d36c9b537'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    ALTER TABLE users
    ADD COLUMN userType varchar(100) DEFAULT 'student' ENUM('student',  'admin')
""")
    pass


def downgrade() -> None:
    op.execute("""
    ALTER TABLE users
    DROP COLUMN userType
""")
    pass
