from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.stock import Stock
from app.schemas.stock import StockOut
from typing import List

router = APIRouter(prefix="/stocks", tags=["Stocks"])

@router.get("/", response_model=List[StockOut])
def get_stocks(db: Session = Depends(get_db)):
    stocks = db.query(Stock).all()
    return stocks

@router.get("/{stock_id}", response_model=StockOut)
def get_stock(stock_id: int, db: Session = Depends(get_db)):
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    return stock
