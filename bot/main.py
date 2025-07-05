import asyncio, os
from bot import notifier

INTERVAL = int(os.getenv("CHECK_INTERVAL", 300))

async def main():
    while True:
        await notifier.send_report()
        await asyncio.sleep(INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
