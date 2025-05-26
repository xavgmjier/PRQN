from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql.expression import null
from .database import Base

class Investor(Base):
    __tablename__ = "investors"

    investor_id = Column(String, primaryKey=True)
    investor_name = Column(String, nullable=False, unique=True)
    fund_type = Column(String, nullable=False)
    investor_country = Column(String, nullable=False)
    investor_date_added = Column(String, nullable=False)
    investor_last_updated = Column(String, nullable=False)

