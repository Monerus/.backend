from core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session
from asyncio import current_task

class DatabaseHelper():
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(url=url, echo=False)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False
        )
    
    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task
        )
        return session
    
    async def session_dependency(self):
        async with self.session_factory() as session:
            yield session
            await session.close()
            
    async def scoped_session_dependency(self):
        session = self.get_scoped_session()
        yield session
        await session.close()
            
db_helper = DatabaseHelper(url=settings.db_url)