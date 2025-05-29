from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Investor(Base):
    __tablename__ = "investors"

    investor_id = Column(String, primary_key=True)
    investor_name = Column(String, nullable=False, unique=True)
    investory_type = Column(String, nullable=False)
    investor_country = Column(String, nullable=False)
    investor_date_added = Column(String, nullable=False)
    investor_last_updated = Column(String, nullable=False)

class Commitment(Base):
    __tablename__ = 'commitments'

    commitment_id = Column(String, primary_key=True)
    commitment_asset_class = Column(String, nullable=False)
    commitment_currency = Column(String, nullable=False)
    commitment_amount = Column(Integer, nullable=False)
    investor_id = Column(String, ForeignKey('investors.id'), nullable=False)
