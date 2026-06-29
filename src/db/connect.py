from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from src.config import settings


DB_URL = settings.pg_dsn.encoded_string()

engine = create_async_engine(
    DB_URL,                     # type: ignore
    echo=True,
) 

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    async with SessionLocal() as session:
        yield session

