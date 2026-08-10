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
                            
                            # === Sistema Híbrido: Reglas + IA ===
                            text_lower = text.lower()
                            reply_text = ""
                            
                            # 1. Reglas (Respuestas rápidas y estáticas)
                            if "hola" in text_lower or "buenos dias" in text_lower:
                                reply_text = "¡Hola! Bienvenido a Upmina. ¿En qué te podemos ayudar hoy?"
                            elif "precio" in text_lower or "costo" in text_lower:
                                reply_text = "Nuestra app Upmina es gratuita, pero ofrecemos un plan premium por $4.99/mes."
                            elif "soporte" in text_lower or "ayuda" in text_lower:
                                reply_text = "Puedes contactar a nuestro equipo de soporte enviando un correo a soporte@upmina.com."
                            
                            # 2. IA (Si ninguna regla coincide)
                            if not reply_text:
                                try:
                                    from app.config import settings
                                    from groq import AsyncGroq
                                    
                                    if settings.GROQ_API_KEY:
                                        client = AsyncGroq(api_key=settings.GROQ_API_KEY)
                                        response = await client.chat.completions.create(
                                            model="llama3-8b-8192",
                                            messages=[
                                                {"role": "system", "content": "Eres el asistente virtual amable de la aplicación móvil Upmina."},
                                                {"role": "user", "content": text}
                                            ],
                                            max_tokens=150
                                        )
                                        reply_text = response.choices[0].message.content
                                    else:
                                        reply_text = "Lo siento, no tengo una respuesta configurada para eso."
                                except Exception as e:
                                    print(f"❌ Error con Groq: {e}")
                                    reply_text = "Lo siento, mi sistema de IA no está disponible en este momento."
                            
                            if reply_text:
                                await send_whatsapp_message(sender_phone, reply_text)
                        else:
                            print(f"⚠️ Recibido mensaje de tipo no soportado: {msg_type}")
    except Exception as e:
        print(f"❌ Error al procesar el webhook: {e}")
        raise e
