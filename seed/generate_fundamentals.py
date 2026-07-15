import json
import random
import os

random.seed(7)

# Sector-wise realistic ranges (approx, for mock/demo data only)
sector_ranges = {
    "IT": {"pe": (18, 32), "pb": (5, 15), "de": (0.0, 0.3), "roe": (18, 42), "roa": (12, 26), "div": (1.0, 3.0), "cr": (1.8, 2.8)},
    "Banking": {"pe": (10, 24), "pb": (1.5, 4.0), "de": (0.5, 1.2), "roe": (10, 20), "roa": (0.8, 2.2), "div": (0.5, 2.0), "cr": (1.0, 1.6)},
    "Pharma": {"pe": (20, 40), "pb": (3, 8), "de": (0.05, 0.4), "roe": (10, 22), "roa": (7, 16), "div": (0.5, 1.8), "cr": (1.5, 2.3)},
    "FMCG": {"pe": (35, 65), "pb": (8, 20), "de": (0.0, 0.3), "roe": (20, 45), "roa": (15, 30), "div": (1.0, 2.5), "cr": (1.2, 2.0)},
    "Industrials": {"pe": (15, 30), "pb": (2, 6), "de": (0.3, 1.2), "roe": (8, 20), "roa": (4, 12), "div": (0.5, 3.5), "cr": (1.0, 1.8)},
    "Energy": {"pe": (8, 20), "pb": (1, 3.5), "de": (0.4, 1.0), "roe": (10, 18), "roa": (5, 10), "div": (2.0, 5.0), "cr": (0.9, 1.5)},
}

def generate_fundamentals(stock):
    sector = stock.get("sector", "Industrials")
    ranges = sector_ranges.get(sector, sector_ranges["Industrials"])

    revenue = round(random.uniform(5000, 260000), 2)
    net_income = round(revenue * random.uniform(0.03, 0.22), 2)
    eps = round(random.uniform(2, 130), 2)

    return {
        "stock_symbol": stock["symbol"],
        "period": "FY2025",
        "revenue": revenue,
        "net_income": net_income,
        "eps": eps,
        "pe_ratio": round(random.uniform(*ranges["pe"]), 2),
        "pb_ratio": round(random.uniform(*ranges["pb"]), 2),
        "debt_to_equity": round(random.uniform(*ranges["de"]), 2),
        "roe": round(random.uniform(*ranges["roe"]), 2),
        "roa": round(random.uniform(*ranges["roa"]), 2),
        "dividend_yield": round(random.uniform(*ranges["div"]), 2),
        "current_ratio": round(random.uniform(*ranges["cr"]), 2),
    }

def main():
    base_dir = os.path.dirname(__file__)

    all_stocks = []
    for filename in ["seed_data.json", "seed_data_100.json"]:
        path = os.path.join(base_dir, filename)
        if os.path.exists(path):
            with open(path) as f:
                all_stocks.extend(json.load(f))

    fundamentals = [generate_fundamentals(s) for s in all_stocks]

    out_path = os.path.join(base_dir, "seed_fundamentals_100.json")
    with open(out_path, "w") as f:
        json.dump(fundamentals, f, indent=2)

    print(f"{len(fundamentals)} fundamentals records generated ✅ -> seed_fundamentals_100.json")

if __name__ == "__main__":
    main()