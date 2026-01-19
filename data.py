import yfinance as yf
import feedparser

def market_data():
    tickers = ["^GSPC", "^DJI", "^IXIC"]
    data = {}
    for t in tickers:
        stock = yf.Ticker(t)
        hist = stock.history(period="1d")
        data[t] = hist.tail(1)["Close"].values[0]
    return data

def news_data():
    feed = feedparser.parse(
        "https://news.google.com/rss/search?q=stock+market+economy"
    )
    return [n.title for n in feed.entries[:8]]
