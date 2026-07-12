from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base

class FinancialHealthScore(Base):
    __tablename__ = "financial_health_scores"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)

    liquidity_score = Column(Float)
    solvency_score = Column(Float)
    profitability_score = Column(Float)
    leverage_score = Column(Float)
    composite_score = Column(Float)

    computed_at = Column(DateTime(timezone=True), server_default=func.now())