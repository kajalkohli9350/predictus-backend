from pydantic import BaseModel
from typing import Optional

class FundamentalsOut(BaseModel):
    id: int
    stock_id: int
    period: str
    revenue: Optional[float] = None
    net_income: Optional[float] = None
    eps: Optional[float] = None
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    debt_to_equity: Optional[float] = None
    roe: Optional[float] = None
    roa: Optional[float] = None
    dividend_yield: Optional[float] = None
    current_ratio: Optional[float] = None

    class Config:
        from_attributes = True