from pydantic import BaseModel
from typing import Optional, List
from app.schemas.stock import StockOut

class ScreenerFilter(BaseModel):
    sector: Optional[str] = None
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    roe: Optional[float] = None
    dividend_yield: Optional[float] = None

class ScreenerResult(BaseModel):
    total_matches: int
    stocks: List[StockOut]