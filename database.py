from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncEngine
from typing import AsyncGenerator

# Use asyncpg driver for PostgreSQL
SQL_ALCHEMY_DB_URL = "postgresql+asyncpg://postgres:G%40dfwnjq787724%21@localhost:5432/Final_ProjectDB"

# Async engine
engine: AsyncEngine = create_async_engine(SQL_ALCHEMY_DB_URL, echo=True)

# Async session maker
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

# Declarative Base
Base = declarative_base()

# Dependency to get DB session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker


# SQL_ALCHEMY_DB_URL= "postgresql://postgres:G%40dfwnjq787724%21@localhost:5432/Final_ProjectDB"

# engine= create_engine(SQL_ALCHEMY_DB_URL)

# SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit= False)

# Base= declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()