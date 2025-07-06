import os
from telegram import Bot
from importlib import import_module

bot = Bot(token=os.getenv("BOT_TOKEN"))
REPORT_IDS = [int(i) for i in os.getenv("TELEGRAM_REPORT_IDS", "").split(',') if i]

def get_modules():
    from pathlib import Path
    return [f.stem for f in Path(__file__).parent.joinpath("modules").glob("*.py") if f.stem != "__init__"]

async def send_report():
    msgs = []
    for mod_name in get_modules():
        mod = import_module(f"bot.modules.{mod_name}")
        try:
            output = mod.report()
            if output:
                msgs.append(f"[{mod_name}]\n{output}")
        except Exception as e:
            msgs.append(f"[{mod_name}] Error: {e}")
    text = "\n\n".join(msgs[:10])
    for rid in REPORT_IDS:
        await bot.send_message(chat_id=rid, text=text)

