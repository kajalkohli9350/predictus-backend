import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.database import SessionLocal
from app.models.stock import Stock

def seed_stocks():
    db = SessionLocal()

    with open(os.path.join(os.path.dirname(__file__), "seed_data_100.json")) as f:
        stocks_data = json.load(f)

    added = 0
    for stock in stocks_data:
        existing = db.query(Stock).filter(Stock.symbol == stock["symbol"]).first()
        if existing:
            continue
        new_stock = Stock(**stock)
        db.add(new_stock)
        added += 1

    db.commit()
    db.close()
    print(f"Seeding complete ✅ — {added} new stocks added")

if __name__ == "__main__":
    seed_stocks()