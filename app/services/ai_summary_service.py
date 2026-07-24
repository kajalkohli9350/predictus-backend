import re

from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_stock_summary(stock, fundamentals):
    if not fundamentals:
        fundamentals_text = "No fundamentals data available."
    else:
        latest = fundamentals[0]
        fundamentals_text = f"""
        Revenue: {latest.revenue}, Net Income: {latest.net_income}, EPS: {latest.eps},
        P/E Ratio: {latest.pe_ratio}, P/B Ratio: {latest.pb_ratio}, Debt to Equity: {latest.debt_to_equity},
        ROE: {latest.roe}%, ROA: {latest.roa}%, Dividend Yield: {latest.dividend_yield}%, Current Ratio: {latest.current_ratio}
        """

    prompt = f"""
    Write a clear, concise 200-word summary for a retail investor about this stock.
    Cover its business context, sector, and what the fundamentals suggest about its financial health.

    Stock: {stock.name} ({stock.symbol})
    Sector: {stock.sector}, Industry: {stock.industry}
    Market Cap: {stock.market_cap}, Exchange: {stock.exchange}

    Fundamentals:
    {fundamentals_text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=350,
    )

    return response.choices[0].message.content

def generate_price_and_news(stock):
    prompt = f"""
    Search the web for the latest stock price and recent news for {stock.name} ({stock.symbol}),
    listed on {stock.exchange}. Give a short summary: current price if available, and 2-3 recent
    news headlines with a one-line description each.
    """

    response = client.responses.create(
        model="gpt-4o-mini",
        tools=[{"type": "web_search_preview"}],
        input=prompt,
    )
    raw_text = response.output_text

    # Markdown links jaise ([source](url)) ko hatao
    cleaned_text = re.sub(r'\(\[[^\]]+\]\([^)]+\)\)', '', raw_text)
    # Agar koi standalone [text](url) bach jaye, usse bhi hatao
    cleaned_text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', cleaned_text)

    return cleaned_text