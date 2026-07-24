from sqlalchemy.orm import Session
from app.models.health_score import FinancialHealthScore
from app.services.fundamentals_service import get_latest_fundamentals


def calculate_liquidity_score(current_ratio: float) -> float:
    if current_ratio is None:
        return 50.0
    # Ideal current ratio ~2.0. Scale 0-100 around that.
    score = (current_ratio / 2.0) * 100
    return max(0, min(100, score))

def calculate_solvency_score(debt_to_equity: float) -> float:
    if debt_to_equity is None:
        return 50.0
    # Lower debt-to-equity = better. 0 D/E = 100 score, 2.0+ D/E = 0 score
    score = 100 - (debt_to_equity / 2.0) * 100
    return max(0, min(100, score))

def calculate_profitability_score(roe: float, roa: float) -> float:
    if roe is None or roa is None:
        return 50.0
    # ROE up to 30% = full score contribution, ROA up to 20% = full score
    roe_score = max(0,min(100, (roe / 30.0) * 100))
    roa_score = max(0, min(100, (roa / 20.0) * 100))
    return (roe_score + roa_score) / 2

def calculate_leverage_score(dividend_yield: float) -> float:
    # Simplified for MVP — using dividend yield as a stability proxy.
    if dividend_yield is None:
        return 50.0
    score = (dividend_yield / 4.0) * 100
    return max(0, min(100, score))

def calculate_composite_score(fundamentals) -> dict:
    liquidity = calculate_liquidity_score(fundamentals.current_ratio)
    solvency = calculate_solvency_score(fundamentals.debt_to_equity)
    profitability = calculate_profitability_score(fundamentals.roe, fundamentals.roa)
    leverage = calculate_leverage_score(fundamentals.dividend_yield)

    composite = (liquidity + solvency + profitability + leverage) / 4

    return {
        "liquidity_score": round(liquidity, 2),
        "solvency_score": round(solvency, 2),
        "profitability_score": round(profitability, 2),
        "leverage_score": round(leverage, 2),
        "composite_score": round(composite, 2),
    }

def compute_and_save_health_score(db: Session, stock_id: int):
    fundamentals = get_latest_fundamentals(db, stock_id)
    if not fundamentals:
        return None

    scores = calculate_composite_score(fundamentals)

    health_score = FinancialHealthScore(stock_id=stock_id, **scores)
    db.add(health_score)
    db.commit()
    db.refresh(health_score)

    return health_score

def get_or_compute_health_score(db: Session, stock_id: int):
    existing = (
        db.query(FinancialHealthScore)
        .filter(FinancialHealthScore.stock_id == stock_id)
        .order_by(FinancialHealthScore.id.desc())
        .first()
    )
    if existing:
        return existing
    return compute_and_save_health_score(db, stock_id)    