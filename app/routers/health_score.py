from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.fundamentals import StockFundamentals
from app.models.health_score import FinancialHealthScore
from app.services.health_score import calculate_composite_score

router = APIRouter(prefix="/health-score", tags=["Health Score"])

@router.post("/{stock_id}/compute")
def compute_health_score(stock_id: int, db: Session = Depends(get_db)):
    fundamentals = db.query(StockFundamentals).filter(
        StockFundamentals.stock_id == stock_id
    ).order_by(StockFundamentals.id.desc()).first()

    if not fundamentals:
        raise HTTPException(status_code=404, detail="No fundamentals found for this stock")

    scores = calculate_composite_score(fundamentals)

    health_score = FinancialHealthScore(stock_id=stock_id, **scores)
    db.add(health_score)
    db.commit()
    db.refresh(health_score)

    return {
        "stock_id": stock_id,
        "liquidity_score": health_score.liquidity_score,
        "solvency_score": health_score.solvency_score,
        "profitability_score": health_score.profitability_score,
        "leverage_score": health_score.leverage_score,
        "composite_score": health_score.composite_score,
    }