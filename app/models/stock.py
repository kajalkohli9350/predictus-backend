from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    sector = Column(String, index=True)
    industry = Column(String)
    market_cap = Column(Float)
    exchange = Column(String)
    logo_url = Column(String, nullable=True)