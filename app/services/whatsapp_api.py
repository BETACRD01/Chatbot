import httpx
from app.config import settings

async def send_whatsapp_message(to_number: str, message: str):
    """
    Envía un mensaje de texto usando la API oficial de WhatsApp Cloud.
    """
    if not settings.WHATSAPP_TOKEN or not settings.PHONE_NUMBER_ID:
        print("⚠️ No se puede enviar el mensaje: Faltan credenciales de WhatsApp en el .env")
        return

    url = f"https://graph.facebook.com/v17.0/{settings.PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_number,
        "type": "text",
        "text": {"preview_url": False, "body": message}
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            print(f"✅ Mensaje enviado a {to_number}")
        except Exception as e:
            print(f"❌ Error al enviar mensaje: {str(e)}")
