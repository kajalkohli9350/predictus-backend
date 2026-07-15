from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.health_score import compute_and_save_health_score

router = APIRouter(prefix="/health-score", tags=["Health Score"])

@router.post("/{stock_id}/compute")
def compute_health_score(stock_id: int, db: Session = Depends(get_db)):
    result = compute_and_save_health_score(db, stock_id)
    if not result:
        raise HTTPException(status_code=404, detail="No fundamentals found for this stock")

    return {
        "stock_id": stock_id,
        "liquidity_score": result.liquidity_score,
        "solvency_score": result.solvency_score,
        "profitability_score": result.profitability_score,
        "leverage_score": result.leverage_score,
        "composite_score": result.composite_score,
    }