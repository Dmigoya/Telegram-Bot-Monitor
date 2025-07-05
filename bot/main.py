import asyncio, os, signal
from bot import notifier
from bot import test_connection

INTERVAL = int(os.getenv("CHECK_INTERVAL", 300))

stop_event = asyncio.Event()


async def shutdown() -> None:
    """Send a disconnect notice and stop the loop."""
    await notifier.bot.send_message(
        chat_id=notifier.user_id, text="❌ Bot de notificaciones detenido"
    )
    stop_event.set()

async def main():
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda s=sig: asyncio.create_task(shutdown()))

    await test_connection.run()
    while not stop_event.is_set():
        await notifier.send_report()
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=INTERVAL)
        except asyncio.TimeoutError:
            pass

if __name__ == "__main__":
    asyncio.run(main())
