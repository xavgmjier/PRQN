from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./InvestorCommitments.db"

# check-same-thread is false beacuse we're using a SQLite database

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check-same-thread": False}) 

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()
