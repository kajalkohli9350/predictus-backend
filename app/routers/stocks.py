from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db, redis_client
from app.schemas.stock import StockOut
from app.services.stock_service import get_all_stocks, get_stock_by_id
from typing import List
import json

router = APIRouter(prefix="/stocks", tags=["Stocks"])

@router.get("/")
def get_stocks(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    cache_key = f"stocks:page={page}:page_size={page_size}"

    # Step 1: Check karo Redis mein already cached hai kya
    cached_result = redis_client.get(cache_key)
    if cached_result:
        return json.loads(cached_result)

    # Step 2: Agar nahi mila, database se lao
    skip = (page - 1) * page_size
    stocks, total = get_all_stocks(db, skip=skip, limit=page_size)

    result = {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
        "data": [
            {
                "id": s.id,
                "symbol": s.symbol,
                "name": s.name,
                "sector": s.sector,
                "industry": s.industry,
                "market_cap": s.market_cap,
                "exchange": s.exchange,
                "logo_url": s.logo_url,
            }
            for s in stocks
        ],
    }

    # Step 3: Redis mein save karo, 5 minute (300 sec) ke liye
    redis_client.setex(cache_key, 300, json.dumps(result))

    return result

@router.get("/{stock_id}", response_model=StockOut)
def get_stock(stock_id: int, db: Session = Depends(get_db)):
    return get_stock_by_id(db, stock_id)