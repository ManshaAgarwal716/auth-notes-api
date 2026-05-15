from sqlmodel import SQLModel, create_engine
from src.config import set
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker
from src.users.models import User
engine=create_async_engine(set.DATABASE_URL,echo=True)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
Session=sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
async def get_session() :
    async with Session() as session:
        yield session