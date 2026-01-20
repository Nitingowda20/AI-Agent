# COMPLETE REPLACEMENT: FIXED data.py
# Fixes: AAPL ticker, numeric market data, robust news filtering, debug prints
import yfinance as yf
from datetime import datetime

DEFAULT_TICKERS = ["SPY", "QQQ", "AAPL", "MSFT", "NVDA", "TSLA", "^VIX"]  # FIXED: AAPL not AAIL

def market_data(tickers=DEFAULT_TICKERS) -> str:
    lines = []
    ts = datetime.utcnow().isoformat() + "Z"
    lines.append(f"Timestamp (UTC): {ts}")
    lines.append("Prices (last close | change | % change):")

    for t in tickers:
        try:
            tk = yf.Ticker(t)
            hist = tk.history(period="5d")
            if hist is None or hist.empty or len(hist) < 2:
                lines.append(f"- {t}: NO DATA")
                continue
            prev = float(hist["Close"].iloc[-2])
            last = float(hist["Close"].iloc[-1])
            chg = last - prev
            chg_pct = (chg / prev) * 100 if prev != 0 else 0.0
            lines.append(f"- {t}: ${last:.2f} ({chg:+.2f}, {chg_pct:+.2f}%)")
        except Exception as e:
            lines.append(f"- {t}: ERROR ({e})")

    return "\n".join(lines)

def news_data(ticker_for_news="SPY", max_items=10) -> str:
    tk = yf.Ticker(ticker_for_news)
    try:
        raw_news = tk.news or []
        print(f"RAW NEWS COUNT: {len(raw_news)}")
        if raw_news:
            print(f"RAW NEWS SAMPLE (first title): {raw_news[0].get('content', {}).get('title', 'NONE')}")
    except Exception as e:
        print(f"NEWS FETCH ERROR: {e}")
        return "News fetch failed."

    cleaned = []
    for i, item in enumerate(raw_news):
        content_dict = item.get("content", {})
        if not isinstance(content_dict, dict):
            continue

        # Title first, then summary
        title = content_dict.get("title") or content_dict.get("summary") or ""
        title = title.strip()
        if not title or len(title) < 10:
            continue

        # SMART TRUNCATE: First 80 chars + "..." if long (prevents prompt bloat)
        if len(title) > 80:
            title = title[:80].rsplit(' ', 1)[0] + "..."

        provider = content_dict.get("provider", {})
        publisher = provider.get("displayName", "") if isinstance(provider, dict) else ""
        publisher = publisher.strip()[:20]  # Short publisher

        entry = f"{i+1}. {title}"
        if publisher:
            entry += f" ({publisher})"
        cleaned.append(entry)

    if not cleaned:
        return "No headlines available. Focus on market prices."

    return f"Top headlines:\n" + "\n".join(cleaned[:max_items])