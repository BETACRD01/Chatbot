import hmac
import hashlib
from fastapi import APIRouter, Request, Query, Header, HTTPException
from fastapi.responses import PlainTextResponse

from app.config import settings
from app.services.message_handler import process_whatsapp_message

router = APIRouter()

def verify_signature(payload: bytes, signature_header: str) -> bool:
    if not settings.APP_SECRET or not signature_header:
        return True # Solo para desarrollo si no hay secreto
    
    expected_hash = hmac.new(
        key=settings.APP_SECRET.encode(),
        msg=payload,
        digestmod=hashlib.sha256
    ).hexdigest()
    
    expected_signature = f"sha256={expected_hash}"
    return hmac.compare_digest(expected_signature, signature_header)

@router.get("/webhook")
async def verify_webhook(
    mode: str = Query(None, alias="hub.mode"),
    token: str = Query(None, alias="hub.verify_token"),
    challenge: str = Query(None, alias="hub.challenge")
):
    if mode and token:
        if mode == "subscribe" and token == settings.VERIFY_TOKEN:
            print("✅ Webhook verificado correctamente por Meta")
            return PlainTextResponse(content=challenge, status_code=200)
        raise HTTPException(status_code=403, detail="El token de verificación no coincide")
    raise HTTPException(status_code=400, detail="Faltan parámetros")

@router.post("/webhook")
async def receive_webhook(request: Request, x_hub_signature_256: str = Header(None)):
    raw_body = await request.body()
    if settings.APP_SECRET and not verify_signature(raw_body, x_hub_signature_256):
        raise HTTPException(status_code=403, detail="Firma inválida")

    body = await request.json()
    
    try:
        await process_whatsapp_message(body)
    except Exception:
        # Devolver 200 OK siempre para evitar reintentos de Meta
        return {"status": "error"}

    return {"status": "ok"}
