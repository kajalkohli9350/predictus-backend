from sqlalchemy.orm import Session
from app.models.fundamentals import StockFundamentals

def get_fundamentals_by_stock_id(db: Session, stock_id: int):
    return db.query(StockFundamentals).filter(
        StockFundamentals.stock_id == stock_id
    ).all()

def get_latest_fundamentals(db: Session, stock_id: int):
    return db.query(StockFundamentals).filter(
        StockFundamentals.stock_id == stock_id
    ).order_by(StockFundamentals.id.desc()).first()