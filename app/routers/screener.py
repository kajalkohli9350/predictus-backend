from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.screener import ScreenerFilter, ScreenerResult
from app.services.screener_engine import screener_engine

router = APIRouter(prefix="/screener", tags=["Screener"])

@router.post("/run", response_model=ScreenerResult)
def run_stock_screener(filters: ScreenerFilter, db: Session = Depends(get_db)):
    results = screener_engine(db, filters)
    return {
        "total_matches": len(results),
        "stocks": results,
    }