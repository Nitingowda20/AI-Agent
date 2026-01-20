
from data import market_data, news_data
from prompts import PROMPT
from langchain_ollama import OllamaLLM

# llm = OllamaLLM(
#     model="tinyllama",
#     temperature=0.1,
#     num_predict=1200,
#     repeat_penalty=1.15,  # ANTI-LOOP
# )
## TINYLLAMA-OPTIMIZED: agent.py LLM config (replace yours)
llm = OllamaLLM(
    model="tinyllama",
    temperature=0.0,      # Zero creativity = copy facts
    num_predict=2500,     # Max room
    repeat_penalty=1.35,  # Kill loops hard
    top_p=0.8,            # Less wild
    top_k=40,             # Restrict vocab drift
)
def run():
    print("▶ Agent started")

    market = market_data()
    print("▶ Market data fetched")

    news = news_data()
    print("▶ News fetched")

    final_prompt = PROMPT.format(market=market, news=news)
    print("▶ Prompt ready, calling LLM")

    # print("=== DEBUG INPUTS ===")
    # print("MARKET PREVIEW:", market[:500] + "..." if len(market) > 500 else market)
    # print("NEWS PREVIEW:", news[:500] + "..." if len(news) > 500 else news)
    # print("====================")

    result = llm.invoke(final_prompt)
    # print("LLM OUTPUT LENGTH:", len(result))
    # print("LLM OUTPUT END:", result[-200:]) 

    print("▶ LLM responded")
    return result