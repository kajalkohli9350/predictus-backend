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
    roe_score = min(100, (roe / 30.0) * 100)
    roa_score = min(100, (roa / 20.0) * 100)
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