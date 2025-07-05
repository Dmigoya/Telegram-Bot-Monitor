import os
from telegram import Bot


async def run() -> None:
    """Send a test message to confirm bot connectivity."""
    token = os.getenv("BOT_TOKEN")
    user = os.getenv("TELEGRAM_USER_ID")
    if not token or not user:
        raise RuntimeError("BOT_TOKEN and TELEGRAM_USER_ID must be set")
    bot = Bot(token=token)
    await bot.send_message(chat_id=int(user), text="✅ Bot de notificaciones conectado")


if __name__ == "__main__":
    import asyncio
    asyncio.run(run())
