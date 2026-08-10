# Chatbot Meta Webhook 🤖

[![Deploy Chatbot to VM](https://github.com/BETACRD01/Chatbot/actions/workflows/deploy.yml/badge.svg)](https://github.com/BETACRD01/Chatbot/actions/workflows/deploy.yml)

Este es el backend oficial del Chatbot de Upmina, integrado con la **WhatsApp Cloud API** de Meta.

## Arquitectura
- **Framework:** FastAPI (Python)
- **Despliegue Continuo (CI/CD):** GitHub Actions 
- **Servidor:** Ubuntu VM + Nginx + Systemd + Let's Encrypt (HTTPS)

## Funcionalidad actual
- Verificación segura con HMAC-SHA256.
- Recepción de mensajes entrantes de WhatsApp.
- Respuesta automática de prueba ("Hola! Recibí tu mensaje...").

---
*Desarrollado y desplegado de forma automática a producción.*
