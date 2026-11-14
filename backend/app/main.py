from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend" / "src"

app = FastAPI(title="MailPhish")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


# Register API routes above the frontend mount so the API handles them first.
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
