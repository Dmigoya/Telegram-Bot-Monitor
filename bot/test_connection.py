import os
from telegram import Bot


async def run() -> None:
    """Send a test message to confirm bot connectivity."""
    token = os.getenv("BOT_TOKEN")
    users = [int(i) for i in os.getenv("TELEGRAM_REPORT_IDS", "").split(',') if i]
    if not token or not users:
        raise RuntimeError("BOT_TOKEN and TELEGRAM_REPORT_IDS must be set")
    bot = Bot(token=token)
    await bot.send_message(chat_id=users[0], text="✅ Bot de notificaciones conectado")


if __name__ == "__main__":
    import asyncio
    asyncio.run(run())

