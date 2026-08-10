from app.services.whatsapp_api import send_whatsapp_message

async def process_whatsapp_message(body: dict):
    """
    Desglosa el payload de Meta, extrae el mensaje y decide cómo responder.
    """
    try:
        if body.get("object") == "whatsapp_business_account":
            for entry in body.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    
                    if "messages" in value:
                        message_info = value["messages"][0]
                        sender_phone = message_info["from"]
                        msg_type = message_info.get("type")
                        
                        if msg_type == "text":
                            text = message_info["text"]["body"]
                            print(f"\n📩 Mensaje de {sender_phone}: {text}")
                            
                            # Lógica del Chatbot
                            reply_text = f"Hola! Soy tu asistente virtual. Recibí tu mensaje: '{text}'"
                            
                            await send_whatsapp_message(sender_phone, reply_text)
                        else:
                            print(f"⚠️ Recibido mensaje de tipo no soportado: {msg_type}")
    except Exception as e:
        print(f"❌ Error al procesar el webhook: {e}")
        raise e
