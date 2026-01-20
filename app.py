from fastapi import FastAPI
from agent import run

app = FastAPI()


@app.get("/")
def home():
    return {"status": "Market Agent Running"}

@app.get("/brief")
def brief():
    return {"report": run()}

@app.get("/ping")
def ping():
    return {"status": "ok"}
