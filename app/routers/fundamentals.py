from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.fundamentals import FundamentalsOut
from app.services.fundamentals_service import get_fundamentals_by_stock_id
from app.services.stock_service import get_stock_by_symbol
from typing import List



router = APIRouter(prefix="/fundamentals", tags=["Fundamentals"])

@router.get("/{stock_id}", response_model=List[FundamentalsOut])
def get_fundamentals(stock_id: int, db: Session = Depends(get_db)):
    return get_fundamentals_by_stock_id(db, stock_id)

@router.get("/symbol/{symbol}", response_model=List[FundamentalsOut])
def get_fundamentals_by_symbol(symbol: str, db: Session = Depends(get_db)):
    stock = get_stock_by_symbol(db, symbol)
    if not stock:
        return []
    return get_fundamentals_by_stock_id(db, stock.id)