"""Remove bot channel row, add GambleData table

Revision ID: 02e96b27ab7c
Revises: 8cb4aa183dc2
Create Date: 2024-06-26 16:25:03.586979

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "02e96b27ab7c"
down_revision: Union[str, None] = "8cb4aa183dc2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "gamble_data",
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("guild_id", sa.String(), nullable=False),
        sa.Column("funds", sa.Integer(), nullable=False),
        sa.Column("last_gamble", sa.DateTime(), nullable=True),
        sa.Column("bankrupcy_cooldown_until", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["guild_id"],
            ["guild.id"],
        ),
        sa.PrimaryKeyConstraint("user_id"),
    )
    op.add_column(
        "settings",
        sa.Column(
            "gamble_starting_funds",
            sa.Integer(),
            server_default=sa.text("1000"),
            nullable=False,
        ),
    )
    op.add_column(
        "settings", sa.Column("gamble_bankrupt_cooldown", sa.Integer(), nullable=True)
    )
    op.add_column(
        "settings",
        sa.Column(
            "gamble_win_chance",
            sa.SmallInteger(),
            server_default=sa.text("40"),
            nullable=False,
        ),
    )
    op.drop_column("settings", "cmd_channel")

    # alembic autogeneration of constraints below is not supported, needed to be added manually
    op.execute(
        "ALTER TABLE settings ADD CONSTRAINT check_starting_funds_positive CHECK(gamble_starting_funds > 0);"
    )
    op.execute(
        "ALTER TABLE settings ADD CONSTRAINT check_cooldown_positive CHECK(gamble_bankrupt_cooldown > 0);"
    )
    op.execute(
        "ALTER TABLE settings ADD CONSTRAINT chance_between_0_and_100 CHECK(gamble_win_chance >= 0 AND gamble_win_chance <= 100);"
    )

    op.execute(
        "ALTER TABLE gamble_data ADD CONSTRAINT check_funds_positive CHECK(funds >= 0);"
    )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "settings",
        sa.Column("cmd_channel", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.drop_column("settings", "gamble_win_chance")
    op.drop_column("settings", "gamble_bankrupt_cooldown")
    op.drop_column("settings", "gamble_starting_funds")
    op.drop_table("gamble_data")
    # ### end Alembic commands ###
