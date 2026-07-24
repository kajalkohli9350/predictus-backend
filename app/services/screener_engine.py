from sqlalchemy.orm import Session
from app.models.stock import Stock
from app.models.fundamentals import StockFundamentals
from app.schemas.screener import ScreenerFilter

def screener_engine(db: Session, filters: ScreenerFilter):
    query = db.query(Stock).join(StockFundamentals, Stock.id == StockFundamentals.stock_id)

    if filters.sector:
        query = query.filter(Stock.sector == filters.sector)

    if filters.market_cap is not None:
        query = query.filter(Stock.market_cap >= filters.market_cap)

    if filters.pe_ratio is not None:
        query = query.filter(StockFundamentals.pe_ratio <= filters.pe_ratio)

    if filters.roe is not None:
        query = query.filter(StockFundamentals.roe >= filters.roe)

    if filters.dividend_yield is not None:
        query = query.filter(StockFundamentals.dividend_yield >= filters.dividend_yield)

    query = query.distinct()
    return query.all()