from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from utils import MetaSingleton


# Useful discussion on setting up sqlalchemy, and discord bot db structure
# https://discord.com/channels/336642139381301249/1223723644933505044


class DatabaseSingleton(metaclass=MetaSingleton):
    def __init__(self, db_url):
        self.dburl = db_url
        self.engine = None
        self.base = declarative_base(name="Defined Base.")
        self.session = None

    async def init_db(self):
        self.engine = create_async_engine(self.dburl, echo=True)
        async with self.engine.begin() as conn:
            await conn.run_sync(self.base.metadata.create_all)

    async def close_async(self):
        # Use me on shutdown!
        await self.engine.dispose()

    def create_session(self):
        session_maker = async_sessionmaker(bind=self.engine, expire_on_commit=False)
        return session_maker()
