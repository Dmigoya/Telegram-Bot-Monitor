# Telegram Monitor Bot 📡

Bot Dockerizado para monitoreo del servidor. Envía por Telegram:

- Seguridad: fail2ban
- Estado del sistema: CPU, RAM, red
- Estado de contenedores Docker

## Uso

1. Copia `.env.example` a `.env` y edítalo.
2. Ejecuta:

```bash
docker compose up -d --build
```

## Expansión

Agrega módulos en `bot/modules/`. Cada módulo debe implementar:

```python
def run() -> str:
    return "Mensaje que será enviado"
```
