from fastapi import HTTPException , status
from sqlalchemy.orm import Session
from app.models.stock import Stock

def get_all_stocks(db: Session, skip: int = 0, limit: int = 10):
    total = db.query(Stock).count()
    stocks = db.query(Stock).offset(skip).limit(limit).all()
    return stocks, total

def get_stock_by_id(db: Session, stock_id: int):
    stock = (db.query(Stock).filter(Stock.id == stock_id).first())
    if stock is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,detail =f"stock with ID {stock_id} not found",
        )
    return stock