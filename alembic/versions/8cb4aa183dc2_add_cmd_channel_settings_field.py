"""Add cmd_channel Settings field

Revision ID: 8cb4aa183dc2
Revises: c849245b8eb1
Create Date: 2024-06-24 14:22:10.757904

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8cb4aa183dc2"
down_revision: Union[str, None] = "c849245b8eb1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("settings", sa.Column("cmd_channel", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("settings", "cmd_channel")
    # ### end Alembic commands ###