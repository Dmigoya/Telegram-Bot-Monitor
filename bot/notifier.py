import os
from telegram import Bot
from importlib import import_module

bot = Bot(token=os.getenv("BOT_TOKEN"))
user_id = int(os.getenv("TELEGRAM_USER_ID"))

def get_modules():
    from pathlib import Path
    return [f.stem for f in Path(__file__).parent.joinpath("modules").glob("*.py") if f.stem != "__init__"]

async def send_report():
    msgs = []
    for mod_name in get_modules():
        mod = import_module(f"bot.modules.{mod_name}")
        try:
            output = mod.run()
            if output:
                msgs.append(f"[{mod_name}]\n{output}")
        except Exception as e:
            msgs.append(f"[{mod_name}] Error: {e}")
    await bot.send_message(chat_id=user_id, text="\n\n".join(msgs[:10]))
