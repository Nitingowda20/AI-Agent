import yfinance as yf
from datetime import datetime

DEFAULT_TICKERS = ["SPY", "QQQ", "AAPL", "MSFT", "NVDA", "TSLA", "^VIX"]


def market_data(tickers=DEFAULT_TICKERS) -> str:
    lines = []
    lines.append(f"Timestamp: {datetime.utcnow().isoformat()}Z")
    lines.append("Prices (last close vs prior close):")

    for t in tickers:
        tk = yf.Ticker(t)
        hist = tk.history(period="5d")
        if hist is None or hist.empty or len(hist) < 2:
            lines.append(f"- {t}: (no data)")
            continue

        prev = float(hist["Close"].iloc[-2])
        last = float(hist["Close"].iloc[-1])
        chg = last - prev
        chg_pct = (chg / prev) * 100 if prev else 0.0
        lines.append(f"- {t}: {last:.2f} ({chg:+.2f}, {chg_pct:+.2f}%)")

    return "\n".join(lines)


def news_data(ticker_for_news="SPY", max_items=8) -> str:
    tk = yf.Ticker(ticker_for_news)

    items = []
    try:
        items = tk.news or []
    except Exception:
        items = []

    if not items:
        return "No headlines returned."

    lines = [f"Top headlines (via yfinance {ticker_for_news}):"]
    for i, item in enumerate(items[:max_items], start=1):
        title = item.get("title", "Untitled")
        publisher = item.get("publisher", "")
        lines.append(f"{i}. {title} — {publisher}".strip())
    return "\n".join(lines)