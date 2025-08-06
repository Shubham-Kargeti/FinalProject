from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQL_ALCHEMY_DB_URL= "postgresql://postgres:G%40dfwnjq787724%21@localhost:5432/Final_ProjectDB"

engine= create_engine(SQL_ALCHEMY_DB_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit= False)

Base= declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()