import datetime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, String
from sqlalchemy.sql import func


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Guild(Base):
    __tablename__ = "guild"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    bot_join_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    settings = relationship("Settings", backref="guild", uselist=False)

    @property
    def guild_id(self):
        return self.id


class Settings(Base):
    """server specific settings 1-1 with guild"""

    __tablename__ = "settings"

    id: Mapped[str] = mapped_column(String, ForeignKey(Guild.id), primary_key=True)

    @property
    def guild_id(self):
        return self.id
