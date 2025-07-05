import asyncio
from bot import notifier, test_connection

async def run() -> None:
    await test_connection.run()
    await notifier.send_report()

if __name__ == "__main__":
    asyncio.run(run())
