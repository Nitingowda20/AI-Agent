import os
from contextlib import asynccontextmanager

import anyio
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from apscheduler.schedulers.background import BackgroundScheduler

from agent import run
from db import init_db, save_report, get_latest_report, get_history


def _env_bool(name: str, default: str = "1") -> bool:
    return os.getenv(name, default).strip().lower() in ("1", "true", "yes", "y", "on")


ENABLE_SCHEDULER = _env_bool("ENABLE_SCHEDULER", "1")
SCHEDULE_EVERY_MINUTES = int(os.getenv("SCHEDULE_EVERY_MINUTES", "60"))


def job_generate_and_store():
    # Runs in APScheduler thread
    report = run()
    save_report(report)
    print("▶ Saved report to SQLite")


scheduler = BackgroundScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- startup ----
    init_db()

    # Optional: "warm" the model so first real request is faster.
    # llm.invoke(...) is sync in this setup, so run it in a thread:
    try:
        await anyio.to_thread.run_sync(run)  # warm + also saves nothing
        # If you don't want a warm run, remove this line.
    except Exception as e:
        print(f"Warmup failed: {e}")

    if ENABLE_SCHEDULER:
        scheduler.add_job(
            job_generate_and_store,
            trigger="interval",
            minutes=SCHEDULE_EVERY_MINUTES,
            max_instances=1,
            coalesce=True,
        )
        scheduler.start()
        print(f"▶ Scheduler started: every {SCHEDULE_EVERY_MINUTES} minute(s)")
    else:
        print("▶ Scheduler disabled (ENABLE_SCHEDULER=0)")

    yield

    # ---- shutdown ----
    if scheduler.running:
        scheduler.shutdown(wait=False)
        print("▶ Scheduler stopped")


app = FastAPI(lifespan=lifespan)


@app.get("/")
def home():
    return {"status": "Market Agent Running"}


@app.get("/ping")
def ping():
    return {"status": "ok"}


@app.get("/brief")
def brief(force: bool = Query(False, description="Run agent now and store a new report")):
    if force:
        report = run()
        save_report(report)
        pretty = report.replace("\\n", "\n")
        return JSONResponse(content={"report": pretty, "source": "fresh"})

    latest = get_latest_report()
    if not latest:
        report = run()
        save_report(report)
        pretty = report.replace("\\n", "\n")
        return JSONResponse(content={"report": pretty, "source": "fresh-first"})

    pretty = latest["report"].replace("\\n", "\n")
    return JSONResponse(
        content={
            "report": pretty,
            "source": "db",
            "created_at": latest["created_at"],
            "id": latest["id"],
        }
    )


@app.get("/history")
def history(limit: int = 25):
    items = get_history(limit=limit)
    # Keep payload light; dashboard can request more if needed
    return {"items": items}