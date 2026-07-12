import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.database import SessionLocal
from app.models.stock import Stock
from app.models.fundamentals import StockFundamentals

def seed_fundamentals():
    db = SessionLocal()

    with open(os.path.join(os.path.dirname(__file__), "seed_fundamentals.json")) as f:
        data = json.load(f)

    for item in data:
        stock = db.query(Stock).filter(Stock.symbol == item["stock_symbol"]).first()
        if not stock:
            print(f"Skipping {item['stock_symbol']} — stock not found")
            continue

        existing = db.query(StockFundamentals).filter(
            StockFundamentals.stock_id == stock.id,
            StockFundamentals.period == item["period"]
        ).first()
        if existing:
            print(f"Skipping {item['stock_symbol']} {item['period']} — already exists")
            continue

        fundamentals = StockFundamentals(
            stock_id=stock.id,
            period=item["period"],
            revenue=item["revenue"],
            net_income=item["net_income"],
            eps=item["eps"],
            pe_ratio=item["pe_ratio"],
            pb_ratio=item["pb_ratio"],
            debt_to_equity=item["debt_to_equity"],
            roe=item["roe"],
            roa=item["roa"],
            dividend_yield=item["dividend_yield"],
            current_ratio=item["current_ratio"],
        )
        db.add(fundamentals)

    db.commit()
    db.close()
    print("Fundamentals seeding complete ✅")

if __name__ == "__main__":
    seed_fundamentals()