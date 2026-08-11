from fastapi import FastAPI
import uvicorn

from app.api.webhooks import router as webhooks_router

app = FastAPI(title="Meta Chatbot Webhook (Robust & Scalable)")

app.include_router(webhooks_router, prefix="/api/v1")

from fastapi.responses import HTMLResponse
from pathlib import Path

@app.get("/health")
async def health():
    return {"status": "ok", "message": "Chatbot server is running"}

@app.get("/privacy", response_class=HTMLResponse)
async def privacy_policy():
    html_path = Path(__file__).parent / "templates" / "privacy.html"
    return html_path.read_text(encoding="utf-8")

if __name__ == "__main__":
    print("Iniciando servidor chatbot (Escalable) en el puerto 8000...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
