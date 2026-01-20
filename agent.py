# from langchain_community.llms import Ollama
from data import market_data, news_data
from prompts import PROMPT

# llm = Ollama(model="mistral")
# def run():
#     market = market_data()
#     news = news_data()

#     final_prompt = PROMPT.format(market=market, news=news)
#     return llm.invoke(final_prompt)

# from langchain_ollama import OllamaLLM
# llm = OllamaLLM(model="phi")  # or tinyllama

from langchain_ollama import OllamaLLM

llm = OllamaLLM(
    model="tinyllama",
    temperature=0.2,
    num_predict=150
)


# def run():
#     market = market_data()
#     news = news_data()
#     final_prompt = PROMPT.format(market=market, news=news)
#     return llm.invoke(final_prompt)
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
