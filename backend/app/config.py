from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

#config database: "postgresql+asyncpg://user:password@host:port/database"
DB_CONFIG = f"postgresql+asyncpg://postgres:1234567890@localhost:5432/test"


SECRET_KEY = "3DmedVN23"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ACCESS_TOKEN_EXPIRE_DAYS = 7
ACCESS_TOKEN_EXPIRE_YEARS = 1

#CHOICE: MINUTES, DAYS, YEARS, NONE = NEVER EXPIRE
ACCESS_TOKEN_EXPIRE_TYPE = "DAYS"

class AsyncDatabaseSession:

    def __init__(self) -> None:
        self.session = None
        self.engine = None

    def __getattr__(self,name):
        return getattr(self.session,name)

    def init(self):
        self.engine = create_async_engine(DB_CONFIG,future=True, echo=True)
        self.session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)()

    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)


db = AsyncDatabaseSession()

async def commit_rollback():
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    