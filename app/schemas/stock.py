from pydantic import BaseModel
from typing import Optional

class StockOut(BaseModel):
    id: int
    symbol: str
    name: str
    sector: Optional[str] = None
    industry: Optional[str] = None
    market_cap: Optional[float] = None
    exchange: Optional[str] = None
    logo_url: Optional[str] = None

    class Config:
        from_attributes = True
        