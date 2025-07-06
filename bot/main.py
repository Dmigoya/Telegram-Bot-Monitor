import asyncio
import os
from importlib import import_module
from pathlib import Path
from telegram import BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes

from bot import notifier
from bot.auth import auth_required

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 300))

_dynamic_handlers = []


def discover_modules():
    modules = []
    for file in Path(__file__).parent.joinpath("modules").glob("*.py"):
        if file.stem == "__init__":
            continue
        mod = import_module(f"bot.modules.{file.stem}")
        modules.append(mod)
    return modules


def build_handler(mod):
    async def handler(update, context):
        await mod.run(update, context)
    return handler


async def register_dynamic_commands(app: Application):
    for h in _dynamic_handlers:
        app.remove_handler(h, group=1)
    _dynamic_handlers.clear()
    commands = []
    for mod in discover_modules():
        handler = CommandHandler(mod.CMD_NAME, auth_required(build_handler(mod)))
        app.add_handler(handler, group=1)
        _dynamic_handlers.append(handler)
        commands.append(BotCommand(mod.CMD_NAME, mod.CMD_DESC))
    await app.bot.set_my_commands(commands)


async def refresh(update, context):
    await register_dynamic_commands(context.application)
    await update.message.reply_text("\ud83d\udd04 Comandos recargados")


async def report_job(context: ContextTypes.DEFAULT_TYPE):
    await notifier.send_report()


def main():
    app = Application.builder().token(os.getenv("BOT_TOKEN")).build()
    asyncio.run(register_dynamic_commands(app))
    app.add_handler(CommandHandler("refresh", auth_required(refresh)), group=0)
    app.job_queue.run_repeating(report_job, interval=CHECK_INTERVAL)
    app.run_polling()


if __name__ == "__main__":
    main()

