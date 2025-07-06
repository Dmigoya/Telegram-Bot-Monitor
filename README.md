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

Agrega módulos en `bot/modules/` siguiendo la convención:

```python
CMD_NAME = "mem"        # nombre del comando
CMD_DESC = "Uso de RAM" # descripción

def report() -> str:
    ...  # texto para los reportes automáticos

async def run(update, context):
    await update.message.reply_text(report())
```

Ejecuta `/refresh` para que el bot descubra nuevos comandos sin reiniciar.

### Seguridad de comandos
- **Administradores** (`TELEGRAM_ADMIN_IDS`): pueden ejecutar comandos.
- **Receptores**   (`TELEGRAM_REPORT_IDS`): reciben reportes automáticos.

Ambas variables aceptan múltiples IDs separados por coma.
Usuarios no listados obtendrán respuesta 🚫 y, tras `BAN_THRESHOLD` intentos, serán baneados `BAN_TIME` segundos.

