from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.fundamentals import StockFundamentals
from app.schemas.fundamentals import FundamentalsOut
from typing import List

router = APIRouter(prefix="/fundamentals", tags=["Fundamentals"])

@router.get("/{stock_id}", response_model=List[FundamentalsOut])
def get_fundamentals(stock_id: int, db: Session = Depends(get_db)):
    results = db.query(StockFundamentals).filter(StockFundamentals.stock_id == stock_id).all()
    return results