from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class StockFundamentals(Base):
    __tablename__ = "stock_fundamentals"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    period = Column(String, nullable=False)  # e.g. "Q1-2026", "FY2025"

    revenue = Column(Float)
    net_income = Column(Float)
    eps = Column(Float)
    pe_ratio = Column(Float)
    pb_ratio = Column(Float)
    debt_to_equity = Column(Float)
    roe = Column(Float)
    roa = Column(Float)
    dividend_yield = Column(Float)
    current_ratio = Column(Float)

    stock = relationship("Stock", backref="fundamentals")