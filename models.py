import datetime
from typing import List
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import (
    ForeignKey,
    DateTime,
    SmallInteger,
    CheckConstraint,
    select,
    text,
)
from sqlalchemy.sql import func


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Guild(Base):
    __tablename__ = "guild"

    id: Mapped[str] = mapped_column(primary_key=True)
    bot_join_date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    settings: Mapped["Settings"] = relationship(back_populates="guild")
    gamble_data: Mapped[List["GambleData"]] = relationship()

    @property
    def guild_id(self):
        return self.id


class Settings(Base):
    """server specific settings 1-1 with guild"""

    __tablename__ = "settings"

    id: Mapped[str] = mapped_column(ForeignKey(Guild.id), primary_key=True)
    guild: Mapped["Guild"] = relationship(back_populates="settings")

    gamble_starting_funds: Mapped[int] = mapped_column(
        CheckConstraint("gamble_starting_funds > 0"), server_default=text("1000")
    )
    gamble_bankrupt_cooldown: Mapped[int] = mapped_column(
        CheckConstraint("gamble_bankrupt_cooldown > 0"),
        nullable=True,
        server_default=None,
    )  # in seconds
    gamble_win_chance: Mapped[int] = mapped_column(
        SmallInteger,
        CheckConstraint("gamble_win_chance >= 0 AND gamble_win_chance <= 100"),
        server_default=text("40"),
    )  # 1 to 100 (skip % sign when adding value)

    @property
    def guild_id(self):
        return self.id


class GambleData(Base):
    """/gamble data"""

    __tablename__ = "gamble_data"

    user_id: Mapped[str] = mapped_column(primary_key=True)
    guild: Mapped[str] = mapped_column(ForeignKey(Guild.id))

    funds: Mapped[int] = mapped_column(CheckConstraint("funds >= 0"), default=1000)
    last_gamble: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=None, nullable=True
    )
    bankrupcy_cooldown_until: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=None, nullable=True
    )

    @property
    def id(self):
        return self.user_id

    def set_bankrupcy_cooldown_until(self, session: AsyncSession):
        gamble_bankrupt_cooldown = (
            select(Settings.gamble_win_chance)
            .select_from(Settings)
            .where(id=self.guild_id)
        )
        if not gamble_bankrupt_cooldown:
            return False
        self.bankrupcy_cooldown_until = datetime.datetime().now() + datetime.timedelta(
            seconds=gamble_bankrupt_cooldown
        )
        session.commit()
        return True
