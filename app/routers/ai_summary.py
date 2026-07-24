from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.stock_service import get_stock_by_symbol
from app.services.fundamentals_service import get_fundamentals_by_stock_id
from app.services.ai_summary_service import generate_stock_summary, generate_price_and_news

router = APIRouter(prefix="/ai-summary", tags=["AI Summary"])

@router.get("/{symbol}")
def get_ai_summary(symbol: str, db: Session = Depends(get_db)):
    stock = get_stock_by_symbol(db, symbol)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    fundamentals = get_fundamentals_by_stock_id(db, stock.id)
    summary = generate_stock_summary(stock, fundamentals)

    return {"symbol": symbol, "summary": summary}

@router.get("/{symbol}/news")
def get_stock_news(symbol: str, db: Session = Depends(get_db)):
    stock = get_stock_by_symbol(db, symbol)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    news = generate_price_and_news(stock)
    return {"symbol": symbol, "news": news}