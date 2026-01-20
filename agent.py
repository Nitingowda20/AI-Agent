
from data import market_data, news_data
from prompts import PROMPT
from langchain_ollama import OllamaLLM

llm = OllamaLLM(
    model="tinyllama",
    temperature=0.2,
    num_predict=1000)
def run():
    print("▶ Agent started")

    market = market_data()
    print("▶ Market data fetched")

    news = news_data()
    print("▶ News fetched")

    final_prompt = PROMPT.format(market=market, news=news)
    print("▶ Prompt ready, calling LLM")

    result = llm.invoke(final_prompt)

    print("▶ LLM responded")
    return result
